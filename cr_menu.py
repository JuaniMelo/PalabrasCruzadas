from tkinter import CENTER
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from archivo_exterior import obtener_lista_niveles
from functools import partial
from color_label import ButtonBlue, HoverButton
from kivy.uix.textinput import TextInput

class crMenuNiveles(StackLayout):
    #PARAMETROS: (niveles= LISTA con sublistas= SUBLISTA con 3 elementos: Nombre del conjunto de niveles, nombre del primer nivel, nombre del segundo nivel) SACAR DE 'obtener_lista_niveles'
    def __init__(self, niveles, **kwargs):
        super().__init__(**kwargs)
        self.scroll_timeout = 0
        self.init_layout(niveles)
        self.padding = (8, 0)
        self.spacing = 5

    def init_layout(self, niveles):
        self.botones = []
        self.niveles = niveles
        i = 0
        for nivel in self.niveles:
            self.botones.append(ButtonBlue(disabled_color=(1, 1, 1, 1),text=nivel[0], size_hint=(1, None),width=165, height=50, halign='left',valign='middle', font_name='fonts/bebas_neue.ttf', font_size=15))
            print(self.botones[i].size)
            self.botones[i].text_size=self.botones[i].size
            self.add_widget(self.botones[i])
            self.botones[i].bind(on_press=self.apretar_boton)
            i += 1
        self.size_hint = (1, None)
        self.bind(minimum_height = self.setter('height'))

    def apretar_boton(self, instance):
        for btn in self.botones:
            btn.background_normal = 'images/botones/btn2_blue_normal.png'
            btn.disabled = False
        instance.background_disabled_normal = 'images/botones/btn2_blue_down.png'
        instance.disabled = True
        nivel = instance.text
        for lvl in self.niveles:
            if lvl[0] == nivel:
                self.parent.parent.parent.parent.crear_selector(lvl[0], lvl[1], lvl[2])
                pass

class crPregameMenu(ScrollView):
    #PARAMETROS: (niveles= LISTA con 3 elementos: Nombre del conjunto de niveles, nombre del primer nivel, nombre del segundo nivel)  SACAR DE 'obtener_lista_niveles'
    def __init__(self, niveles, **kwargs):
        super(crPregameMenu, self).__init__(**kwargs)
        niveles = crMenuNiveles(niveles)
        niveles.size_hint = (1, None)
        niveles.height = niveles.minimum_height
        self.add_widget(niveles)

class scMarco(BoxLayout):
    def __init__(self, niveles, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 5
        self.padding = (2, 4)
        self.niveles = niveles
        self.init_layout()

    def init_layout(self):
        self.scMenu = crPregameMenu(self.niveles)
        self.add_widget(self.scMenu)
        self.ingreso = BoxLayout(size_hint=(1, None), height=40, spacing=5, padding = (8, 0))
        self.add_widget(self.ingreso)
        self.nivel_input = TextInput(multiline=False, hint_text='Añadir nivel')
        self.ingreso.add_widget(self.nivel_input)
        self.agregar = ButtonBlue(text='+',font_size=30,size_hint=(None, None), size=(40, 40))
        self.agregar.bind(on_release=self.apretar_boton_agregar)
        self.ingreso.add_widget(self.agregar)

    def apretar_boton_agregar(self, instance):
        if self.nivel_input.text == '' or self.nivel_input.text == ' ':
            return
        else:
            nivel_a_crear = self.nivel_input.text
        self.nivel_input.text = ''
        self.crear_nivel(nivel_a_crear)
    
    def crear_nivel(self, nombre_nivel):
        self.niveles.append([nombre_nivel, 'Primera Ronda', 'Segunda Ronda'])
        self.remove_widget(self.scMenu)
        self.scMenu = crPregameMenu(self.niveles)
        self.add_widget(self.scMenu, index=1)
        #FALTA Escribir el código para guardar en el archivo los cambios






if __name__ == '__main__':
    class MiApp(App):
        def build(self):
            ruta = 'cr_files/niveles.txt'
            return crPregameMenu(obtener_lista_niveles(ruta))


    MiApp().run()