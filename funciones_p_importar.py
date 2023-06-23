
from colorama import Fore
import re
from unidecode import unidecode
import random
import datetime
import json
import glob

def reemplazar_raza_habilidades_por_lista(lista:list):
    '''
    brief: Reemplaza el valor(str) de las keys "Raza" y "Habilidades"
        por una lista de ser necesario.
        param lista: Lista sobre la cual trabajar.
    '''
    
    reemplazar_por_lista(lista, "Raza", "-")
    reemplazar_por_lista(lista, "Habilidades", "|")

def reemplazar_por_lista(lista:list, key:str, split:str):
    '''
    brief: Verifica si el string valor de una key contiene x caracter.
    De ser así lo utiliza como corte para crear una lista.
    param lista: Lista con la cual trabajar
    param key: key sobre la cual se quiere verificar si
    es necesario convertir en lista
    param split: caracter el cual utilizar como punto de corte
    '''
    for personaje in lista:
        if "Three-Eyed People" not in personaje[key] and "Shin-jin" not in personaje[key]:
            search_return = re.search(split, personaje[key])
            if search_return != None:
                personaje[key] = personaje[key].split(split)

def convertir_a_enteros(lista:list):
    '''
    Brief: Reemplaza los strings que representan datos numericos 
    de una lista de diccionarios por datos numericos.
    Parameter: Lista la cual normalizar.
    '''
    if validacion_simple_lista:
        for diccionario in lista:
            for clave, valor in diccionario.items():
                if valor.isnumeric():
                    diccionario[clave] = int(valor)
                else:
                    try:
                        numero_decimal = float(diccionario[clave])
                        diccionario[clave] = int(numero_decimal)
                    except ValueError:
                        pass
        print("Datos Normalizados")
    else:
        print("Error: Lista vacía o formato incorrecto")

def quitar_espacios_habilidades(lista:list)->list:

    '''
    brief: quita los espacios sueltos a la izquierda y/o derecha
    de todas las habilidades de la lista.
    '''
    
    for pj in lista:
        for habilidad in range(len(pj["Habilidades"])):
            pj["Habilidades"][habilidad] = pj["Habilidades"][habilidad].strip()
    
    return lista

def normalizar_todo(lista:list)->list:

    '''
    aplica a la lista todas las funciones que sirvan para 
    normalizarla
    param list: lista a normatizar
    '''

    if validacion_simple_lista(lista) != True: #VALIDACION
        print("lista no valida")
        return

    convertir_a_enteros(lista)
    reemplazar_raza_habilidades_por_lista(lista)
    quitar_espacios_habilidades(lista)

#VALIDACIONES # VALIDACIONES # VALIDACIONES

def validacion_simple_lista(lista:list)->bool:
    '''
    brief: Valida que la lista sea mayor a 0 y el tipo de dato sea list
    param list: Lista la cual validar
    '''
    if len(lista) > 0 and type(lista) == list:
        return True
    else: return False

def validar_diccionario(dicc)->bool:
    '''
    brief: Valida que el diccionario sea tipo de dato dict
    param dicc: Diccionario el cual validar
    '''
    return isinstance(dicc, dict)

def validar_dicc_key_es_str_list(dicc:dict, key:str):
    '''
    brief: Valida que el diccionario sea tipo dict 
    y la key ingresada tipo str o list
    '''
    return validar_diccionario and isinstance(dicc.get(key), str) or isinstance(dicc.get(key), list)

def validar_string(string:str)->bool:
    '''
    brief: Valida que el string sea tipo str y que no esté vacio.
    '''
    return isinstance(string, str) and len(string) > 0 

def validacion_continuar_while()->str:

    '''
    pregunta si deseas continuar
    return: "si" or "no"
    '''

    respuesta = input("desea continuar? si o no ").lower()
    while respuesta != "si" and respuesta != "no":
        respuesta = input("desea continuar? si o no ").lower()
    
    return respuesta

def validacion_int(num:int, maximo:int)->bool:
    '''
    valida que un numero sea de tipo int, mayor a 0
    y menor al int pasado por parametro
    param num: numero a validar
    maximo: numero maximo que puede tomar el validado.
    '''
    if isinstance(num, int):
        if num > 0 and num <= maximo:
            return True
        else:
            print("Error en el formato. se espera un int")
            return False
    else: 
        print("Error en el formato. se espera un int")
        return False

##########################################################

def crear_lista_por_key(lista:list, key:str)->list:
    '''
    brief: crea una lista con todos los valores 
    de la key ingresada por parametro
    param lista: lista la cual recorrer
    param key: key elegida para crear la lista
    '''
    if validacion_simple_lista(lista) != True:
        return
    if validar_string(key) != True:
        return

    lista_key = set()

    for personaje in lista: 
        if type(personaje[key]) == list:
            for dato in personaje[key]:
                lista_key.add(dato)
        elif type(personaje[key]) == str:
            lista_key.add(personaje[key])
    
    return [dato for dato in lista_key]

