#Línea 1, hacemos la importacion de los modulos para trabajar con CSV
import csv
import os
import sys        

from collections import namedtuple # Linea 2, aquí hacemos la importacion del modulo collecctions para trabjar con Tuplas

ventas = namedtuple("ventas", "fecha consulta_folio decripcionProducto cantidadPiezas precioVenta subtotal iva total") # Línea 4, definimos los valores de las variables que se encuentran en nuesta Tupla

ventasDiccionario = {} # Línea 6, aquí abrimos un diccionario vacio 

while True:
    print("*" * 30)
    print("Bienvendio al menú principal")
    print("Por favor eliga la opcion que quiera realizar \n")
    opcion = int(input("1- Registrar una venta | 2- Consultar una venta | 3- Salir: \n")) # Línea 12, aquí se preguntan las opciones del menú
    print("*" * 30)
    if opcion == 1: #Líenea 14, creamos una condicional para nuestra primera variable
        while True: #Línea 15, abrimos un ciclo para la opción
            fecha = input("Ingrese la fecha de la venta DD/MM/AA: \n") #línea 16, se pide la fecha que se desea buscar
            if fecha in ventasDiccionario.keys(): # Líena 17, Creamos una condicional para buscar la fecha en el diccionario
                print("Esa fecha ya esta registrado, ingrese uno nuevo por favor") # Línea 18, informamos que ya existe 
            else:
                consulta_folio = input("Ingrese su numero de folio por favor\n")
                decripcionProducto = input("Por favor ingrese la descrpcion de todos sus producto: \n")
                cantidadPiezas = int(input("Por favor ingrese la cantidad total de piezas: \n"))
                precioVenta =int(input("Por favor ingrese el precio total de la venta: ")) #Línea 20 a 23, pedimos los datos faltantes para el registro
                print(f"Su fecha de venta es : {fecha} \n su numero de folio es : {consulta_folio}\n la descripcion es : {decripcionProducto}\n la cantidad de peizas es : {cantidadPiezas}\n el precio de venta es : {precioVenta}") #Línea 24, le mostramos los registros de los datos de la venta
                subtotal = (cantidadPiezas * precioVenta) #Línea 25, fórmula para sacar el subtotal
                iva = (0.16 * subtotal) #Línea 26, fórmula para sacar el iva 
                total = (subtotal + iva) #Línea 27, procedimiento para sacar el total
                print(f"SUBTOTAL: {subtotal}")
                print(f"IVA: {iva}")
                print(f"TOTAL: {total}") #Líena 28 a 30, mostramos el subtotal, el iva y el total
                break

       
        
        nuevaVenta = ventas(fecha, consulta_folio, decripcionProducto, cantidadPiezas, precioVenta, subtotal, iva, total) #Línea 35, guardamos dentro de una Tupla las varibales del registro de venta

        ventasDiccionario[fecha] = nuevaVenta #Línea 37 hacemos que la Tupla sea almacendad en un diccionario
        
    elif opcion == 2: # Linea 39, se abre una condicional para la opción numero 2
        consultarVenta= input("Ingrese la fecha de venta que desea buscar: ") #Linea 40, se solicitala fecha que se desea buscar 
        for ventas in ventasDiccionario.keys(): #Linea 41, Creamos un for que recorre las llaves o claves del diccionario donde almacenamos las ventas 
            if consultarVenta in ventasDiccionario.keys(): #Linea 42, verificamos que exista la fecha que queremos dentro de la lista 
                print(f"Datos de la venta:\n Fecha de la venta: {ventasDiccionario[consultarVenta].fecha}\n Numero de folio: {ventasDiccionario[consultarVenta].consulta_folio}\n Descripcion del producto o productos: {ventasDiccionario[consultarVenta].decripcionProducto}\n Total de cantidad de piezas: {ventasDiccionario[consultarVenta].cantidadPiezas}\n Precio total de venta: {ventasDiccionario[consultarVenta].precioVenta}\n Subtotal:{ventasDiccionario[consultarVenta].subtotal}\n Iva:{ventasDiccionario[consultarVenta].iva}\n Total:{ventasDiccionario[consultarVenta].total} ")#Linea 43. desplegamos el registro encontrado en ventasDiccionario usando como id la varaible de venta consultada
                break

            else: #Linea 46, creamos un else por si no existe la fecha solicitado dentro del diccionario
                print("Fecha de venta no registrada, por favor ingrese una fecha que ya este registrada.") #Linea 47, avisamos al usuario que su fecha no esta registrado
    elif opcion == 3:
        print("Su compra se realizao de manera exitosa")
        with open("ventasRecibo.csv","w", newline="") as archivo:  #Línea 54, abrimos el CSV en modo de escritura con el nombre de "ventasRecibo"
            guardado = csv.writer(archivo)
            guardado.writerow(("Fecha", "Folio", "Descripcion", "Cantidad de productos", "Precio de venta", "subtotal", "Iva", "Total")) #Línea 56, introducimos los encabezados que contendra nuestro CSV
            guardado.writerows([(fecha, datos.consulta_folio, datos.decripcionProducto, datos.cantidadPiezas, datos.precioVenta, datos.subtotal, datos.iva, datos.total) for fecha, datos in ventasDiccionario.items()]) #Línea 57, introducimos los valores a nuestro CSV       
        print(f"\nCSV guardado correctamente {os.getcwd()}")
        break #Línea 59 terminamos con el proceso