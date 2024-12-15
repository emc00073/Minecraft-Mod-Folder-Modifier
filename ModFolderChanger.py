import json
import os
import shutil
import tkinter as tk
from tkinter import messagebox
import sys
from datetime import datetime

# Obtener la ruta del directorio actual donde se encuentra el script
if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable)
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))

# Limpiar el contenido del archivo de salida al iniciar el script
output_file_path = os.path.join(current_dir, 'ModFolderChangerOutput.txt')
with open(output_file_path, 'w') as log_file:
    log_file.write("")

# Función para manejar la selección del perfil
def select_profile(profile_key):
    global selected_profile
    selected_profile = profile_key
    update_last_used(profile_key)
    root.destroy()

# Función para actualizar la variable "lastUsed"
def update_last_used(profile_key):
    launcher_profiles_path = os.path.join(current_dir, 'launcher_profiles.json')
    with open(launcher_profiles_path, 'r') as file:
        data = json.load(file)
    
    # Actualizar la variable "lastUsed" del perfil seleccionado
    data['profiles'][profile_key]['lastUsed'] = datetime.utcnow().isoformat() + 'Z'
    
    # Guardar los cambios en el archivo
    with open(launcher_profiles_path, 'w') as file:
        json.dump(data, file, indent=4)

# Primero se abrirá el archivo ./launcher_profiles.json y se buscará aquellos perfiles que empiecen por fabric-loader o forge
launcher_profiles_path = os.path.join(current_dir, 'launcher_profiles.json')
with open(launcher_profiles_path, 'r') as file:
    data = json.load(file)

# Iterar sobre los perfiles y modificar la variable key de aquellos que empiecen por 'forge', asignándoles el campo 'name'
# for key, value in data['profiles'].items():
#     if key.startswith('forge'):
#         key = f"{value['name']}"
#         data['profiles'][key] = data['profiles'].pop(key)

# Filtrar los perfiles que empiecen por 'fabric-loader' o 'forge'
profiles = {k: v for k, v in data['profiles'].items() if k.startswith('fabric-loader') or k.startswith('forge')}

# Ordenar los perfiles en orden descendente
sorted_profiles = dict(sorted(profiles.items(), key=lambda item: tuple(map(int, item[0].split('-')[-1].split('.'))), reverse=True))

# Se mostrará una lista de los perfiles encontrados y se pedirá al usuario que seleccione uno de ellos
if not sorted_profiles:
    with open(output_file_path, 'a') as log_file:
        log_file.write("No se encontraron perfiles que empiecen por 'fabric-loader' o 'forge'.\n")
    print("No se encontraron perfiles que empiecen por 'fabric-loader' o 'forge'.")
    sys.exit(1)

# Crear una ventana para la selección del perfil
root = tk.Tk()
root.title("Seleccionar Perfil")

# Definir el tamaño de la ventana
window_width = 300
button_height = 30
window_height = button_height * len(sorted_profiles) + 25  #25 for padding and title bar

# Obtener el tamaño de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular la posición de la ventana para que esté centrada
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
root.resizable(False, False)  # Hacer la ventana no redimensionable

# Manejar el cierre de la ventana sin selección
def on_closing():
    with open(output_file_path, 'a') as log_file:
        log_file.write("No se seleccionó ningún perfil.\n")
    root.destroy()
    sys.exit(1)

root.protocol("WM_DELETE_WINDOW", on_closing)

button_width = 15  # Definir un ancho fijo para los botones
for profile_key in sorted_profiles.keys():
    button = tk.Button(root, text=f"{'Fabric - ' if 'fabric' in profile_key else 'Forge - '} {profile_key.split('-')[-1]}", command=lambda pk=profile_key: select_profile(pk), width=button_width)
    button.pack(pady=5)

root.mainloop()

# Verificar si se ha seleccionado un perfil
if 'selected_profile' not in globals():
    with open(output_file_path, 'a') as log_file:
        log_file.write("No se seleccionó ningún perfil.\n")
    print("No se seleccionó ningún perfil.")
    sys.exit(1)