def dz_determinar_cantidad_key_por_dicc(lista:list, key:str)->dict:
    '''
    brief: Crea un diccionario, itera la lista y añade al diccionario
    como key los valores de la key brindada por parametro.
    y les asigna como valor un contador. El cual suma cada vez que un
    diccionario de la lista tiene el mismo valor.
    param lista: Lista sobre la cual iterar
    param key: Key con la cual se quiere hacer el diccionario de contador.
    '''
    
    if validacion_simple_lista(lista) != True:
        print("Error. Lista vacia o formato incorrecto")
        return 
    
    dicc_cantidad_atributos = {}

    for diccinario in lista:
        if type(diccinario[key]) == str:
            if diccinario[key] in dicc_cantidad_atributos:
                    dicc_cantidad_atributos[diccinario[key]] += 1
            else:
                    dicc_cantidad_atributos[diccinario[key]] = 1

        elif type(diccinario[key]) == list:
            for valor_key in diccinario[key]:
                if valor_key in dicc_cantidad_atributos:
                        dicc_cantidad_atributos[valor_key] += 1
                else:
                        dicc_cantidad_atributos[valor_key] = 1
    
    return dicc_cantidad_atributos

def crear_lista_diccionario_por_key(lista:list, key:str)->list:
    '''
    brief: crea una lista de diccionarios vacios por cada raza existente 
    dentro de la lista
    param: lista la cual iterar para crear la lista de razas.
    '''
    if not validacion_simple_lista(lista):
        print("no se obtuvo una lista")
        return

    set_lista = set()
    for personaje in lista:
        if validar_dicc_key_es_str_list(personaje, key):
            if isinstance(personaje[key], str):
                set_lista.add(personaje[key])
            else:
                set_lista.update(personaje[key])
        else:
            print("Formato incorrecto")

    return [{dato: {}} for dato in set_lista]

def agrupar_personaje_con_su_poder(personaje:dict)->dict:
    '''
    brief: crea un diccionario con "nombre" como key 
    y "poder de ataque como valor.
    param personaje: diccionario sobre el cual sacar nombre y poder.
    '''
    if validar_diccionario(personaje):
        dict_personaje_poder = {}

        dict_personaje_poder[personaje['Nombre']] = [personaje['Poder de ataque']]

        return dict_personaje_poder

    else: print("no se obtuvo un dicc")

def dz_agrupar_personaje_poder_por_raza(lista:list):
    '''
    brief: Crea una lista de diccionarios raza el cual contiene 
    nombres de personajes con su poder de ataque
    param lista: Lista sobre la cual iterar para tomar los datos
    y devolver la nueva lista.
    '''

    if validacion_simple_lista(lista) != True: #VALIDACION
        print("lista no valida")
        return

    lista_razas_personajes_con_poder = crear_lista_diccionario_por_key(lista, "Raza")
    for personaje in lista:
        personaje_con_poder = agrupar_personaje_con_su_poder(personaje)

        if type(personaje["Raza"]) == str:
            for claves in lista_razas_personajes_con_poder:
                if personaje["Raza"] in claves.keys():
                    claves[personaje["Raza"]].update(personaje_con_poder)
        else:
            for raza in personaje["Raza"]:
                for claves in lista_razas_personajes_con_poder:
                    if raza in claves.keys():
                        claves[raza].update(personaje_con_poder)

    for dato in lista_razas_personajes_con_poder:
                        for dicc, valor in dato.items():
                            print(f"{Fore.LIGHTRED_EX}{dicc}{Fore.RESET}: {valor}")


### PUNTO 4

def crear_lista_todas_habilidades(lista:list)->set:
    '''
    brief: Crea una lista con todas las habilidades que hay
    param lista: Lista la cual recorrer para buscar las habilidades existentes.
    '''
    if validacion_simple_lista(lista) != True:
        print("Formato de lista incorrecto")
        return

    habilidades = set()
    for personaje in lista:
        for habilidad in personaje["Habilidades"]:
            habilidades.add(habilidad.strip())

    habilidades_lista = [habilidad for habilidad in habilidades]
    return habilidades_lista 

def calcular_promedio(suma1:int, suma2:int, dividendo:int):
    '''
    calcula el promedio entre 2 valores.
    param:
    valor1: el primer valor
    valor2: segundo valor
    dividendo: el dividendo de la suma de los 2 valores <-- está al pedo jaja
    '''
    if type(suma1) != int or type(suma2) != int or type(dividendo) != int or dividendo == 0:
        print("Formato incorrecto o division imposible")
        return
    return ((suma1 + suma2) / dividendo)

