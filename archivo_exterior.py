from encodings import utf_8


destino = 'cr_files/niveles.txt'

def obtener_lista_niveles(ruta='cr_files/niveles.txt'):
    lista_niveles = []
    lista_aux = []
    with open(ruta, 'r', encoding='utf-8') as f:
        f = f.readlines()
        for renglon in f:
            if '<n>' in renglon:
                renglon = renglon.rstrip('<n>\n')
                renglon = renglon.strip('<n>')
                lista_aux.append(renglon)
            elif '<t>' in renglon:
                renglon = renglon.rstrip('<t>\n')
                renglon = renglon.strip('<t>')
                lista_aux.append(renglon)
                if len(lista_aux) == 3:
                    lista_niveles.append(lista_aux)
                    lista_aux = []
    return lista_niveles        # Devuelve una lista con listas de cada nivel: [[Nombre nivel, primer juego, segundo juego], ['Prendas y Frutas', 'prendas', 'frutas']]
        
def obtener_lista_grupos(ruta='cr_files/niveles.txt'):
    lista_grupos = []
    with open(ruta, 'r', encoding='utf-8') as f:
        f = f.readlines()
        for renglon in f:
            if '<n>' in renglon:
                renglon = renglon.rstrip('<n>\n')
                renglon = renglon.strip('<n>')
                lista_grupos.append(renglon)
    return lista_grupos

def obtener_lista_palabras(titulo, ruta='cr_files/niveles.txt'):
    lista_palabras = []
    with open(ruta, 'r', encoding='utf-8') as f:
        linea = f.readline()
        while linea != f'<t>{titulo.upper()}<t>\n':
            linea = f.readline()
        linea = f.readline()
        while '<fin>' not in linea:
            linea = linea.rstrip('\n')
            linea = linea.split('&&')
            lista_palabras.append(linea)
            linea = f.readline()
    return lista_palabras

def guardar_nuevo_nivel(nombre_nivel, ruta='cr_files/niveles.txt'):
    with open(ruta, 'a', encoding='utf_8') as f:
        texto = f'<n>{nombre_nivel.upper()}<n>\n<t>PRIMERA RONDA<t>\n<fin>\n<t>SEGUNDA RONDA<t>\n<fin>\n\n'
        f.write(texto)

def eliminar_info_nivel(nombre_nivel, ruta='cr_files/niveles.txt'):
    texto_a_eliminar = f'<n>{nombre_nivel.upper()}<n>\n'
    with open(ruta, 'r+', encoding='utf_8') as f:
        lineas = f.readlines()
        f.seek(0)
        borrando = False
        cont_fin = 0
        espacio_extra_borrado = False
        for linea in lineas:
            if texto_a_eliminar not in linea and not borrando:
                f.write(linea)
            elif '<fin>' not in linea:
                if espacio_extra_borrado:
                    borrando = False
                else:
                    borrando = True
            else:
                cont_fin += 1
                if cont_fin >= 2 and not espacio_extra_borrado:
                    espacio_extra_borrado = True
        f.truncate()
    
def guardar_cambios_nivel(nombre_nivel, texto_a_guardar, ruta='cr_files/niveles.txt'):
    with open(ruta, 'r+', encoding='utf_8') as f:
        nombre_nivel = f'<n>{nombre_nivel.upper()}<n>\n'
        f.seek(0)
        lineas = f.readlines()
        f.seek(0)
        borrando = False
        cont_fin = 0
        espacio_extra_borrado = False
        for linea in lineas:
            if nombre_nivel not in linea and not borrando:
                f.write(linea)
            elif '<fin>' not in linea:
                if espacio_extra_borrado:
                    borrando = False
                else:
                    borrando = True
            else:
                cont_fin += 1
                if cont_fin >= 2 and not espacio_extra_borrado:
                    espacio_extra_borrado = True
                    f.write(texto_a_guardar)
        f.truncate()