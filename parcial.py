# Debes realizar un menú que permita al usuario trabajar con las siguientes opciones:

# 6.
# 8. Salir del programa.

from colorama import Fore, Style
import re
from funciones_p_importar import *
from os import system


archivo_csv = "DBZ.csv"

def parser_csv(path:str) -> list:
    lista = []

    archivo = open(path, 'r', encoding='utf-8')
    for personaje in archivo:
        lectura = re.split(",", personaje)
        personaje = {}
        personaje['ID'] = lectura[0].strip()
        personaje['Nombre'] = lectura[1].strip()
        personaje['Raza'] = lectura[2].strip()
        personaje['Poder de pelea'] = lectura[3].strip()
        personaje['Poder de ataque'] = lectura[4].strip()
        personaje['Habilidades'] = lectura[5].strip()
        personaje['Habilidades'] = personaje['Habilidades'].replace("$%", "")
        lista.append(personaje)
    archivo.close()
    
    return lista

def dz_main():
    '''
    corre la app
    '''

    bandera_lista = False

    while True:

        respuesta = dz_menu()

        system("cls")
        if not bandera_lista:
            match respuesta:
                case 1:
                    lista_datos = parser_csv(archivo_csv)
                    print("Datos obtenidos")
                    normalizar_todo(lista_datos)
                    bandera_lista = True
                case _:
                    if bandera_lista:
                        pass
                    else:
                        print("NO HAY LISTA CON LA CUAL TRABAJAR, SELECCIONE LA OPCION 1 POR FAVOR")
            
        if bandera_lista:         
            match respuesta:
                case 2:
                    print(f"{Fore.RED}\t\t\t\t\tCantidad por raza:{Style.RESET_ALL}")
                    cantidad_por_raza = dz_determinar_cantidad_key_por_dicc(lista_datos, "Raza")
                    for dato, valor in cantidad_por_raza.items():
                        print(f"Hay {valor} {Fore.LIGHTYELLOW_EX}{dato}{Fore.RESET}")
                case 3:
                    print(f"{Fore.RED}\t\t\t\t\tListar personajes por raza:{Style.RESET_ALL}")
                    dz_agrupar_personaje_poder_por_raza(lista_datos)
                    
                case 4:
                    print(f"{Fore.RED}\t\t\t\t\tListar personajes por ingreso de habilidad:{Style.RESET_ALL}")
                    dz_listar_personajes_por_habilidad(lista_datos)
                case 5:
                    print(f"{Fore.RED}\t\t\t\t\tBATALLAAAAAAAAAAA:{Style.RESET_ALL}")
                    dz_jugar_batalla(lista_datos)
                case 6:
                    print(f"{Fore.RED}\t\t\t\t\tIngresa una raza y una habilidad. Guardar json:{Style.RESET_ALL}")
                    dz_ingresar_raza_habilidad_guardar_json(lista_datos)
                case 7:
                    leer_json_s()
                case 8:
                    print(f"{Fore.RED}\t\t\t\t\tYa se añadio la transformacion nivel dios a los saiyan :p{Style.RESET_ALL}")
                    añadir_transformacion_nivel_dios(lista_datos)
                case 9:
                    actualizacion_csv(lista_datos)
                case 10: 
                    dz_ordenar_lista_diccionarios_por_key(lista_datos)
                case 11:
                    dz_agregar_codigo_personaje(lista_datos)
                    print ("hecho")
                case 12: 
                    print(f"{Fore.GREEN}\t\t\t\t LISTA DE PERSONAJES {Style.RESET_ALL}")
                    
                    for pj in lista_datos:
                        print(f"{pj}\n")
                case 13:
                    break 


dz_main() ############ APP