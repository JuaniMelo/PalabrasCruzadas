from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.app import App
from color_label import *
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.core.window import Window
Window.size = (960, 540)
Window.borderless = True
Window.left = 100
Window.top = 140

Builder.load_string( '''
<crGamePuntos>:
    nombre_nivel: self.nombre_nivel
    source: self.source
    canvas.before:
        Rectangle:
            source: self.source
            pos: self.pos
            size: self.size
    ImageLabel:
        color: root.NARANJA
        source: 'images/botones/btn_oscuro.png'
        text: root.nombre_nivel
        size_hint: (1, .2)
        font_name: 'fonts/bebas_neue.ttf'
        font_size: 30
        padding: (0, 10)
    BoxLayout:
        id: cuadro_puntos
        StackLayout:
            id: stack_naranja
            ColorLabel:
                bg_color: (.5, .4, 1, 1)
                color: root.NARANJA
                text: 'EQUIPO NARANJA'
                size_hint: (1, .1)
                font_name: 'fonts/bebas_neue.ttf'
                font_size: 25
                padding: (0, 10)
            GridLayout:
                id: grid_naranja
                cols: 2
        StackLayout:
            id: stack_azul
            ColorLabel:
                color: root.AZUL
                text: 'EQUIPO AZUL'
                size_hint: (1, .1)
                font_name: 'fonts/bebas_neue.ttf'
                font_size: 25
                padding: (0, 10)
            GridLayout:
                id: grid_azul
                cols: 2
    ButtonOrange:
        text: 'salir'
        size_hint: (1, .1)
        font_name: 'fonts/bebas_neue.ttf'
        font_size: 25
        padding: (10, 10)
        on_release: root.apretar_boton_salir
''')

class crGamePuntos(BoxLayout):

    nombre_nivel = StringProperty()
    source: StringProperty()

    FUENTE = 'fonts/Eurostile.ttf'
    ALT_FUENTE = 15
    AZUL= (38/255, 81/255, 142/255, 1)
    NARANJA= (224/255, 135/255, 56/255, 1)

    def __init__(self, nombre_nivel, tiempos_rest, cant_aciertos, **kwargs):
    #PARAMETROS: (nombre de la ronda que se va a jugar)
        super().__init__(**kwargs)
        self.source='images/fondos/fondo_menu.png'
        self.orientation = 'vertical'
        self.padding = 10
        self.nombre_nivel = nombre_nivel
        self.aciertos = cant_aciertos
        self.tiempo = tiempos_rest
        self.init_puntos()

        '''self.layout_central = BoxLayout(size_hint=(1, .5), orientation='vertical', padding=(0, 240, 0, 0))
        self.add_widget(self.layout_central)
        self.lbl_nivel=Label(text=nombre_ronda, font_name=self.FUENTE, font_size=40)
        self.layout_central.add_widget(self.lbl_nivel)
    #Arma los botones de JUGAR y SIGUIENTE
        self.btn_salir=ButtonOrange(text='SALIR', size_hint=(1, .05), font_name=self.FUENTE, font_size=25, padding=(10, 10))
        self.btn_salir.bind(on_release=self.apretar_boton_salir)
        self.add_widget(self.btn_salir)'''

    def init_puntos(self):
        self.tiempo0 = str(self.tiempo[0])
        self.tiempo1 = str(self.tiempo[1])
        self.aciertos0 = str(self.aciertos[0])
        self.aciertos1 = str(self.aciertos[1])
        self.total0 = str(self.tiempo[0]+self.aciertos[0])
        self.total1 = str(self.tiempo[1]+self.aciertos[1])
        
    def init_ui_puntaje(self, tiempo):
    #ARMA LA PRIMER COLUMNA DE TEXTO
        self.ids.grid_naranja = 0
        pass
        
    def crear_puntos_equipo(self, tiempo, aciertos):
        pass

    def apretar_boton_salir(self, instance):
        self.parent.parent.salir_del_juego()



if __name__ == '__main__':

    class JugarRonda(App):
        def build(self):
            return crGamePuntos('Frutas y Prendas',(0, 15), (4, 9))

    JugarRonda().run()