import mysql.connector
import tkinter as tk
from tkinter import messagebox

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="plant_inventory"
)
cursor = conn.cursor()

tables = {
    "семена": "seeds",
    "растения": "plants",
    "цветы": "flowers",
    "товары для сада": "garden_goods",
    "разное": "miscellaneous"
}



conn.commit()

for table_name in tables.values():
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), quantity INT)")


def show_table_content(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    items = cursor.fetchall()
    text.delete(1.0, tk.END)
    for item in items:
        text.insert(tk.END, f"ID: {item[0]}, Наименование: {item[1]}, Количество: {item[2]}\n")



def update_quantity(table_name):
    item_id = entry_id.get()
    new_quantity = entry_new_quantity.get()
    cursor.execute(f"UPDATE {table_name} SET quantity = %s WHERE id = %s", (new_quantity, item_id))
    conn.commit()
    messagebox.showinfo("Успех", "Количество успешно изменено")
    show_table_content(table_name)


def delete_item(table_name):
    item_id = entry_id.get()
    cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (item_id,))
    conn.commit()
    messagebox.showinfo("Успех", "Объект успешно удален")
    show_table_content(table_name)


def add_item(table_name):
    item_name = entry_name.get()
    item_quantity = entry_quantity.get()
    cursor.execute(f"INSERT INTO {table_name} (name, quantity) VALUES (%s, %s)", (item_name, item_quantity))
    conn.commit()
    messagebox.showinfo("Успех", "Объект успешно добавлен")
    show_table_content(table_name)



root = tk.Tk()
root.title("Учет склада растений")

menu_frame = tk.Frame(root)
menu_frame.pack()

buttons = {}


def on_category_click(category):
    table_name = tables[category]
    show_table_content(table_name)

    for btn in buttons.values():
        btn.config(bg="SystemButtonFace")
    buttons[category].config(bg="lightblue")

    button_add.config(command=lambda: add_item(table_name))
    button_update.config(command=lambda: update_quantity(table_name))
    button_delete.config(command=lambda: delete_item(table_name))


for category in tables.keys():
    button = tk.Button(menu_frame, text=category, command=lambda c=category: on_category_click(c))
    buttons[category] = button
    button.pack(side=tk.LEFT)

label_name = tk.Label(root, text="Наименование:")
label_name.pack()

entry_name = tk.Entry(root)
entry_name.pack()

label_quantity = tk.Label(root, text="Количество:")
label_quantity.pack()

entry_quantity = tk.Entry(root)
entry_quantity.pack()

label_id = tk.Label(root, text="ID объекта:")
label_id.pack()

entry_id = tk.Entry(root)
entry_id.pack()

label_new_quantity = tk.Label(root, text="Новое количество:")
label_new_quantity.pack()

entry_new_quantity = tk.Entry(root)
entry_new_quantity.pack()

button_update = tk.Button(root, text="Изменить количество")
button_update.pack()

button_delete = tk.Button(root, text="Удалить объект")
button_delete.pack()

button_add = tk.Button(root, text="Добавить объект")
button_add.pack()

text = tk.Text(root)
text.pack()

root.mainloop()


cursor.close()
conn.close()