def crear_string_nombre_raza_promedio(dicc:dict)->str:

    '''
    crea un string con "Nombre", "Raza", y el promedio entre
    "Poder de pelea" y "Poder de ataque"
    param dicc: Diccionario con el cual crear string
    '''

    if validar_diccionario(dicc) != True:
        print("Formato erroneo")
        return
    

    nombre = dicc["Nombre"]
    raza = dicc["Raza"]
    promedio_ataque_pelea = int(calcular_promedio(dicc["Poder de pelea"], dicc["Poder de ataque"], 2))
    
    nombre_raza_promedio = f"{nombre}: {raza} y su promedio de poder es {promedio_ataque_pelea}"
    return nombre_raza_promedio

def crear_lista_habilidades_sin_tilde(lista:list)->list:

    '''
    crea una lista con todas las habilidades sin repetir y sin tildes.
    param lista: lista la cual usar para crear la de habilidades.
    '''

    if validacion_simple_lista(lista) != True:
        print("Formato erroneo")
        return
    
    lista = crear_lista_todas_habilidades(lista)
    lista_sin_tildes = []

    for habilidad in lista:
        habilidad_sin_tilde = quitar_tildes_string(habilidad)
        lista_sin_tildes.append(habilidad_sin_tilde)

    return lista_sin_tildes

def crear_dicc_lista(lista:list)->dict:

    '''
    crea un diccionario donde cada key va a ser el valor de una lista 
    y su valor una lista vacia.
    param lista: lista con la cual crear el diccionario de habilidades
    '''

    if validacion_simple_lista(lista) != True:
        print("Formato erroneo")
        return
    
    dicc_lista_vacia = {dato: [] for dato in lista}
    return dicc_lista_vacia

def crear_dicc_lista_habilidades(lista:list)->list:

    '''
    crea un diccionario donde cada key va a ser una habilidad con su valor como lista vacia.
    param lista: lista con la cual crear el diccionario de habilidades
    '''

    if validacion_simple_lista(lista) != True: #VALIDACION
        print("lista no valida")
        return
    
    lista = crear_lista_habilidades_sin_tilde(lista)
    lista = crear_dicc_lista(lista)

    return lista

def crear_dicc_lista_habilidades_con_pj(lista:list)->dict:

    '''
    crea un diccionario donde cada key va a ser el valor de una lista 
    y su valor va a ser un string que tenga el nombre, la raza y el 
    promedio entre poder de ataque y pelea de un personaje.
    param lista: lista con la cual crear el diccionario de habilidades
    '''

    if validacion_simple_lista(lista) != True: #VALIDACION
        print("lista no valida")
        return

    diccionario_lista = crear_lista_habilidades_sin_tilde(lista)
    diccionario_lista = crear_dicc_lista(diccionario_lista)
    lista_personajes = lista
    
    
    for pj in lista_personajes:
        nombre_raza_promedio = crear_string_nombre_raza_promedio(pj)
        for habilidad in pj["Habilidades"]:
                for key in diccionario_lista:
                    if quitar_tildes_string(habilidad) == key:
                        diccionario_lista[key] = nombre_raza_promedio
    return diccionario_lista

def quitar_tildes_string(texto:str)->str:

    '''
    brief: toma un string y lo devuelve sin tildes
    '''

    if validar_string(texto) != True:
        print("String no valido")
        return

    tildes = ['á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú']

    for i in range(len(tildes)):
        texto = texto.replace(tildes[i], unidecode(tildes[i]))
    
    return texto

def crear_lista_mayuscula(lista:list)->list:

    '''
    brief: copia una lista y la devuelve en mayuscula
    param lista: lista para copiar
    '''

    if validacion_simple_lista(lista) != True: #VALIDACION
        print("lista no valida")
        return

    lista_mayuscula = []
    for dato in lista:
        if type(dato) == str:
            lista_mayuscula.append(dato.upper())
    return lista_mayuscula

def crear_lista_habilidades_mayus_sin_tildes(lista:list)->list:
    '''
    brief: crea una lista de todas las habilidades que hay pero formateadas
    a mayuscula y sin tildes
    param lista: lista de la cual sacar las habilidades
    '''
    if validacion_simple_lista(lista) != True: #VALIDACION
        print("lista no valida")
        return

    lista = crear_lista_todas_habilidades(lista)
    lista = quitar_tildes_lista(lista)
    lista = crear_lista_mayuscula(lista)
    lista = crear_dicc_lista(lista)

    return lista

