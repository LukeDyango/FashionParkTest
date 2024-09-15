#Test 1 sin IA (Este lo probe y se demora en ejecutar pero funciona)

import pandas as pd

df1 = pd.read_csv("C:/Users/lukas/Desktop/TestFSP/compras_202301.csv", delimiter=';')
df2 = pd.read_csv("C:/Users/lukas/Desktop/TestFSP/compras_202302.csv", delimiter=';')
df3 = pd.read_csv("C:/Users/lukas/Desktop/TestFSP/compras_202303.csv", delimiter=';')
df4 = pd.read_csv("C:/Users/lukas/Desktop/TestFSP/compras_202304.csv", delimiter=';')
df5 = pd.read_csv("C:/Users/lukas/Desktop/TestFSP/compras_202305.csv", delimiter=';')
df6 = pd.read_csv("C:/Users/lukas/Desktop/TestFSP/compras_202306.csv", delimiter=';')
df7 = pd.read_csv("C:/Users/lukas/Desktop/TestFSP/compras_202307.csv", delimiter=';')
df8 = pd.read_csv("C:/Users/lukas/Desktop/TestFSP/compras_202308.csv", delimiter=';')
df9 = pd.read_csv("C:/Users/lukas/Desktop/TestFSP/compras_202309.csv", delimiter=';')
df10 = pd.read_csv("C:/Users/lukas/Desktop/TestFSP/compras_202310.csv", delimiter=';')
df11 = pd.read_csv("C:/Users/lukas/Desktop/TestFSP/compras_202311.csv", delimiter=';')
df12 = pd.read_csv("C:/Users/lukas/Desktop/TestFSP/compras_202312.csv", delimiter=';')


all_data = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12])


all_data['creation_date'] = pd.to_datetime(all_data['creation_date']).dt.strftime('%Y-%m-%d')


all_data['buy'] = all_data['buy'].astype(int)
all_data['amount'] = all_data['amount'].astype(float)
all_data['times'] = all_data['times'].astype(int)


all_data['compras_u3m'] = 0
all_data['monto_compras_u3m'] = 0.0
all_data['veces_compras_u3m'] = 0
all_data['periodo_ultima_compra'] = 0
all_data['meses_sin_comprar'] = 0


all_data = all_data.sort_values(by=['account', 'period'])


df_grouped = all_data.groupby('account')

for account, group in df_grouped:
    
    group = group.sort_values(by='period')
    
    
    for i in range(3, len(group)):
        current_period = group.iloc[i]
        last_3_months = group.iloc[i-3:i]
        
        compras_u3m = last_3_months['buy'].sum() > 0
        monto_compras_u3m = last_3_months['amount'].sum()
        veces_compras_u3m = last_3_months['times'].sum()
        
        all_data.loc[(all_data['account'] == account) & (all_data['period'] == current_period['period']), 'compras_u3m'] = int(compras_u3m)
        all_data.loc[(all_data['account'] == account) & (all_data['period'] == current_period['period']), 'monto_compras_u3m'] = monto_compras_u3m
        all_data.loc[(all_data['account'] == account) & (all_data['period'] == current_period['period']), 'veces_compras_u3m'] = veces_compras_u3m
    
    
    last_buy_period = 0
    for i in range(len(group)):
        current_period = group.iloc[i]
        
        if current_period['buy'] > 0:
            last_buy_period = current_period['period']
            all_data.loc[(all_data['account'] == account) & (all_data['period'] == current_period['period']), 'periodo_ultima_compra'] = last_buy_period
            all_data.loc[(all_data['account'] == account) & (all_data['period'] == current_period['period']), 'meses_sin_comprar'] = 0
        else:
            if last_buy_period != 0:
                months_since_last_buy = int(current_period['period']) - int(last_buy_period)
                all_data.loc[(all_data['account'] == account) & (all_data['period'] == current_period['period']), 'meses_sin_comprar'] = months_since_last_buy


all_data.to_csv("C:/Users/lukas/Desktop/TestFSP/compras.csv", index=False)

all_data
----------------------------------------------------------------------------------------------------------------------
##CODIGO OPTIMIZADO

import pandas as pd

# Load data
file_paths = [f"C:/Users/lukas/Desktop/TestFSP/compras_2023{i:02}.csv" for i in range(1, 13)]
dfs = [pd.read_csv(file_path, delimiter=';') for file_path in file_paths]
all_data = pd.concat(dfs)

