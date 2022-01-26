from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from archivo_exterior import obtener_lista_niveles
from functools import partial
from color_label import ButtonBlue

class crMenuNiveles(StackLayout):
    #PARAMETROS: (niveles= LISTA con sublistas= SUBLISTA con 3 elementos: Nombre del conjunto de niveles, nombre del primer nivel, nombre del segundo nivel) SACAR DE 'obtener_lista_niveles'
    def __init__(self, niveles, **kwargs):
        super().__init__(**kwargs)
        self.scroll_timeout = 0
        self.init_layout(niveles)
        self.padding = 10
        self.spacing = 10

    def init_layout(self, niveles):
        self.botones = []
        self.niveles = niveles
        i = 0
        for nivel in self.niveles:
            self.botones.append(ButtonBlue(text=nivel[0], size_hint=(1, None), height=50, font_name='fonts/bebas_neue.ttf', font_size=25))
            self.add_widget(self.botones[i])
            self.botones[i].bind(on_press=self.apretar_boton)
            i += 1
        self.size_hint = (1, None)
        self.bind(minimum_height = self.setter('height'))

    def apretar_boton(self, instance):
        nivel = instance.text
        for lvl in self.niveles:
            if lvl[0] == nivel:
                self.parent.parent.parent.crear_selector(lvl[0], lvl[1], lvl[2])
                pass

class crPregameMenu(ScrollView):
    #PARAMETROS: (niveles= LISTA con 3 elementos: Nombre del conjunto de niveles, nombre del primer nivel, nombre del segundo nivel)  SACAR DE 'obtener_lista_niveles'
    def __init__(self, niveles, **kwargs):
        super(crPregameMenu, self).__init__(**kwargs)
        niveles = crMenuNiveles(niveles)
        niveles.size_hint = (1, None)
        niveles.height = niveles.minimum_height
        self.add_widget(niveles)

if __name__ == '__main__':
    class MiApp(App):
        def build(self):
            ruta = 'cr_files/niveles.txt'
            return crPregameMenu(obtener_lista_niveles(ruta))

    MiApp().run()