def quitar_tildes_lista(lista:list)->list:

    '''
    brief: quita las tildes de las palabras de una lista
    param lista: lista la cual formatear
    '''

    if validacion_simple_lista(lista) != True: #VALIDACION
        print("lista no valida")
        return

    lista_nueva = []

    for dato in lista:
        if validar_string(dato) != True:
            print("String no valido")
        dato_no_tilde = quitar_tildes_string(dato)
        lista_nueva.append(dato_no_tilde)
    return lista_nueva

def preparar_comparacion_string(string:str)->str:
    '''
    brief: toma un string por parametro,
    lo devuelve en mayuscula y sin tildes
    param string: string que formatear
    '''
    if validar_string(string) != True:
        print("Datos erroneos")
        return
    
    string = quitar_tildes_string(string)
    string = string.upper()

    return string

def dz_listar_personajes_por_habilidad(lista:list):
    
    '''
    Muestra los personajes que tienen una habilidad específica ingresada por el usuario.

    Args:
        - lista: una lista de diccionarios, cada diccionario representa un personaje con sus habilidades.
    '''
        
    if validacion_simple_lista(lista) != True: #VALIDACION
        print("lista no valida")
        return

    lista_habilidades =  crear_lista_todas_habilidades(lista)
    lista_p_comparar = crear_lista_habilidades_mayus_sin_tildes(lista)
    lista_habilidad_por_personaje = crear_dicc_lista_habilidades_con_pj(lista)

    while True:

        print(f"{Fore.RED}HABILIDADES:{Fore.RESET}\n{lista_habilidades}")
        habilidad_ingresada = input("Ingrese una habilidad ").upper()
        while habilidad_ingresada not in lista_p_comparar:
            habilidad_ingresada = input("Error. Ingrese una habilidad valida ").upper()

        for key, valor in lista_habilidad_por_personaje.items():
            if habilidad_ingresada == key.upper():
                print(f"{key}, {valor}")

        respuesta = validacion_continuar_while()
        if respuesta == "no":
            break

##############PUNTO 5#############

def calcular_maximo(valor1:int, valor2:int)->int:

    '''
    Calcula el valor máximo entre dos valores enteros.

    Args:
    valor1 (int): El primer valor entero a comparar.
    valor2 (int): El segundo valor entero a comparar.
    '''

    if validacion_int(valor1, valor1) != True or validacion_int(valor2, valor2) != True:
        return

    if valor1 > valor2:
        return valor1
    else: return valor2

def imprimir_pjs_con_id_devolver_ult_iteracion(lista:list)->int:

    """
    Imprime los personajes de una lista junto con su identificador y devuelve la última iteración del bucle.

    Parameters:
    lista (list): Una lista de diccionarios que contienen información de los personajes.

    Returns:
    int: El número total de personajes en la lista.
    """

    if validacion_simple_lista(lista) != True: #VALIDACION
        return

    for i in range(len(lista)):
        print(f"{i+1} = {lista[i]['Nombre']}")
        ultima_it = i+1
    return ultima_it

def seleccionar_pj(ultima_it:int)->int:
    '''
    La función seleccionar_pj permite al usuario seleccionar un personaje de una lista y devuelve su índice en la lista.
    Argumentos:
    ultima_it: entero que representa la última iteración posible para seleccionar un personaje (corresponde al número total de personajes disponibles en la lista).
    Retorno:
    personaje_seleccionado: entero que representa el índice del personaje seleccionado en la lista.
    '''

    if validacion_int(ultima_it, ultima_it) != True:
        return

    personaje_seleccionado = input(f"{Fore.RED}SELECCIONE UN PERSONAJE CON SU NUMERO: {Fore.RESET}")
    try:
        personaje_seleccionado = int(personaje_seleccionado)
    except ValueError:
        pass
    while validacion_int(personaje_seleccionado, ultima_it) != True:
        personaje_seleccionado = input(f"{Fore.RED}ERROR. SELECCIONE UN PERSONAJE CON SU NUMERO: {Fore.RESET}")
        try:
            personaje_seleccionado = int(personaje_seleccionado)
        except ValueError:
            pass
    
    personaje_seleccionado = personaje_seleccionado - 1
    return personaje_seleccionado

def devolver_nombre_poder_ataque_por_pj_index(lista:list, personaje:int)->tuple[str, int]:

    '''
    Función que devuelve el nombre y poder de ataque de un personaje dada su posición
    en una lista.

    Args:
    - lista (list): Lista de personajes con su información.
    - personaje (int): Índice del personaje que se va a comparar.

    Returns:
    - Una tupla con el nombre y poder de ataque del personaje seleccionado.
    '''

    ## SE PUEDE GENERALIZAR PONIENDO LAS KEYS POR PARAMETROS

    if validacion_int(personaje,5000000000) != True or validacion_simple_lista(lista) != True:
        return

    for i in range(len(lista)):
        if personaje == i:
            personaje_seleccionado = lista[i]["Nombre"]
            personaje_seleccionado_poder = lista[i]["Poder de ataque"]

    return personaje_seleccionado, personaje_seleccionado_poder

