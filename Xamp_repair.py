import shutil
import os
import tkinter as tk
from tkinter import filedialog


# Reparar error Xamp "error: mysql shutdown unexpectedly." de forma autmática
#Sin perder los datos de la base de datos
#Autor Llorens19
#Fecha 29/01/2023
#Versión 1.2
#1.1 Solución error que no copiaba los archivos de dentro de las carpetas que seleccionábamos
#Testeado sobre el xamp



#####################################################
#Importante, tener los servicios del xamp parados#
#####################################################


def borrar_carpeta(ruta):
    try:
        shutil.rmtree(ruta)
        print("Correcto")
    except Exception as e:
        print(f"Error")


def cambiar_nombre_carpeta(ruta_original, nuevo_nombre):
    try:
        #la función dirname nos retrocede una direccion, es decir, nos da la ruta padre de la ruta qeu le damos
        nueva_ruta =os.path.dirname(ruta_original) + "/" + nuevo_nombre 

        os.rename(ruta_original, nueva_ruta)

        print(f"Correcto")
    except Exception as e:
        print(f"Error")

def crear_carpeta(ruta, nombre_carpeta):
    try:
        nueva_ruta = ruta + "/" + nombre_carpeta
        
        os.makedirs(nueva_ruta)

        print("Correcto")
    except Exception as e:
        print("Error")


def copiar(origen, destino):
    try:
        # Si la carpeta destino no existe la creamos
        if not os.path.exists(destino):
            os.makedirs(destino)

        # Copiar cada archivo individualmente
        for elemento in os.listdir(origen):
            f_ruta_origen = origen + "/" + elemento
            f_ruta_destino = destino + "/" + elemento

            #En caso de ser una carpeta, volveremos a llamar a la función para que también se copien los archivos que hay dentro de ella
            #En caso de ser un archivo, lo copiaremos directamente 
            if os.path.isdir(f_ruta_origen):
                copiar(f_ruta_origen, f_ruta_destino)
            else:
                shutil.copy2(f_ruta_origen, f_ruta_destino)

        print("Correcto")
    except Exception as e:
        print("Error")


def copiar_archivo(origen, destino):
    try:
        shutil.copy(origen, destino)

        print("Correcto")
    except Exception as e:
        print("Error")


def copiar_carpetas(origen, destino):
    try:
        # Si la carpeta destino no existe la creamos
        if not os.path.exists(destino):
            os.makedirs(destino)

        # Copiar solo los directorios desde la carpeta de origen a la carpeta de destino
        for elemento in os.listdir(origen):
            f_ruta_origen = origen + "/" + elemento
            f_ruta_destino = destino + "/" + elemento
            
            #En este caso solo queremos copiar las carpetas, por tanto, si encontramos archivos no los copiamos
            if os.path.isdir(f_ruta_origen):
                # copiar_carpetas(f_ruta_origen, f_ruta_destino)
                copiar(f_ruta_origen, f_ruta_destino) #Como en este caso si queremos que se copien los archivos de dentro, usmos esta función


        print("Correcto")
    except Exception as e:
        print("Error")





class AplicacionReparacionXamp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Reparación Xamp")
        self.geometry("400x300")


        self.ruta_label = tk.Label(self, text="Seleccione la ruta de mysql: ")
        self.ruta_label.pack(pady=10)

        self.ruta_entry = tk.Entry(self, width=40)
        self.ruta_entry.pack(pady=10)

        self.seleccionar_ruta_button = tk.Button(self, text="Seleccionar Ruta", command=self.seleccionar_ruta)
        self.seleccionar_ruta_button.pack(pady=10)

        self.ejecutar_button = tk.Button(self, text="Ejecutar Reparación", command=self.ejecutar_reparacion)
        self.ejecutar_button.pack(pady=10)

        self.ruta_label = tk.Label(self, text="Created by Llorens19")
        self.ruta_label.pack(pady=55)
    def seleccionar_ruta(self):
        ruta_seleccionada = filedialog.askdirectory()
        self.ruta_entry.delete(0, tk.END)
        self.ruta_entry.insert(0, ruta_seleccionada)

    def ejecutar_reparacion(self):
        ruta = self.ruta_entry.get()


        carpeta_borrar = "data-old"
        carpeta_cambiar = "data"
        carpeta_cambiar_nuevo_nombre = "data-old"
        carpeta_nueva = "data"
        carpeta_origen = "backup"
        carpeta_destino = "data"
        archivo_origen = "data-old/ibdata1"
        carpeta_origen_2 = "data-old"
        carpeta_destino_2 = "temporal"
        carpeta_borrar_2 = "mysql"
        carpeta_borrar_3 = "performance_schema"
        carpeta_borrar_4 = "phpmyadmin"

        ruta_borrar = ruta + "/" + carpeta_borrar
        ruta_cambiar = ruta + "/" + carpeta_cambiar
        ruta_nueva = ruta
        ruta_origen = ruta + "/" + carpeta_origen
        ruta_destino = ruta + "/" + carpeta_destino
        ruta_archivo_origen = ruta + "/" + archivo_origen
        ruta_origen_2 = ruta + "/" + carpeta_origen_2
        ruta_destino_2 = ruta + "/" + carpeta_destino_2
        ruta_borrar_2 = ruta + "/temporal/" + carpeta_borrar_2
        ruta_borrar_3 = ruta + "/temporal/" + carpeta_borrar_3
        ruta_borrar_4 = ruta + "/temporal/" + carpeta_borrar_4
        ruta_temporal = ruta + "/temporal"

        #Borramos la carpeta  data-old, por si ya hemos usado antes este programa, 
        #de todas formas, si no se borra se sobreescribe


        borrar_carpeta(ruta_borrar)

        #Cambiamos el nombre de la carpeta data a data-old

        cambiar_nombre_carpeta(ruta_cambiar, carpeta_cambiar_nuevo_nombre)

        #Creamos la carpeta data otra vez

        crear_carpeta(ruta_nueva, carpeta_nueva)

        #Copiamos los archivos de la carpeta backup a la carpeta data

        copiar(ruta_origen, ruta_destino)

        #Copiamos el archivo ibdata1 a la carpeta data

        copiar_archivo(ruta_archivo_origen, ruta_destino)

        #Creamos una ccarpeta de apollo
        #Esto se hace por que debido a mis conociemientos limitados de python, 
        #No he sabido copiar de forma selectiva todas las carpetas escepto 3
        #y como dependiendo de las db que tenemos creadas cada uno,
        #es imposible saber el nombre de las carpetas que hay que copiar y cuales no,
        #Una posible solución sería crer otra funcion de copiar carpetas y dentro del bucle, 
        #discriminar estas tres carpetas que se crean pero he decidido no complicarme.

        crear_carpeta(ruta_nueva, "temporal")

        #Copiamos SOLO las carpetas de data-old a temporal
        copiar_carpetas(ruta_origen_2, ruta_destino_2)

        #Borramos las carpetas que no deseamos copiar
        borrar_carpeta(ruta_borrar_2)

        borrar_carpeta(ruta_borrar_3)

        borrar_carpeta(ruta_borrar_4)

        #Copiamos las carpetas de temporal a data

        copiar(ruta_destino_2, ruta_destino)

        #Borramos la carpeta temporal

        borrar_carpeta(ruta_temporal)

        tk.messagebox.showinfo("Reparación Xamp", "Reparación completada con éxito")
if __name__ == "__main__":
    app = AplicacionReparacionXamp()
    app.mainloop()




