from kivy.app import App
from color_label import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
import archivo_exterior
from cr_game_ronda import *
from cr_menu import *
from cr_pregame import *
from cr_registro import *
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
Window.size = (960, 540)
Window.borderless = True
Window.left = 100
Window.top = 140

class Juego(Screen):
    def __init__(self, nombre_nivel, ronda1, ronda2, **kwargs):
        super().__init__(**kwargs)
        self.primera_ronda = ronda1
        self.segunda_ronda = ronda2
        self.nombre_nivel = nombre_nivel
        self.cont_rondas = 0
        self.init_layout()
        
    def init_layout(self):
        lista_palabras = obtener_lista_palabras('cr_files/niveles.txt', self.primera_ronda)
        self.juego = crRonda(self.primera_ronda, lista_palabras)
        self.add_widget(self.juego)

    def siguiente_ronda(self):
        self.cont_rondas += 1
        if self.cont_rondas < 2:
            self.clear_widgets()
            lista_palabras = obtener_lista_palabras('cr_files/niveles.txt', self.segunda_ronda)
            self.juego = crRonda(self.segunda_ronda, lista_palabras)
            self.add_widget(self.juego)
        else:
            self.clear_widgets()        #CAMBIAR DE PANTALLA AL RESUMEN DE LOS PUNTOS DE CADA EQUIPO
            pass

    def volver_al_menu(self):
        pass

if __name__ == '__main__':
    class MiApp(App):
        def build(self):
            lista_niveles = obtener_lista_niveles('cr_files/niveles.txt')
            return Juego(lista_niveles[0][0], lista_niveles[0][1], lista_niveles[0][2])

    MiApp().run()