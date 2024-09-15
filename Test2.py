import csv
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Ruta del archivo CSV
file_path = 'C:/Users/lukas/Desktop/TestFSP/mantenedor_clientes.csv'

# Función para escribir los datos en el archivo CSV
def save_client():
    rut = entry_rut.get()
    name = entry_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    channel = channel_var.get()
    date = datetime.now().strftime('%Y-%m-%d')
    user = user_var.get()

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([rut, name, last_name, email, phone, channel, date, user])

    # Limpiar los campos después de guardar
    entry_rut.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_phone.delete(0, tk.END)

# Crear la ventana principal
root = tk.Tk()
root.title('Formulario de Ingreso de Clientes')

# Crear y colocar las etiquetas y entradas
tk.Label(root, text='RUT:').grid(row=0, column=0, padx=10, pady=5)
entry_rut = tk.Entry(root)
entry_rut.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text='Nombre:').grid(row=1, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text='Apellido:').grid(row=2, column=0, padx=10, pady=5)
entry_last_name = tk.Entry(root)
entry_last_name.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text='Email:').grid(row=3, column=0, padx=10, pady=5)
entry_email = tk.Entry(root)
entry_email.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text='Teléfono:').grid(row=4, column=0, padx=10, pady=5)
entry_phone = tk.Entry(root)
entry_phone.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text='Canal de Ingreso:').grid(row=5, column=0, padx=10, pady=5)
channel_var = tk.StringVar()
channel_menu = ttk.Combobox(root, textvariable=channel_var)
channel_menu['values'] = ['Call Center', 'Web', 'Email']
channel_menu.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text='Usuario:').grid(row=6, column=0, padx=10, pady=5)
user_var = tk.StringVar()
user_menu = ttk.Combobox(root, textvariable=user_var)
user_menu['values'] = ['AC1', 'AC2', 'AC3', 'JC']
user_menu.grid(row=6, column=1, padx=10, pady=5)

# Botón para guardar los datos
btn_save = tk.Button(root, text='Guardar Cliente', command=save_client)
btn_save.grid(row=7, columnspan=2, pady=10)

# Ejecutar la aplicación
root.mainloop()

