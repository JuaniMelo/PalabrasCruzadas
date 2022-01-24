import random
from kivy.app import App
from color_label import ColorLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class Columnas(BoxLayout):
    def __init__(self, lista, **kwargs):
        super().__init__(**kwargs)
        self.color_label = (1, .5, 0, 1)
        self.padding = [50, 0, 50, 0]
        self.lista_palabras = lista
        self.lblPP = []
        self.lblSP = []
        self.crear_listas()
        self.init_layout()

    def init_layout(self):                              #Dibuja las listas y el temporizador
    #BOX PP
        self.boxPP = BoxLayout(orientation='vertical',size_hint=(.8, 1), spacing=10, padding=10)
        for i in range(len(self.lista_palabras)):
            self.lblPP.append(ColorLabel(text=self.lista_mezclada_PP[i], color=self.color_label, font_size = 20, font_name = 'fonts/bebas_neue.ttf'))
            self.boxPP.add_widget(self.lblPP[i])
        self.add_widget(self.boxPP)
    #TEMPORIZADOR
        self.temp = Label(font_size='50dp', font_name='fonts/Lcd.ttf', halign='center')
        self.add_widget(self.temp)
    #BOX SP
        self.boxSP = BoxLayout(orientation='vertical',size_hint=(.8, 1), spacing=10, padding=10)
        for i in range(len(self.lista_palabras)):
            self.lblSP.append(ColorLabel(text=self.lista_mezclada_SP[i], color=self.color_label, font_size = '20dp', font_name = 'fonts/bebas_neue.ttf'))
            self.boxSP.add_widget(self.lblSP[i])
        self.add_widget(self.boxSP)

    def crear_listas(self):                             #Crea las listas mezcladas
        self.lista_mezclada_PP = []
        self.lista_mezclada_SP = []
        for i in range(len(self.lista_palabras)):
            self.lista_mezclada_PP.append(self.lista_palabras[i][0])
            self.lista_mezclada_SP.append(self.lista_palabras[i][1])
        self.lista_mezclada_PP, self.lista_mezclada_SP = self.chequear_listas(self.lista_mezclada_PP, self.lista_mezclada_SP)
    
    def chequear_listas(self, lista1, lista2):          #Chequea que estén mezcladas
        x = []
        lista_control = []
        for i in range(len(lista1)):
            x.append(lista1[i] + lista2[i])
        for i in range(len(self.lista_palabras)):
            lista_control.append(self.lista_palabras[i][0] + self.lista_palabras[i][1])
        while any(palabra in lista_control for palabra in x):
            random.shuffle(lista1)
            random.shuffle(lista2)
            x = []
            for i in range(len(lista1)):
                x.append(lista1[i] + lista2[i])
        return lista1, lista2

if __name__ == '__main__': 
    lista_palabras = [
            ('BA', 'NANA', 'El tipo ese es un langa, debe estar lleno de potasio porque es un terrible ...'),
            ('AC', 'ELGA', 'Si vas a saludar en la verdulería no les digas "¡Qué ...!"'),
            ('NA', 'BO', 'Si no lo sabés está todo bien, no te preocupes por quedar como un ...'),
            ('NARA', 'NJA', 'Oíme, igual, la posta es que si no sabés de qué va el juego no pasa ...'),
            ('MAN', 'GO', 'Irónicamente no tengo esta fruta, porque no cobré un ...'),
            ('PE', 'PINO', 'Si no entendés la consigna, se podría decir que no entendiste un ...'),
            ('DU', 'RAZNO', 'No se lo dije al asador, pero el vacío casi me saca un diente, estaba re ...'),
            ('ZAP', 'ALLAZO', 'La clavó al ángulo con tremenda violencia, fue un terrible ...'),
            ('TOM', 'ATE', 'Cuando estabas loco se solía decir que estabas del ...')
        ]

    class PalCruzApp(App):
        def build(self):
            columnas = Columnas(lista_palabras)
            return columnas

    PalCruzApp().run()