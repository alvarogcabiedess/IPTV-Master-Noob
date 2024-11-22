from datetime import datetime

# Definir el nombre del archivo
filename = "workflow.dat"

# Obtener la hora actual
hora_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Abrir (o crear si no existe) el archivo en modo de escritura (sobrescribir si existe)
with open(filename, 'w') as file:
    # Escribir contenido en el archivo
    file.write("Este es un archivo creado por un script de Python.\n")
    file.write("Esto ha sido hecho como parte de un workflow.\n")
    
    # Escribir la hora de creación al final del archivo
    file.write(f"\nHora de creación: {hora_creacion}\n")
    
print(f"El archivo '{filename}' ha sido creado, sobrescrito y escrito exitosamente.")
