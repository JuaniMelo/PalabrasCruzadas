from turtle import width
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from color_label import *
from kivy.lang import Builder

Builder.load_string( '''
<crGameMenuInicial>:
    source: self.source
    canvas.before:
        Rectangle:
            source: self.source
            pos: self.pos
            size: self.size

<crGameMenuFinal>:
    source: self.source
    canvas.before:
        Rectangle:
            source: self.source
            pos: self.pos
            size: self.size
''')

class crGameMenuInicial(BoxLayout):

    LOGO_CR = 'images/Vane.png'
    FUENTE = 'fonts/bebas_neue.ttf'
    ALT_FUENTE = 20

    def __init__(self, nombre_ronda, **kwargs):
    #PARAMETROS: (nombre de la ronda que se va a jugar)
        super().__init__(**kwargs)
        self.source='images/fondos/fondo_menu.png'
        self.orientation = 'vertical'
        self.layout_central = BoxLayout(size_hint=(1, .5), orientation='vertical', padding=(0, 240, 0, 0))
        self.add_widget(self.layout_central)
        self.lbl_nivel=Label(text=nombre_ronda)
        self.layout_central.add_widget(self.lbl_nivel)
    #Arma los botones de JUGAR y SIGUIENTE
        self.btn_jugar=ButtonOrange(text='JUGAR', size_hint=(1, .05))
        self.btn_jugar.bind(on_release=self.apretar_boton_jugar)
        self.add_widget(self.btn_jugar)
    
    def apretar_boton_jugar(self, instance):
        self.parent.comenzar_ronda()

class crGameMenuFinal(BoxLayout):

    LOGO_CR = 'images/Vane.png'
    FUENTE = 'fonts/bebas_neue.ttf'
    ALT_FUENTE = 20

    def __init__(self, nombre_ronda, lista_aciertos, **kwargs):
    #PARAMETROS: (nombre de la ronda que se va a jugar)
        super().__init__(**kwargs)
        self.nombre_ronda = nombre_ronda
        self.source='images/fondos/fondo_menu.png'
        self.lista_aciertos = lista_aciertos
        self.orientation = 'vertical'
        self.init_layout()

    def init_layout(self):
        self.layout_central = BoxLayout(size_hint=(1, .5), orientation='vertical', padding=(0, 160, 0, 0))
        self.add_widget(self.layout_central)
        self.box_aciertos = BoxLayout(padding=80, size_hint=(1, .8), orientation= 'vertical')
        self.layout_central.add_widget(self.box_aciertos)
    #Arma los aciertos y errores
        self.aciertos = StackLayout(spacing=5, padding=40)
        self.box_aciertos.add_widget(self.aciertos)
        self.errores = StackLayout(spacing=5, padding=40)
        self.box_aciertos.add_widget(self.errores)
    #Arma el botón SIGUIENTE
        self.btn_siguiente=ButtonOrange(text='SIGUIENTE', size_hint=(1, .05)) 
        self.btn_siguiente.bind(on_release=self.apretar_boton_siguiente)
        self.add_widget(self.btn_siguiente)

    def crear_listas_aciertos(self):
        self.palabras_acertadas, self.palabras_no_acertadas = self.obtener_aciertos()
        self.lbl_acertadas = []
        self.lbl_no_acertadas = []
        if len(self.palabras_acertadas) < 1:
            self.lbl_acertadas.append(Label(text='\n¡NO ACERTASTE NINGUNA PALABRA!', font_name=self.FUENTE, size_hint=(1, 1), font_size=self.ALT_FUENTE))
            self.aciertos.add_widget(self.lbl_acertadas[0])
        else:
            for i in range(len(self.palabras_acertadas)):
                self.lbl_acertadas.append('')
                self.lbl_acertadas[i] = ColorLabel(text=self.palabras_acertadas[i], color=(0, .7, .1, 1), font_name=self.FUENTE, size_hint=(None, None), size=(140, 30), font_size=self.ALT_FUENTE)
                self.aciertos.add_widget(self.lbl_acertadas[i])
        if len(self.palabras_no_acertadas) < 1:
            self.lbl_no_acertadas.append(Label(text='¡FELICITACIONES! ACERTASTE TODAS LAS PALABRAS', font_name=self.FUENTE, size_hint=(1, 1), font_size=self.ALT_FUENTE))
            self.errores.add_widget(self.lbl_no_acertadas[0])
        else:
            for i in range(len(self.palabras_no_acertadas)):
                self.lbl_no_acertadas.append('')
                self.lbl_no_acertadas[i] = ColorLabel(text=self.palabras_no_acertadas[i], color=(.7, 0, .1, 1), font_name=self.FUENTE, size_hint=(None, None), size=(140, 30), font_size=self.ALT_FUENTE)
                self.errores.add_widget(self.lbl_no_acertadas[i])
                print('foo')

    def obtener_aciertos(self):
        palabras_acertadas = []
        palabras_no_acertadas = []
        i = 0
        for acierto in self.lista_aciertos:
            if acierto:
                palabras_acertadas.append(self.parent.lista_palabras[i][0] + self.parent.lista_palabras[i][1])
            else:
                palabras_no_acertadas.append(self.parent.lista_palabras[i][0] + self.parent.lista_palabras[i][1])
            i +=1
        return palabras_acertadas, palabras_no_acertadas

    def apretar_boton_siguiente(self, instance):
        self.parent.siguiente_ronda()