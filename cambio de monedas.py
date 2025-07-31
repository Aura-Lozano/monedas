from tkinter import *
from tkinter.ttk import Notebook
import Util
import csv
from functional import seq
from datetime import datetime

#subrutinas
def obtenerMonedas():
    with open("./datos/Cambios Monedas.csv") as archivo:
        monedas = seq(csv.reader(archivo)).drop(1) \
                  .map(lambda linea: linea[0]) \
                  .distinct() \
                  .to_list()
    return monedas
        
def obtenerDatos():
    with open("./datos/Cambios Monedas.csv") as archivo:
        datosCSV = csv.reader(archivo)
        next(datosCSV)
        return [
            { "moneda": linea[0], \
              "fecha": datetime.strptime(linea[1], "%d/%m/%Y").date(),
              "cambio": float(linea[2]) \
            } for linea in datosCSV
            ]


def filtrarDatos(datos, moneda, desde, hasta):
    return filter(lambda item: item["moneda"] == moneda \
                  and item["fecha"]>= desde \
                  and item["fecha"]<= hasta, datos)


def extraerFechasYCambios(datos):
    fechas = map(lambda item: item["fecha"], datos)
    cambios = map(lambda item: item["cambio"], datos)
    return fechas, cambios
    
def graficar():
    moneda = monedas [cmbMoneda.current()] #nombre de la moneda escogida
    desde = cldDesde.get_date()
    hasta = cldHasta.get_date()
    datos = obtenerDatos()
    datosFiltrados = filtrarDatos(datos, moneda, desde, hasta)
    fechas, cambios = extraerFechasYCambios(datosFiltrados)
    for fecha in fechas:
        print(fecha)
    for cambio in cambios:
        print(cambio)




        

    

def obtenerEstadisticas():
    pass

#Programa principal
v = Tk()
v.title("cambios de moneda")
v.geometry("500x300")

iconos =["./iconos/grafico.png", "./iconos/Icono 1.png"]
textos=["Gráfica cambio vs fecha","Estadisticas"]

botones = Util.agregarBarra(v, iconos,textos)
botones[0].configure(command = graficar)
botones[1].configure(command = obtenerEstadisticas)

#Agregar panel para seleccionar monedas y rango de fechas
panel = Frame(v)
panel.pack(side=TOP, fill=X)

monedas= obtenerMonedas()

Util.agregarEtiqueta(panel, "Moneda:", 0,0)
cmbMoneda =Util.agregarLista(panel, monedas, 0, 1)
Util.agregarEtiqueta(panel, "Desde:", 0,2)
cldDesde =Util.agregarCalendario(panel, 0, 3)
Util.agregarEtiqueta(panel, "Hasta:", 0,4)
cldHasta =Util.agregarCalendario(panel, 0, 5)

panelPestañas = Notebook(v)
panelPestañas.pack(fill=BOTH, expand=YES)

paneles = []
for texto in textos:
    panel = Frame(v)
    panelPestañas.add(panel, text=texto)
    
