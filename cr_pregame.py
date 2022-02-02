from kivy.app import App
from kivy.animation import Animation
from kivy.uix.togglebutton import ToggleButton
from color_label import *
from archivo_exterior import obtener_lista_palabras
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.lang import Builder
Window.size = (660, 540)
Window.borderless = False
Window.left = 200
Window.top = 140

Builder.load_string('''
<MiPopup>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: popup_lbl
            halign: 'center'
        ButtonBlue:
            id : btn_ok
            size_hint: (.6, None)
            height: 28
            font_size: 12
            pos_hint: {'center_x': .5, 'center_y': .5}
            text: 'Aceptar'
''')

class MiPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.separator_color = (30/255, 60/255, 100/255, 1)
        self.separator_height = 0
        self.title = 'Nivel no disponible'
        self.title = ''
        self.background = 'images/fondos/errorFondo.png'
        self.ids.popup_lbl.text = '\n\n\n\nNivel incompleto\nAgregue contenido\npara jugar'
        self.ids.popup_lbl.color = (0, 0, 0, 1)
        self.ids.popup_lbl.font_size = 12
        self.size_hint = (None, None)
        self.size = (150, 200)
        self.pos_hint= {'center_x': .5, 'center_y': .5}
        self.ids.btn_ok.bind(on_release=self.salir)

    def salir(self, instance):
        self.dismiss()
        #self.parent.parent.remove_widget(self.parent.parent.box_error)
        #print('FOO')