def dz_jugar_batalla(lista:list)->None:

    '''
    Función que simula una batalla entre dos personajes elegidos al azar de una lista dada.
    El usuario elige su personaje y el programa selecciona el personaje contrario al azar.
    Luego se calcula el poder máximo entre ambos personajes y se determina el ganador.
    Finalmente se guarda el resultado en un archivo de texto.

    Args:
    - lista (list): Una lista de personajes con su información.

    Returns:
    - Una lista con los datos de la batalla, incluyendo la fecha y los nombres del ganador y perdedor.
    '''

    if validacion_simple_lista(lista) != True:
        return 

    ultima_it = imprimir_pjs_con_id_devolver_ult_iteracion(lista)

    personaje_seleccionado = seleccionar_pj(ultima_it)
    personaje_aleatorio = random.randint(1, ultima_it)

    personaje_seleccionado , personaje_seleccionado_poder = devolver_nombre_poder_ataque_por_pj_index(lista, personaje_seleccionado)
    personaje_aleatorio, personaje_aleatorio_poder = devolver_nombre_poder_ataque_por_pj_index(lista, personaje_aleatorio)

    poder_maximo = calcular_maximo(personaje_seleccionado_poder, personaje_aleatorio_poder)

    if poder_maximo == personaje_seleccionado_poder:
        print(f"El ganador es el usuario con; {personaje_seleccionado} con un poder de {personaje_seleccionado_poder}")
        ganador = personaje_seleccionado
        perdedor = personaje_aleatorio
    elif poder_maximo == personaje_aleatorio_poder:
        print(f"El ganador es la maquina con; {personaje_aleatorio} con un poder de {personaje_aleatorio_poder}")
        ganador = personaje_aleatorio
        perdedor = personaje_seleccionado
    else:
        print(f"{Fore.RED}HUBO UN EMPATEE!!!!!{Fore.RESET}")
        ganador = "No hubo"
        perdedor = "hubo empate"

    fecha = datetime.date.today().strftime("%d/%m/%Y")

    with open("./batallas.txt", "a") as f:
        f.write(f"{fecha}, Ganador: {ganador}, perdedor: {perdedor}\n")

####################### PUNTO 6 ##############

def formatear_lista(lista:list)->list:
    '''
    brief: quita las tildes y pone en mayuscula 
    todos los valores de una lista
    param lista: lista que formatear
    '''

    if validacion_simple_lista(lista) != True:
        print("no paso")
        return
    
    lista = crear_lista_mayuscula(lista)
    lista = quitar_tildes_lista(lista)

    return lista

def input_elija_una_validado_in_list(str_a_elegir:str, lista_validacion:list)->list:
    '''
    Pide al usuario que elija una opción de una lista validada y devuelve la elección.
    Si la elección no está en la lista de validación, se seguirá pidiendo hasta que se ingrese una opción válida.

    Args:
    - str_a_elegir (str): La descripción de la opción que el usuario debe elegir.
    - lista_validacion (list): Una lista con las opciones válidas.
    '''
    if validar_string(str_a_elegir) != True or validacion_simple_lista(lista_validacion) != True:
        return

    eleccion = input(f"{Fore.MAGENTA}Elija una {str_a_elegir} {Fore.RESET}")
    while preparar_comparacion_string(eleccion) not in lista_validacion:
        eleccion = input(f"{Fore.MAGENTA}ERRRRRROOOR. Elija una {str_a_elegir}: {Fore.RESET}")

    return eleccion

def imprimir_keys_y_preguntar_por_una(lista:list, key:str, str_pregunta:str, str_titulo_imp_lista:str )->str:

    '''
    brief: crea una lista de los valores de una key
    por la lista recibida por parametro, la imprime 
    y pregunta por una.
    param lista: lista la cual recorrer para obtener la nueva lista.
    key: key a elegir para hacer una lista con sus valores
    str_pregunta: string que va a ir en la pregunta del input
    str_titulo_imp_lista: string que va a encabezar la lista que se imprima.
    '''
    if (validacion_simple_lista(lista) != True 
        or validar_string(key) != True 
        or validar_string(str_pregunta) != True
        or validar_string(str_titulo_imp_lista) != True):
        return

    lista_key = crear_lista_por_key(lista, key)
    lista_key_formateada = formatear_lista(lista_key)
    print(f"{Fore.GREEN}{str_titulo_imp_lista}:{Fore.RESET} \n{lista_key}")

    eleccion = input_elija_una_validado_in_list(str_pregunta, lista_key_formateada)

    return eleccion

