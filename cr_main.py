from kivy.uix.image import Image
from kivy.uix.widget import Widget
from cr_game import *
from cr_selector_nivel import *
from archivo_exterior import *
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.app import App

class crScreenManager(ScreenManager):

    TRANS_DUR = .05
    FUENTE = 'fonts/bebas_neue.ttf'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition(duration=self.TRANS_DUR)
        self.cr_screen_menu = SelectorNivel(name='menu')
        self.add_widget(self.cr_screen_menu)
        self.cr_screen_trans_b = FadeScreen(color=(0,0,0,1),name='fadeblack')
        self.add_widget(self.cr_screen_trans_b)
        self.cr_screen_trans_w = FadeScreen(color=(1,1,1,1),name='fadewhite')
        self.add_widget(self.cr_screen_trans_w)
        self.cr_current_game = Screen(name='game')
        self.add_widget(self.cr_current_game)
        self.current = 'menu'

    def comenzar_nivel(self, nivel, ronda1, ronda2):
        self.remove_widget(self.cr_current_game)
        self.cr_current_game = Juego(nivel, ronda1, ronda2, name='game')
        self.add_widget(self.cr_current_game)
        self.current = 'fadeblack'
        self.current = 'game'

    def salir_del_juego(self):
        self.remove_widget(self.cr_current_game)
        self.cr_current_game = Screen(name='game')
        self.add_widget(self.cr_current_game)
        self.current = 'menu'

class FadeScreen(Screen):
    def __init__(self,color=(0,0,0,1), **kw):
        super().__init__(**kw)
        img = Image(color=color)
        self.add_widget(img)

if __name__ == '__main__':
    class MiApp(App):
        def build(self):
            return crScreenManager()

    MiApp().run()