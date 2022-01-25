def escribir(texto, posicion):
    with open('cr_files/prueba.txt', 'a+', encoding = 'utf-8') as f:
        f.seek(posicion)
        f.readline()
        f.write(f'La última linea es: {texto}\n')


escribir('CERDINHO', 20)