class crPregame(BoxLayout):
    NARANJA=(190/255, 100/255, 0, 1)
    AZUL=(38/255, 81/255, 142/255, 1)
    AZUL_OSCURO=(30/255, 60/255, 100/255, 1)
    ROJO=(193/255, 34/255, 34/255, 1)
    VERDE=(77/255, 140/255, 32/255, 1)
    AMARILLO=(204/255, 189/255, 18/255, 1)
    MAGENTA=(180/255, 23/255, 222/255, 1)
    NARANJA_CLARO=(1, .5, 0, 1)
    BLANCO=(1, 1, 1, 1)
    NEGRO=(0, 0, 0, 1)
    FUENTE = 'fonts/merriweather-sans/MerriweatherSans-Bold.ttf'
    FUENTE_BOLD = 'fonts/merriweather-sans/MerriweatherSans-ExtraBold.ttf'
    NORMAL_TOGGLE = 'images/botones/btn_claro.png'                         #'images/fondo_no_resaltado.png'
    DOWN_TOGGLE = 'images/botones/btn_claro_selec.png'                           #'images/fondo_resaltado2.png'

    def __init__(self, nombre_nivel, opa_text, opb_text, **kwargs):
        super().__init__(**kwargs)
        self.lista_a = ['Alista', 'A']
        self.lista_b = ['Blista', 'B']
        self.nombre_nivel = nombre_nivel
        self.opA = opa_text
        self.opB = opb_text
        self.orientation = 'vertical'
        self.nivel_elegido = ''
    #NIVELES
        niv = Button(disabled = True,
            background_disabled_normal = 'images/botones/btn_oscuro.png', 
            bold = True, 
            text = nombre_nivel, 
            color = self.NARANJA, 
            outline_width= 4,
            outline_color=self.AZUL_OSCURO,
            font_name = 'fonts/bebas_neue.ttf',               #'fonts/bebas_neue.ttf'
            font_size = 40, 
            size_hint = (1, .2))
        self.add_widget(niv)
    #ELEGI
        elegi = Label(text=' ', 
            font_name='fonts/bebas_neue.ttf', color= self.NARANJA, font_size= 30, size_hint=(1, .3))
        elegi.height = elegi.height+80
        self.add_widget(elegi)
        espacio2 = Label(text='', size_hint=(1, .05))
        self.add_widget(espacio2)
    #OPCIONES
        self.opciones = BoxLayout(orientation='vertical',padding=10, spacing=0, size_hint=(1, 0.35))
        self.add_widget(self.opciones)
        self.opcion1 = HoverButtonMenu(text=self.opA,                    #Label del opcion 1
            background_normal = self.NORMAL_TOGGLE,
            background_down = self.DOWN_TOGGLE,
            font_name = self.FUENTE,
            group = 'niveles', 
            halign = 'center', 
            font_size= 25,
            color = self.NARANJA)
        self.opciones.add_widget(self.opcion1)
        self.opcion2 = HoverButtonMenu(text=self.opB,                    #Label del opcion 2
            background_normal = self.NORMAL_TOGGLE,
            background_down = self.DOWN_TOGGLE,
            font_name = self.FUENTE,
            group = 'niveles', 
            halign = 'center', 
            font_size= 25,
            color = self.NARANJA)
        self.opciones.add_widget(self.opcion2)
        self.opcion1.bind(state=self.opA_estado)
        self.opcion2.bind(state=self.opB_estado)
        self.add_widget(Label(size_hint=(1, .03)))
    #BOTONES
        botones = BoxLayout(size_hint=(1, .1), spacing=30, padding=(30, 0))
        btn_ver = ButtonOrange(text='EDITAR', font_name='fonts/bebas_neue.ttf', font_size=25)
        btn_ver.bind(on_release=self.ver_lista)
        botones.add_widget(btn_ver)
        btn_jugar = ButtonOrange(text='JUGAR', font_name='fonts/bebas_neue.ttf', font_size=25)        
        btn_jugar.bind(on_release=self.pasar_screen)
        botones.add_widget(btn_jugar)
        self.add_widget(botones)
        espacio2 = Label(text='', size_hint=(1, .05))
    #SEPARADOR
        self.add_widget(Label(size_hint=(1, .05)))

    def opA_estado(self, instance, algo):
        if self.opcion1.state == 'down':
            self.lista_palabras = self.lista_a
            self.nivel_elegido = self.opA
            #self.opcion1.font_size = 25
            #self.opcion1.font_name = self.FUENTE_BOLD
            self.opcion1.color = self.NARANJA_CLARO
            #print(f'Nivel elegido: {self.opA}')
        else:
            self.lista_palabras = ['']
            self.nivel_elegido = ''
            #self.opcion1.font_size = 25
            #self.opcion1.font_name = self.FUENTE
            self.opcion1.color = self.NARANJA
            #print('No hay un nivel elegido')
    
    def opB_estado(self, instance, algo):
        if self.opcion2.state == 'down':
            self.lista_palabras = self.lista_b
            self.nivel_elegido = self.opB
            #self.opcion2.font_size = 25
            #self.opcion2.font_name = self.FUENTE_BOLD
            self.opcion2.color = self.NARANJA_CLARO
            #print(f'Nivel elegido: {self.opB}')
        else:
            self.lista_palabras = ['']
            self.nivel_elegido = ''
            #self.opcion2.font_size = 25
            #self.opcion2.font_name = self.FUENTE
            self.opcion2.color = self.NARANJA
            #print('No hay un nivel elegido')

    def pasar_screen(self, instance):
    #Chequea que las listas de rondas no estén vacías
        if self.nivel_elegido == '':
            return
        elif self.nivel_elegido == self.opA:
            self.nivel_no_elegido = self.opB
            if len(obtener_lista_palabras(self.nombre_nivel,self.opA)) == 0 or len(obtener_lista_palabras(self.nombre_nivel,self.opB)) == 0:
                self.box_error = MiPopup()
                self.box_error.open()
                return
        elif self.nivel_elegido == self.opB:
            self.nivel_no_elegido = self.opA
            if len(obtener_lista_palabras(self.nombre_nivel,self.opA)) == 0 or len(obtener_lista_palabras(self.nombre_nivel,self.opB)) == 0:
                self.box_error = MiPopup()
                self.box_error.open()
                return
        self.parent.parent.parent.crear_juego(self.nombre_nivel, self.nivel_elegido, self.nivel_no_elegido)

    def ver_lista(self, instance):
        self.parent.parent.parent.crear_editor(self.nombre_nivel)

if __name__ == '__main__':
    class Pasapalabra(App):
        def build(self):
            bg_image = BgImage(source='images/blue_bg.jpg')
            current_screen = crPregame('NIVEL PRIMERO', 'Juego de la frutas', 'Juego de las prendas')
            bg_image.add_widget(current_screen)
            return bg_image


    Pasapalabra().run()