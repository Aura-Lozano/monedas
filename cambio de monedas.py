from tkinter import *
import Util


v = Tk()
v.title("cambios de moneda")
v.geometry("500x300")

iconos =["./iconos/grafico.png", "./iconos/Icono 1.png"]
textos=["Gráfica cambio vs fecha","Estadisticas"]

botones = Util.agregarBarra(v, iconos,textos)

panel = Frame(v)
panel.pack(side=TOP, fill=X)

Util.agregarEtiqueta(panel, "Moneda:", 0,0)
cmbMoneda =Util.agregarLista(panel, [], 0, 1)
Util.agregarEtiqueta(panel, "Desde:", 0,2)
cmbDesde =Util.agregarCalendario(panel, 0, 3)
Util.agregarEtiqueta(panel, "Hasta:", 0,4)
cmbHasta =Util.agregarCalendario(panel, 0, 5)
