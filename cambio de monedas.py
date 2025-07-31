from tkinter import *
from tkinter.ttk import Notebook
import Util
import csv
from functional import seq
from datetime import datetime
import matplotlib.pyplot as plt
from functools import reduce

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
    return list(filter(lambda item: item["moneda"] == moneda \
                  and item["fecha"]>= desde \
                  and item["fecha"]<= hasta, datos))


def extraerFechasYCambios(datos):
    fechas = list(map(lambda item: item["fecha"], datos))
    cambios = list(map(lambda item: item["cambio"], datos))
    return fechas, cambios
    
def graficar():
    moneda = monedas [cmbMoneda.current()] #nombre de la moneda escogida
    desde = cldDesde.get_date()
    hasta = cldHasta.get_date()
    datos = obtenerDatos()
    datosFiltrados = filtrarDatos(datos, moneda, desde, hasta)
    fechas, cambios = extraerFechasYCambios(datosFiltrados)

    #grafica
    plt.plot(fechas,cambios)
    plt.ylabel(f"Cambios de {moneda}")
    plt.xlabel("Fecha")
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("graficamonedas.png")

    #mostrar la grafica en el panel

    lblGrafica = Label(paneles[0])
    imgGrafica = PhotoImage(file="graficamonedas.png")
    lblGrafica.configure(image=imgGrafica)
    lblGrafica.image=imgGrafica
    lblGrafica.place(x=0,y=0)

    v.minsize(imgGrafica.width(), imgGrafica.height()+100)

def calcularPromedio(datos):
    return reduce(lambda suma, item: suma+item, datos)/ len(datos) if datos else 0

def calcularDesviacionEstandar(datos):
    promedio = calcularPromedio(datos)
    return reduce(lambda suma, item: suma+(item-promedio)**2, datos)/ len(datos) if datos else 0 

def obtenerEstadisticas():
    moneda = monedas [cmbMoneda.current()] #nombre de la moneda escogida
    desde = cldDesde.get_date()
    hasta = cldHasta.get_date()
    datos = obtenerDatos()
    datosFiltrados = filtrarDatos(datos, moneda, desde, hasta)
    cambios = list(map(lambda item: item["cambio"], datosFiltrados))
    print(calcularPromedio(cambios))
    print(calcularDesviacionEstandar(cambios))

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
    paneles.append(panel)
    