def listar_key_lista(dicc:dict, key:str)->list:
    '''
        Crea y devuelve una lista con los valores asociados a la clave "key" en el diccionario "dicc".
        
        Parámetros:
        - dicc (dict): El diccionario del cual obtener los valores.
        - key (str): La clave cuyos valores deben ser obtenidos.
    '''

    if validar_diccionario(dicc) != True or validar_string(key) != True:
        return

    lista_valores_key = []

    if validacion_simple_lista(dicc[key]):
        for valor in dicc[key]:
            lista_valores_key.append(preparar_comparacion_string(valor))
    else: lista_valores_key.append(preparar_comparacion_string(dicc[key]))

    return lista_valores_key

def dz_ingresar_raza_habilidad_guardar_json(lista:list)->None:
    '''
    El usuario ingresa una raza y una habilidad. Se le imprimen por consola
    los personajes que cumplan esas dos condiciones.
    Se crea un Json con los datos de quien cumplio la condicion.
    param lista: lista con la cual trabajar
    '''

    if validacion_simple_lista(lista) != True:
        return  #VALIDACION

    raza_elegida = imprimir_keys_y_preguntar_por_una(lista, "Raza", "Raza", "RAZAS")
    habilidad_elegida = imprimir_keys_y_preguntar_por_una(lista, "Habilidades", "Habilidad", "HABILIDADES")

    #### PONGO LA CADENA EN MAYUSCULA Y LE SACO LOS TILDES ####
    habilidad_elegida_formateada = preparar_comparacion_string(habilidad_elegida)
    raza_elegida_formateada = preparar_comparacion_string(raza_elegida)

    personajes_p_json = []

    for personaje in lista:
        
        raza_pj = listar_key_lista(personaje, "Raza")
        habilidades_pj = listar_key_lista(personaje, "Habilidades")
        if (habilidad_elegida_formateada in habilidades_pj 
        and raza_elegida_formateada in raza_pj):
            
            print(f"{Fore.RED}{personaje['Nombre']}{Fore.RESET} cumple las condiciones.")
            
            personajes_p_json.append( {
                "Nombre": personaje["Nombre"],
                "Poder de ataque": personaje["Poder de ataque"],
                "Habilidades no buscadas": 
                ([habilidad for habilidad in personaje["Habilidades"] 
                if preparar_comparacion_string(habilidad) != habilidad_elegida_formateada])
            })

    nombre_archivo = raza_elegida.replace(" ", "_") + "_" + habilidad_elegida.replace(" ", "_") + ".json"
    if len(personajes_p_json) == 0:
        personajes_p_json.append("nada")
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(personajes_p_json, archivo, indent = 4 , ensure_ascii=False)

########################### PUNTO 7 ###############################

def leer_json_s():
    '''
    busca todos los archivos .json en el directorio.
    guarda las direcciones en una lista.
    recorre la lista e imprime por consola la data que tiene adentro.
    '''
    # busca todos los archivos .json en el directorio
    json_files = glob.glob('*.json')

    if len(json_files) > 0: 
        for file in json_files:
            with open(file, encoding='utf-8') as f:
                data = json.load(f)
                print (f"{Fore.BLUE}{file}{Fore.RESET}")
                for dicc in data:
                    print (f"{dicc}")
    else: 
        print("no hay ningun archivo json")

################### PUNTO 10 ########### ORDENAMIENTO

def dz_ordenar_lista_diccionarios_por_key(lista:list):
    '''
    El usuario ingresa un atributo y un orden, se ordena la lista en base
    al orden elegido.  
    param lista: lista la cual ordenar sus diccionarios.
    '''

    key = preguntar_por_atributo_existente(lista)  
    
    orden = input("ingrese un orden, ascendente o descendente ").lower()
    while orden != "ascendente" and orden != "descendente" :
        orden = input("ERROR. ingrese un orden valido, ascendente o descendente ").lower()

    if orden == "ascendente":
        orden = True
    elif orden == "descendente" :
        orden = False

    ordenar_lista_diccionarios_por_key(lista, orden, key)

def preguntar_por_atributo_existente(lista:list)->str:
    '''
    El usuario ingresa un atributo y se valida que esté en la lista 
    '''

    lista_keys = crear_lista_keys(lista)

    for atributo in lista_keys: 
        print(f"{Fore.RED}{atributo}{Fore.RESET}")

    key = input("ingrese un atributo por el cual ordenar la lista ")
    while key not in lista_keys:
        key = input("ERROR. ingrese un atributo valido por el cual ordenar la lista ")

    return key