with open(output_file_path, 'a') as log_file:
    log_file.write(f"Has seleccionado el perfil: {selected_profile}\n")
print(f"Has seleccionado el perfil: {selected_profile}")

# Ahora se buscará una carpeta mods_versions en la misma carpeta que este script
# y dentro de ella, otra carpeta con la versión del perfil seleccionado.

# Definir la ruta de la carpeta mods_versions
mods_versions_dir = os.path.join(current_dir, 'mods_versions')

# Obtener la versión del perfil seleccionado
selected_profile_version = selected_profile.split('-')[-1]  # Extraer la versión de la key del perfil
with open(output_file_path, 'a') as log_file:
    log_file.write(f"Versión del perfil seleccionado: {selected_profile_version}\n")
print(f"Versión del perfil seleccionado: {selected_profile_version}")

# Definir la ruta de la carpeta con la versión del perfil seleccionado
version_folder = os.path.join(mods_versions_dir, selected_profile_version)
with open(output_file_path, 'a') as log_file:
    log_file.write(f"Ruta de la carpeta de la versión: {os.path.relpath(version_folder)}\n")
print(f"Ruta de la carpeta de la versión: {os.path.relpath(version_folder)}")

# Verificar si la carpeta existe
if os.path.exists(version_folder) and os.path.isdir(version_folder):
    with open(output_file_path, 'a') as log_file:
        log_file.write(f"Carpeta encontrada: {os.path.relpath(version_folder)}\n")
    print(f"Carpeta encontrada: {os.path.relpath(version_folder)}")
else:
    with open(output_file_path, 'a') as log_file:
        log_file.write(f"No se encontró la carpeta para la versión: {selected_profile_version}\n")
    print(f"No se encontró la carpeta para la versión: {selected_profile_version}")
    sys.exit(1)

# Ahora se procederá a copiar el contenido de la carpeta de la versión seleccionada a la carpeta mods, 
# eliminando el contenido anterior.

# Definir la ruta de la carpeta mods
mods_folder = os.path.join(current_dir, 'mods')

# Verificar si la carpeta mods existe, si no, crearla
if not os.path.exists(mods_folder):
    os.makedirs(mods_folder)

# Eliminar el contenido anterior de la carpeta mods
for filename in os.listdir(mods_folder):
    file_path = os.path.join(mods_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        with open(output_file_path, 'a') as log_file:
            log_file.write(f'Eliminado: {os.path.relpath(file_path)}\n')
        print(f'Eliminado: {os.path.relpath(file_path)}')
    except Exception as e:
        with open(output_file_path, 'a') as log_file:
            log_file.write(f'No se pudo eliminar {os.path.relpath(file_path)}. Razón: {e}\n')
        print(f'No se pudo eliminar {os.path.relpath(file_path)}. Razón: {e}')

# Copiar solo archivos .jar de la carpeta de la versión seleccionada a la carpeta mods
for item in os.listdir(version_folder):
    s = os.path.join(version_folder, item)
    d = os.path.join(mods_folder, item)
    try:
        if os.path.isfile(s) and s.endswith('.jar'):
            shutil.copy2(s, d)
            with open(output_file_path, 'a') as log_file:
                log_file.write(f'Copiado: {os.path.relpath(s)} a {os.path.relpath(d)}\n')
            print(f'Copiado: {os.path.relpath(s)} a {os.path.relpath(d)}')
    except Exception as e:
        with open(output_file_path, 'a') as log_file:
            log_file.write(f'No se pudo copiar {os.path.relpath(s)} a {os.path.relpath(d)}. Razón: {e}\n')
        print(f'No se pudo copiar {os.path.relpath(s)} a {os.path.relpath(d)}. Razón: {e}')

with open(output_file_path, 'a') as log_file:
    log_file.write(f"Contenido de {os.path.relpath(version_folder)} copiado a {os.path.relpath(mods_folder)}\n")
print(f"Contenido de {os.path.relpath(version_folder)} copiado a {os.path.relpath(mods_folder)}")