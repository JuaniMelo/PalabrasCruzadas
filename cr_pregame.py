from kivy.app import App
from kivy.animation import Animation
from kivy.uix.togglebutton import ToggleButton
from color_label import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.core.window import Window
Window.size = (660, 540)
Window.borderless = False
Window.left = 200
Window.top = 140

class crPregame(BoxLayout):
    def __init__(self, nombre_nivel, opa_text, opb_text, **kwargs):
        super().__init__(**kwargs)
        self.lista_a = ['Alista', 'A']
        self.lista_b = ['Blista', 'B']
        self.nombre_nivel = nombre_nivel
        self.opA = opa_text
        self.opB = opb_text
        self.orientation = 'vertical'
        self.nivel_elegido = ''
    #TITULO
        ttl = ColorLabel(markup=True,                   #Label del título
            text='[b]Pasa[/b]palabra',
            font_size=80,
            size_hint=(1, .4),
            color=(.9, .5, .1, 1),
            font_name='fonts/bebas_neue.ttf')
        self.add_widget(ttl)
    #NIVELES
        niv = Label(text=nombre_nivel,                    #Label del nivel
            font_name='fonts/literal/Literal-Bold.ttf', 
            color= (.9, .5, .1, 1), 
            font_size= 40, 
            size_hint=(1, .3))
        self.add_widget(niv)
    #OPCIONES
        self.opcion1 = ToggleButton(text=self.opA,                    #Label del opcion 1
            group = 'niveles', 
            halign = 'center', 
            size_hint= (.5, .1), 
            pos_hint= {'center_x': .5, 'center_y': .5}, 
            padding= (0, 50), 
            font_size= 20, 
            color= (0,0,0,1))
        self.add_widget(self.opcion1)
        espacio = Label(text='', size_hint=(1, .05))
        self.add_widget(espacio)
        self.opcion2 = ToggleButton(text=self.opB,                    #Label del opcion 2
            group = 'niveles', 
            halign = 'center', 
            size_hint= (.5, .1), 
            padding= (0, 50), 
            pos_hint= {'center_x': .5, 'center_y': .5}, 
            font_size= 20, 
            color= (0,0,0,1))
        self.add_widget(self.opcion2)
        self.opcion1.bind(state=self.opA_estado)
        self.opcion2.bind(state=self.opB_estado)
    #ELEGI
        elegi = Label(text='Elegí qué juego querés jugar primero', 
            font_name='fonts/literal/Literal-Bold.ttf', 
            color= (.9, .5, .1, 1), 
            font_size= 30, 
            size_hint=(1, .2))
        self.add_widget(elegi)
    #BOTONES
        botones = BoxLayout(size_hint=(1, .2), spacing=30, padding=(30, 0))
        btn_ver = ButtonMagenta(text='VER', outline_width=3, outline_color=(0, 0, 0), font_size= 20, bold=True)
        btn_ver.bind(on_release=self.ver_lista)
        botones.add_widget(btn_ver)
        btn_jugar = ButtonGreen(text='JUGAR', outline_width=3, outline_color=(0, 0, 0), font_size= 20, bold=True)        
        btn_jugar.bind(on_release=self.pasar_screen)
        botones.add_widget(btn_jugar)
        self.add_widget(botones)
    #SEPARADOR
        self.add_widget(Label(size_hint=(1, .05)))

    def opA_estado(self, instance, algo):
        if self.opcion1.state == 'down':
            self.opcion1.background_down = ''
            self.lista_palabras = self.lista_a
            self.nivel_elegido = self.opA
            self.opcion1.font_size = 22
            self.opcion1.outline_color = (1, 1, 1)
            self.opcion1.outline_width = 2
            self.opcion1.color = (0, 0, 0, 1)
            print(f'Nivel elegido: {self.opA}')
        else:
            self.opcion1.background_normal = ''
            self.lista_palabras = ['']
            self.nivel_elegido = ''
            self.opcion1.font_size = 20
            self.opcion1.outline_width = 0
            print('No hay un nivel elegido')
    
    def opB_estado(self, instance, algo):
        if self.opcion2.state == 'down':
            self.lista_palabras = self.lista_b
            self.nivel_elegido = self.opB
            self.opcion2.font_size = 22
            self.opcion2.outline_color = (1, 1, 1)
            self.opcion2.outline_width = 2
            self.opcion2.color = (0, 0, 0, 1)
            print(f'Nivel elegido: {self.opB}')
        else:
            self.lista_palabras = ['']
            self.nivel_elegido = ''
            self.opcion2.font_size = 20
            self.opcion2.outline_width = 0
            print('No hay un nivel elegido')

    def pasar_screen(self, instance):
        if self.nivel_elegido == '':
            return
        elif self.nivel_elegido == self.opA:
            self.nivel_no_elegido = self.opB
        elif self.nivel_elegido == self.opB:
            self.nivel_no_elegido = self.opA
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