# Convert data types
all_data['creation_date'] = pd.to_datetime(all_data['creation_date']).dt.strftime('%Y-%m-%d')
all_data['buy'] = all_data['buy'].astype(int)
all_data['amount'] = all_data['amount'].astype(float)
all_data['times'] = all_data['times'].astype(int)

# Initialize new columns
all_data['compras_u3m'] = 0
all_data['monto_compras_u3m'] = 0.0
all_data['veces_compras_u3m'] = 0
all_data['periodo_ultima_compra'] = 0
all_data['meses_sin_comprar'] = 0

# Sort values
all_data = all_data.sort_values(by=['account', 'period'])

# Group by account
df_grouped = all_data.groupby('account')

# Define a function to process each group
def process_group(group):
    # Compute rolling sums for the last 3 months
    group['compras_u3m'] = group['buy'].rolling(3, min_periods=1).sum().shift(1).fillna(0).astype(int)
    group['monto_compras_u3m'] = group['amount'].rolling(3, min_periods=1).sum().shift(1).fillna(0)
    group['veces_compras_u3m'] = group['times'].rolling(3, min_periods=1).sum().shift(1).fillna(0).astype(int)
    
    # Compute last buy period and months since last buy
    last_buy_period = 0
    for i in range(len(group)):
        current_period = group.iloc[i]
        if current_period['buy'] > 0:
            last_buy_period = current_period['period']
            group.at[group.index[i], 'periodo_ultima_compra'] = last_buy_period
            group.at[group.index[i], 'meses_sin_comprar'] = 0
        else:
            if last_buy_period != 0:
                months_since_last_buy = int(current_period['period']) - int(last_buy_period)
                group.at[group.index[i], 'meses_sin_comprar'] = months_since_last_buy
                
    return group

# Apply the function to each group
all_data = df_grouped.apply(process_group).reset_index(drop=True)

# Save the result
all_data.to_csv("C:/Users/lukas/Desktop/TestFSP/compras.csv", index=False)

# Display the final DataFrame
all_data

--------------------------------------------------------------------------------------------------------------------------

#Test 1 con IA

import os
import pandas as pd
import numpy as np

# Directorio de archivos
path = r"C:/Users/lukas/Desktop/TestFSP"

# Listar archivos
files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.csv')]
print(f'Archivos encontrados: {len(files)}')
print(files)

# Lista para almacenar los DataFrames
df_list = []

# Leer y procesar cada archivo
for file in files:
    print(f"Leyendo archivo: {file}")
    
    # Leer el archivo con un separador incorrecto para manejar el encabezado malformado
    df = pd.read_csv(file, sep=";")
    
    # Si el archivo solo tiene una columna, es probable que el encabezado esté malformado
    if len(df.columns) == 1:
        df = pd.read_csv(file, sep=";")
        df.columns = ['account', 'period', 'creation_date', 'buy', 'amount', 'times']
        print("El archivo tenía un encabezado malformado. Columnas corregidas.")
    
    # Asegurarse de que todas las columnas existen
    for col in ['account', 'period', 'creation_date', 'buy', 'amount', 'times']:
        if col not in df.columns:
            df[col] = np.nan
            print(f"El archivo {file} no tiene la columna '{col}'. Agregando columna vacía.")
    
    # Reemplazar valores NaN con un valor por defecto
    df['account'] = df['account'].fillna('<NA>')
    df['period'] = df['period'].fillna('<NA>')
    df['creation_date'] = pd.to_datetime(df['creation_date'], errors='coerce')
    df['buy'] = df['buy'].fillna(0).astype(int)
    df['amount'] = df['amount'].fillna('<NA>')
    df['times'] = df['times'].fillna(0).astype(int)
    
    df_list.append(df)

# Concatenar todos los DataFrames
combined_df = pd.concat(df_list, ignore_index=True)
print(f"Total de filas combinadas: {len(combined_df)}")

# Convertir columnas a los tipos adecuados
combined_df['creation_date'] = combined_df['creation_date'].dt.strftime('%Y-%m-%d')
combined_df['period'] = combined_df['period'].replace('<NA>', '0').astype(int)

# Creación de las nuevas variables
combined_df['compras_u3m'] = 0
combined_df['monto_compras_u3m'] = 0.0

print(combined_df.head())

---------------------------------------------------------------------------------------------------------------------------

#Test 2

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
