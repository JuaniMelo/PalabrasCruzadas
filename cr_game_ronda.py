from kivy.app import App
from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from cr_game_columnas import Columnas
from cr_game_menu import *
from color_label import *
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
Window.size = (960, 540)
Window.borderless = True
Window.left = 200
Window.top = 140

Builder.load_string( '''
<crRonda>:
    source: self.source
    canvas.before:
        Rectangle:
            source: self.source
            pos: self.pos
            size: self.size
''')

class crRonda(RelativeLayout):
    FPS = 30
    SEGUNDOS_RONDA = 4
    FUENTE = 'fonts/bebas_neue.ttf'
    ALT_FUENTE = 20
    COLOR = (200/255, 0, 100/255, 1)
    LONG_PARRAFO_PISTA = 90
#INICIALIZADORES
    def __init__(self, nombre_nivel, lista, **kwargs):
        super().__init__(**kwargs)
        self.estado_juego = False
        self.source = 'images/fondos/fondo_azul.png'
        self.size_hint = (1, 1)
        self.nivel = nombre_nivel
        self.lista_palabras = lista
        self.tiempo_actual = self.SEGUNDOS_RONDA * self.FPS
        self.init_layout()
        self.init_menu()
        self.init_aciertos()
        self.contador_pistas = 0
        Clock.schedule_interval(self.actualizar, 1/self.FPS)

    def init_layout(self):
        self.raiz = BoxLayout(orientation='vertical', padding=5, spacing=5)
        self.add_widget(self.raiz)
        '''self.titulo = ColorLabel(text=f'PALABRAS CRUZADAS: {self.nivel}', color=(.7, 0, .3, 1), font_name=self.FUENTE, font_size=45, size_hint=(1, .17))
        self.raiz.add_widget(self.titulo)'''
        self.lbl_pista = ColorLabel(text='',color=(.7,.5,0,1),font_name=self.FUENTE, font_size=30, size_hint=(1, .3))
        self.raiz.add_widget(self.lbl_pista)
        self.columnas = Columnas(self.lista_palabras)
        self.raiz.add_widget(self.columnas)
        self.botones = BoxLayout(padding=5,spacing=5, size_hint=(1, .15))
        self.raiz.add_widget(self.botones)
        self.btn_pasar = ButtonRed(text='PASAPALABRA/INCORRECTO')
        self.btn_pasar.bind(on_release=self.apretar_boton_pasar)
        self.botones.add_widget(self.btn_pasar)
        self.btn_correcto = ButtonGreen(text='CORRECTO')
        self.btn_correcto.bind(on_release=self.apretar_boton_correcto)
        self.botones.add_widget(self.btn_correcto)

    def init_aciertos(self):
        self.aciertos = []
        for elemento in self.lista_palabras:
            self.aciertos.append(False)

    def init_menu(self):
        self.btn_pasar.disabled = True
        self.btn_correcto.disabled = True
        self.menu=crGameMenuInicial(self.nivel)
        self.add_widget(self.menu)

    def nueva_lista(self):
        self.contador_pistas = 0
        self.obtener_pista(self.contador_pistas)

#LOGICA

    def comenzar_ronda(self):
        self.estado_juego = True
        self.nueva_lista()
        self.remove_widget(self.menu)
        self.btn_pasar.disabled = False
        self.btn_correcto.disabled = False

    def terminar_ronda(self):
        self.estado_juego = False
        self.menu = crGameMenuFinal(self.nivel, self.aciertos)
        self.add_widget(self.menu)
        self.menu.crear_listas_aciertos()
        self.btn_pasar.disabled = True
        self.btn_correcto.disabled = True

    def siguiente_ronda(self):
        self.contador_rondas += 1
        self.comenzar_segunda_ronda()               #PROGRAMAR ESTO EN LA SCREEN VIEW

    def obtener_pista(self, i):
        if len(self.lista_palabras[i][2]) < self.LONG_PARRAFO_PISTA:
            self.pista = self.lista_palabras[i][2]
            self.lbl_pista.text = self.pista
        else:
            texto = self.lista_palabras[i][2].split(' ')
            renglones = ['']
            aux = ''
            x = 0
            for word in texto:
                if len(aux) <= self.LONG_PARRAFO_PISTA:
                    # aux = aux + word + ' '
                    aux += f'{word} '
                else:
                    renglones[x] = aux
                    renglones.append('')
                    aux = f'{word} '
                    x += 1
            if renglones[x-1] != aux:
                renglones[x] = aux
            self.pista = '\n'.join(renglones)
            self.lbl_pista.text = self.pista

    def siguiente_pista(self):
        self.contador_pistas += 1
        if self.contador_pistas > len(self.lista_palabras) - 1:
            self.contador_pistas = 0
        while self.aciertos[self.contador_pistas] == True:
            try:
                self.contador_pistas += 1
                if self.contador_pistas > len(self.lista_palabras) - 1:
                    self.contador_pistas = 0
            except:
                raise TimeoutError('Loop infinito')
        self.obtener_pista(self.contador_pistas)

    def buscar_respuesta_correcta(self):
        rtaPP = self.lista_palabras[self.contador_pistas][0]
        rtaSP = self.lista_palabras[self.contador_pistas][1]
        for i in range(len(self.columnas.lista_mezclada_PP)):
            if self.columnas.lista_mezclada_PP[i] == rtaPP:
                self.columnas.lblPP[i].opacity = 0.1
            if self.columnas.lista_mezclada_SP[i] == rtaSP:
                self.columnas.lblSP[i].opacity = 0.1

#BOTONES

    def apretar_boton_pasar(self, instance):
        self.siguiente_pista()

    def apretar_boton_correcto(self, instance):
        self.aciertos[self.contador_pistas] = True
        self.buscar_respuesta_correcta()
        if all(self.aciertos):
            self.terminar_ronda()
            return
        else:
            self.siguiente_pista()

#ACTUALIZAR LOOP

    def actualizar_tiempo(self):
        if self.tiempo_actual > 0:
            self.tiempo_actual -= 1
            self.columnas.temp.text = f'{int(self.tiempo_actual/self.FPS)}'
        else:
            self.terminar_ronda()

    def actualizar(self, dt):
        if self.estado_juego:
            self.actualizar_tiempo()


if __name__ == '__main__':

    nombre_nivel = 'FRUTAS'
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

    class JugarRonda(App):
        def build(self):
            return crRonda(nombre_nivel, lista_palabras)

    JugarRonda().run()