def ordenar_lista_diccionarios_por_key(lista:list, orden:bool, key:str):

    '''
    ordena la lista por la clave "key".
    param lista: lista a ordenar
    key: clave por la cual ordenar
    orden: True; ordenar de forma ascendente, False; ordenar de forma descendente.
    '''  

    n = len(lista)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if comparar_diccionarios(lista[j], lista[j + 1], key, orden) > 0:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

def comparar_diccionarios(diccionario1:dict, diccionario2:dict, key:str, orden:bool)->int:
    '''
    Compara dos diccionarios.
    param diccionario1: diccionario a comparar
    param diccionario2: diccionario a comparar
    key: clave por la cual comparar
    '''


    if orden == True:
        valor1 = diccionario1[key]
        valor2 = diccionario2[key]
    else:
        valor1 = diccionario2[key]
        valor2 = diccionario1[key]

    if type(valor1) == list: 
        valor1 = valor1[0]
    if type(valor2) == list: 
        valor2 = valor2[0]

    if valor1 < valor2:
        return -1
    elif valor1 == valor2:
        return 0
    else:
        return 1

def crear_lista_keys(lista:list)->list:
    '''
    se crea una lista con los atributos de los personajes
    param lista: lista de diccionarios de la cual sacar los atributos
    '''

    lista_keys = []

    for pj in lista:
        for atributo in pj:
            lista_keys.append(atributo)
        break

    return lista_keys

############################ PUNTO 11 #################################

def obtener_inicial_nombre(personaje:dict)->str:

    '''
    Obtiene la primer letra de la key "Nombre" de un diccionario
    '''

    if validar_diccionario(personaje) == False:
        return None

    nombre = personaje["Nombre"]
    for c in nombre:
        nombre = c
        break
    
    return nombre

def obtener_ganador_ataque_defensa(personaje:dict):

    '''
    Obtiene el mayor poder entre ataque y defensa.
    Ademas un string con su valor
    '''

    if validar_diccionario(personaje) == False:
        return None

    if personaje["Poder de ataque"] > personaje["Poder de pelea"]:
        return "A", personaje["Poder de ataque"]
    elif personaje["Poder de ataque"] < personaje["Poder de pelea"]:
        return "D", personaje["Poder de pelea"]
    else:
        return "AD", personaje["Poder de pelea"]
    
def obtener_id(personaje:dict)->int:
    '''
    Obtiene el valor de la key ID de un diccionario
    param personaje: diccionario a obtener el ID
    '''

    if validar_diccionario(personaje) == False:
        return None
    
    id = personaje["ID"]
    return id

def generar_codigo_personaje(personaje:dict)->str:

    '''
    Genera un codigo personaje a partir de la inicial del nombre, id y poder de ataque y/o defensa(pelea)
    param personaje: diccionario personaje con el cual generar el codigo 
    '''

    if validar_diccionario(personaje) == False:
        return None
    
    inicial = obtener_inicial_nombre(personaje)
    ganador, poder = obtener_ganador_ataque_defensa(personaje)
    poder = str(poder)
    id = str(obtener_id(personaje))
    separador = "-"

    cantidad_ceros = 18 - (len(inicial) + len (ganador) + len(poder) + 3)

    id = id.zfill(cantidad_ceros) 

    codigo = separador.join([inicial, ganador, poder, id])

    return codigo

def dz_agregar_codigo_personaje(lista:list):

    '''
    se genera un codigo de personae con la inicial del nombre, el mayor tipo de poder,
    y el id
    param lista: lista la cual iterar para agregar el codigo de personaje a los distintos personajes
    '''

    if not validacion_simple_lista(lista):
        return 
    
    for personaje in lista:
        personaje["Codigo"] = generar_codigo_personaje(personaje)

######################## REQUERIMIENTOS EXTRA ##############

def añadir_multiplicador_a_key(dicc:dict, key:str, multiplicador: float):
    '''
    multiplica el valor de la key ingresada por el valor del multiplicador
    y lo asigna a la key recibida por parametro.
    param: dicc: diccionario al cual se le quiere multiplicar el valor de una key
    key: key que se quiere multiplicar el valor
    multiplicador: numero por el cual se quiere multiplicar la key.

    
    '''
    if validar_string(key) != True or validar_diccionario(dicc) != True or isinstance(multiplicador, float) != True:
        return

    dicc[key] = int(dicc[key] * multiplicador)

def añadir_habilidad_a_dicc(dicc:dict, habilidad:str):
    '''
    añade una habilidad pasada por parametro a un diccionario en la key "Habilidades"
    dicc: diccionario en el cual añadir la habilidad
    habilidad: habilidad la cual se va a añadir
    '''
    dicc["Habilidades"].append(habilidad)

