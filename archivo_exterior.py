destino = 'cr_files/niveles.txt'

def obtener_lista_niveles(ruta):
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
        
def obtener_lista_grupos(ruta):
    lista_grupos = []
    with open(ruta, 'r', encoding='utf-8') as f:
        f = f.readlines()
        for renglon in f:
            if '<n>' in renglon:
                renglon = renglon.rstrip('<n>\n')
                renglon = renglon.strip('<n>')
                lista_grupos.append(renglon)
    return lista_grupos

def obtener_lista_palabras(ruta, titulo):
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

def guardar_informacion(texto):
    pass