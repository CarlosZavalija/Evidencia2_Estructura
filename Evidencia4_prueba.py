import datetime #Impirtacion de los modulos correspondientes para trabajar en esta actividad
import os
import sys
import sqlite3 #Libreria para trabajar con SQLite
from sqlite3 import Error

try: #Utililizacion del modelo TRY
    with sqlite3.connect("Automotriz.db") as conn: #Establecemos el nombre de nuestra base de datos
        c = conn.cursor()  #Hacemos la creacion de nuestro cursos que actuara como mensajero con nuestra base de datos
        c.execute("CREATE TABLE IF NOT EXISTS ventasFolio (Folio INTEGER PRIMARY KEY, Fecha TEXT NOT NULL);") #Creamos las tablas correspondientes
        c.execute('''CREATE TABLE IF NOT EXISTS ventasArticulos (Descripcion TEXT NOT NULL, Cantidad INTEGER NOT NULL,
                    Precio INTEGER NOT NULL, Total REAL NOT NULL, Foliov INTEGER NOT NULL,
                    FOREIGN KEY(Foliov) REFERENCES Foliov(Folio));''')
        print("Tabla creada exitosamente")
    while True:

        print("*" * 30)
        print("Bienvendio al menú principal") #CReacion del menu
        print("Por favor eliga la opcion que quiera realizar \n")
        opcion = int(input("1- Registrar una venta | 2- Consultar una venta | 3-Consultar venta por fecha | 4-Salir: \n")) # Línea 12, aquí se preguntan las opciones del menú
        print("*" * 30)

        if opcion == 1: #opcion uno del menu, registro mediante folio
            while True:
                folio = int(input('Por favor ingrese su numero de folio: '))
                with sqlite3.connect("Automotriz.db") as conn:
                    c = conn.cursor()
                    Venta_folio = {"folio": folio}
                    c.execute("SELECT * FROM ventasFolio WHERE Folio = :folio", Venta_folio) #Seleccionamos los datos de la tabla ventasFolio
                    f = c.fetchall()
                    if f:
                        print("Este folio ya esta registrado por favor ingrese uno nuevo")
                    else:
                        break     
            while True:
                captura_fecha= input('Introduzca la fecha en la que se realizo la venta (dd/mm/yyyy): ')
                fecha = datetime.datetime.strptime(captura_fecha, "%d/%m/%Y").date()
                c.execute("INSERT INTO ventasFolio (Folio, Fecha)VALUES(?,?)", (folio, fecha))
                print("Su venta se ha registrado")
                conn.commit()
                Articulointegrado =1
                while Articulointegrado==1:  
                    descripcion_p= input('Por favor introduzca el articulo: ')  #Solicitamos los datos de la venta 
                    producto_p=int(input('Por favor introduzca el precio del articulo deseado: '))
                    venta_cantidad = int(input('Por favor introduzca la cantidad que se llevara: '))
                    total = descripcion_p * venta_cantidad    
                    c.execute('''INSERT INTO ventasArticulos (Descripcion, Cantidad, Precio,
                                Total, Foliov)VALUES(?,?,?,?,?)''', (descripcion_p, venta_cantidad, producto_p, total, folio))
                    print("Su registro ha sido exitoso") #Insertamos los datos en la tabla ventasArticulos
                    conn.commit()                
#              
                    Articulointegrado=int(input('¿Le gustraia agregar mas mercancia a su compra? \n1)-Si \n2)-No: '))
                    
                    sumaTotal = 0
                    if Articulointegrado == 2:
                        Venta_folio = {"folio": folio}
                        sumaTotal = 0
                        c.execute('''SELECT ventasFolio.Folio, ventasFolio.Fecha, ventasArticulos.Descripcion, ventasArticulos.Cantidad, ventasArticulos.Precio, ventasArticulos.Total \
                                 FROM ventasFolio \
                                 INNER JOIN ventasArticulos ON ventasArticulos.Foliov = ventasFolio.Folio WHERE Folio = :folio''',Venta_folio)
                        fec = c.fetchall()
                        if fec:
                            print("Folio\tFecha\t\tDescripcion\tCantidad\t\tPrecio\t\tTotal")
                        for Folio, Fecha, Descripcion, Cantidad, Precio, Total in fec:
                            print(f"{Folio}\t{Fecha}\t{Descripcion}\t\t{Cantidad}\t\t{Precio}\t\t{Total}")
                            sumaTotal+= Total
                        print("*******************")
                        print(f'Subtotal: ${sumaTotal}')
                        iva = sumaTotal * .16
                        iva_total = sumaTotal + iva
                        print(f'Total + IVA: ${iva_total}')
                        
                break
         
#    
        elif opcion == 2:
            folio_busqueda = int(input('Por favor ingrese el folio que desea buscar: ')) #Opcion dos del menu en la que se realiza la busqueda de la venta mediante el folio
            Venta_folio = {"folio": folio_busqueda}
            c.execute('''SELECT ventasFolio.Folio, ventasFolio.Fecha, ventasArticulos.Descripcion, ventasArticulos.Cantidad, ventasArticulos.Precio \
                         FROM ventasFolio \
                         INNER JOIN ventasArticulos ON ventasArticulos.Foliov = ventasFolio.Folio WHERE Folio = :folio''', Venta_folio)
            f = c.fetchall()
            if f:
                print("Folio\tFecha\t\tDescripcion\t\tCantidad\t\tPrecio")
                for Folio, Fecha, Descripcion, Cantidad, Precio in f:
                    print(f"{Folio}\t{Fecha}\t{Descripcion}\t\t\t{Cantidad}\t\t\t{Precio}")
            else:
                print("El folio que desea buscar no se encuenra registrado ingrese uno ya registrado")
                        
    #          
        elif opcion == 3:  #Opcion tres del menu aqui se realiza la busqueda de una venta mediante la fecha
            fecha_i = input('\nIngrese la fecha de la venta que desea buscar: ')
            fecha_busqueda = datetime.datetime.strptime(fecha_i, "%d/%m/%Y").date() #Con la importacion de datetime hacemos la conversion a fecha
            sumaTotal = 0
            fecha_ = {"folio": fecha_busqueda}
            c.execute('''SELECT ventasFolio.Folio, ventasFolio.Fecha, ventasArticulos.Descripcion, ventasArticulos.Cantidad, ventasArticulos.Precio, ventasArticulos.Total \
                         FROM ventasFolio \
                         INNER JOIN ventasArticulos ON ventasArticulos.Foliov = ventasFolio.Folio WHERE Fecha = :folio''', fecha_)
            fec = c.fetchall()
            if fec:
                print("Folio\tFecha\t\tDescripcion\tCantidad\tPrecio\t\tTotal")
                for Folio, Fecha, Descripcion, Cantidad, Precio, Total in fec:
                    print(f"{Folio}\t{Fecha}\t{Descripcion}\t\t{Cantidad}\t\t{Precio}\t\t{Total}")
                    sumaTotal+= Total
                print(f'Ventas {fecha_busqueda}')
                print("*******************")
                print(f'Subtotal: ${sumaTotal}')
                iva = sumaTotal * .16
                totaliva = sumaTotal + iva
                print(f'Total + IVA: ${totaliva}') #Hacemos la suma total ya con el IVA includo
            else:
                print("Fecha ingresada no registrada por favor ingrese una nueva fecha")
    #               
        elif opcion == 4: #opcion que termina con la salida del menu
            print("Base de datos creada exitosamente!! que pase buen dia")
            break  
#
except Error as e:
    print (e)
except Exception:  #Finalizamos el metodo try y except que nos ayudan a atrapar las excepciones 
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    if conn:   
        conn.close()