def añadir_transformacion_nivel_dios(lista:list):
    '''
    añade la habilidad transformacion nivel dios a los diccionarios
    que posean la raza saiyan y multiplica los stats de "poder de ataque" y "poder de pelea"
    param lista: lista de diccionarios la cual se quiere recorrer para añadir la habilidad
    '''
    if validacion_simple_lista(lista) != True:
        return

    for personaje in lista:
        if "Saiyan" in personaje["Raza"] and "transformación nivel dios" not in personaje["Habilidades"]:
            añadir_multiplicador_a_key(personaje, "Poder de pelea", 1.5)
            añadir_multiplicador_a_key(personaje, "Poder de ataque", 1.7)
            añadir_habilidad_a_dicc(personaje, "transformación nivel dios" )

def normalizar_para_csv(key:str, lista:list)->str:
    '''
    tranforma una lista en un string con un separador por elementos de la lista
    param key: se utiliza para seleccionar que separador se va a utilizar.
    lista: lista la cual recorrer para convertirla en string
    '''
    if validacion_simple_lista(lista) != True or validar_string(key) != True:
        return
    
    if key == "Habilidades":
        separador = "|"
    elif key == "Raza":
        separador = "-"
    else: return

    bandera = 0
    for dato in lista:
        if bandera == 0:
            dato_guardado = dato
            bandera = 1
        else:
            dato_guardado = separador.join([dato_guardado,dato])
    
    return dato_guardado

def normalizar_todo_para_csv(lista:list)->list:
    '''
    normaliza las keys "Habilidades" y "Raza" para que queden como string
    lista: lista la cual se quiere normalizar
    '''
    if validacion_simple_lista(lista) != True:
        return
    
    for dicc in lista:
            if type(dicc["Raza"]) == list:
                dicc["Raza"] = normalizar_para_csv("Raza", dicc["Raza"])
            if type(dicc["Habilidades"]) == list:
                dicc["Habilidades"] = normalizar_para_csv("Habilidades", dicc["Habilidades"])

    return lista

def actualizacion_csv(lista):
    '''
    Crea un archivo csv con los personajes que tengan la raza "Saiyan"
    param lista: lista la cual se va a normalizar y utilizar para escribir el archivo csv
    creado.
    '''
    if validacion_simple_lista(lista) != True:
        return

    lista_dicc_transformacion_agregados = ([personaje for personaje in lista if "Saiyan" in personaje["Raza"]])
    lista_dicc_transformacion_agregados = normalizar_todo_para_csv(lista_dicc_transformacion_agregados)

    with open('actualizados.csv', mode='w', encoding= "utf-8") as file:
        for dicc in lista_dicc_transformacion_agregados:
            file.write(f'''{dicc["ID"]},{dicc["Nombre"]},{dicc["Raza"]},{dicc["Poder de pelea"]},{dicc["Poder de ataque"]},{dicc["Habilidades"]}\n''')
            
    # {dicc["ID"]},       Me HACE SALTOS DE LINEA Q NO QUIERO
    #             {dicc["Nombre"]},
    #             {dicc["Raza"]},
    #             {dicc["Poder de pelea"]},
    #             {dicc["Poder de ataque"]},
    #             {dicc["Habilidades"]},

########################## Menuu #######################

def mostrar_menu():
    '''
    Brief: imprime por consola el menu con sus opciones.
    '''

    menu = [  "1 - Traer datos desde el archivo"
            , "2 - Listar cantidad por raza" 
            , "3 - Listar personajes por raza"
            , "4 - Listar personajes por ingreso de habilidad" 
            , "5 - Jugar batalla" 
            , "6 - Ingresa una raza y una habilidad. Guardar json" 
            , "7 - Leer Json"
            , "8 - Añadir transformacion nivel dios a los saiyan"
            , "9 - Actualizacion csv"
            , "10 - Ordenar lista"
            , "11 - Agregar codigos a personajes"
            , "12 - Printear lista"
            , "13 - Salir"]

    for opcion in menu:
        print(f"{Fore.LIGHTCYAN_EX}{opcion}{Fore.RESET}")

def dz_menu():
    '''
    Brief: imprime por consola el menu con sus opciones y pregunta cual elegir. Valida esa respuesta y la devuelve como int
    '''

    print(f"\n{Fore.LIGHTGREEN_EX}ELIJA LA OPCION QUE DESEE{Fore.RESET}")
    mostrar_menu()
    respuesta = input()
    if respuesta.isnumeric():
        return int(respuesta)
    else:
        while respuesta.isnumeric() == False or int(respuesta) > 13:
            respuesta = input("Por favor ingrese un numero valido")
        return int(respuesta)








