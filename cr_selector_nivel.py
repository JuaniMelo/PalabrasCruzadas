from kivy.app import App
from color_label import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
import archivo_exterior
from cr_menu import *
from cr_pregame import *
from cr_registro import *
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
Window.size = (960, 540)
Window.borderless = False
Window.left = 100
Window.top = 140

class SelectorNivel(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Rectangle(source='images/fondos/sCruzadas_menu.png', size_hint=(None, None), size=Window.size)
        self.lista_niveles = obtener_lista_niveles('cr_files/niveles.txt')
        self.init_layout()
        
    def init_layout(self):
        self.main_layout= BoxLayout(padding = (0, 5))
        self.add_widget(self.main_layout)
        self.scroll_menu=scMarco(self.lista_niveles, size_hint=(None, 1), width=200)
        self.main_layout.add_widget(self.scroll_menu)
        self.fondo_lado = BgImage(source='images/fondos/sCruzadas_menu.png')
        self.main_layout.add_widget(self.fondo_lado)
        self.reset_fondo_lado()

    def reset_fondo_lado(self):
    #resetea el fondo para mostrar la imagen de menú pelado
        self.fondo_lado.clear_widgets()
        fondo = BgImage(source='images/fondos/sCruzadas_menu.png')
        self.fondo_lado.add_widget(fondo)

    def crear_selector(self, nivel, ronda1, ronda2):
        self.fondo_lado.clear_widgets()
        self.selector_nivel = crPregame(nivel, ronda1, ronda2)
        self.fondo_lado.add_widget(self.selector_nivel)

    def crear_editor(self, nivel):
        self.fondo_lado.clear_widgets()
        for lvl in self.lista_niveles:
            if lvl[0] == nivel:
                nivel_elegido = lvl
        self.editor_nivel = MainMenu(nivel_elegido)
        self.fondo_lado.add_widget(self.editor_nivel)

    def crear_juego(self, nivel, ronda1, ronda2):
        #cambiar al juego
        pass

if __name__ == '__main__':
    class MiApp(App):
        def build(self):
            Window.bind(on_resize=self.fix_size)
            return SelectorNivel()

        def fix_size(self, instance, width, height):
            Window.size = ((960, 540))

    MiApp().run()