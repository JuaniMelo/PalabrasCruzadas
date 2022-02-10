from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from color_label import *
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
Window.size = (960, 540)
Window.borderless = False
Window.left = 100
Window.top = 140

Builder.load_string( '''
<crGamePuntos>:
    source: self.source
    canvas.before:
        Rectangle:
            source: self.source
            pos: self.pos
            size: self.size
''')

class crGamePuntos(BoxLayout):

    FPS = 30
    FUENTE = 'fonts/Eurostile.ttf'
    ALT_FUENTE = 25
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
        self.init_layout()

        '''self.layout_central = BoxLayout(size_hint=(1, .5), orientation='vertical', padding=(0, 240, 0, 0))
        self.add_widget(self.layout_central)
        self.lbl_nivel=Label(text=nombre_ronda, font_name=self.FUENTE, font_size=40)
        self.layout_central.add_widget(self.lbl_nivel)
    #Arma los botones de JUGAR y SIGUIENTE
        self.btn_salir=ButtonOrange(text='SALIR', size_hint=(1, .05), font_name=self.FUENTE, font_size=25, padding=(10, 10))
        self.btn_salir.bind(on_release=self.apretar_boton_salir)
        self.add_widget(self.btn_salir)'''

    def init_puntos(self):
        self.total0_actual = 0
        self.total1_actual = 0
        self.tiempo0 = int(self.tiempo[0]/2)
        self.tiempo1 = int(self.tiempo[1]/2)
        self.aciertos0 = self.aciertos[0]
        self.aciertos1 = self.aciertos[1]
        self.total0 = self.tiempo0+self.aciertos0
        self.total1 = self.tiempo1+self.aciertos1
        print(f'tiempo nar: {self.tiempo0}, tiempo azul: {self.tiempo1}, aciertos nar: {self.aciertos0}, aciertos azul: {self.aciertos1}, total nar: {self.total0}, total nar: {self.total1}, ')
        
    def init_layout(self):
    #CREA EL TITULO Y LAS ETIQUETAS DE LOS EQUIPOS
    #TITULO
        self.lbl_nivel = ImageLabel(color= self.NARANJA,
            source= 'images/botones/btn_oscuro.png',
            text= self.nombre_nivel,
            size_hint= (1, .2),
            font_name= 'fonts/bebas_neue.ttf',
            font_size= 30)
            #padding= (0,0,100,0))
        self.add_widget(self.lbl_nivel)
    #BOX DE PUNTOS
        self.puntos_box = BoxLayout(spacing=10, padding=10)
        self.add_widget(self.puntos_box)
        self.stack_naranja = StackLayout(orientation='tb-lr')
        self.puntos_box.add_widget(self.stack_naranja)
        self.stack_azul = StackLayout(orientation='tb-lr')
        self.puntos_box.add_widget(self.stack_azul)
    #ETIQUETAS DEL EQUIPO    
        self.lbl_naranja = ColorLabel(color= self.NARANJA,
            text= 'EQUIPO NARANJA',
            size_hint= (1, .1),
            font_name= 'fonts/bebas_neue.ttf',
            font_size= 25,
            padding= (0, 10))
        self.stack_naranja.add_widget(self.lbl_naranja)
        self.lbl_azul = ColorLabel(color= self.AZUL,
            text= 'EQUIPO AZUL',
            size_hint= (1, .1),
            font_name= 'fonts/bebas_neue.ttf',
            font_size= 25,
            padding= (0, 10))
        self.stack_azul.add_widget(self.lbl_azul)
    #Arma los botones de JUGAR
        self.btn_salir=ButtonOrange(text='VOLVER AL MENU PRINCIPAL', size_hint=(1, .1), font_name='fonts/bebas_neue.ttf', font_size=25, padding=(10, 10))
        self.btn_salir.bind(on_release=self.apretar_boton_salir)
        self.add_widget(self.btn_salir)
        crear_aciertos = Clock.schedule_once(self.init_pts_aciertos, .5)
        #crear_tiempo = Clock.schedule_once(self.init_pts_tiempo, 1)
        #crear_totales = Clock.schedule_once(self.init_pts_total, 1.5)


    def init_pts_aciertos(self, dt):
    #AÑADE LOS ACIERTOS NARANJAS
        self.aciertos_lbl_naranja = Label(text_size= self.size,
            halign= 'left',
            text= 'ACIERTOS:',
            font_name= self.FUENTE,
            font_size= self.ALT_FUENTE,
            size_hint=(.5, None),
            height=20)
        self.stack_naranja.add_widget(self.aciertos_lbl_naranja)
        self.aciertos_pts_naranja = Label(text_size= self.size,
            halign= 'right',
            text= str(self.aciertos0),
            font_name= self.FUENTE,
            font_size= self.ALT_FUENTE,
            size_hint=(.5, None),
            height=20)
        self.stack_naranja.add_widget(self.aciertos_pts_naranja)
    #AÑADE LOS ACIERTOS AZULES
        self.aciertos_lbl_azul = Label(text_size= self.size,
            halign= 'left',
            text= 'ACIERTOS:',
            font_name= self.FUENTE,
            font_size= self.ALT_FUENTE,
            size_hint=(.5, None),
            height=20)
        self.stack_azul.add_widget(self.aciertos_lbl_azul)
        self.aciertos_pts_azul = Label(text_size= self.size,
            halign= 'right',
            text= str(self.aciertos1),
            font_name= self.FUENTE,
            font_size= self.ALT_FUENTE,
            size_hint=(.5, None),
            height=20)
        self.stack_azul.add_widget(self.aciertos_pts_azul)
        crear_tiempo = Clock.schedule_once(self.init_pts_tiempo, .5)
        
    def init_pts_tiempo(self, dt):
        #AÑADE LOS TIEMPOS NARANJAS
        self.tiempo_lbl_naranja = Label(text_size= self.size,
            halign= 'left',
            text= 'TIEMPO RESTANTE:',
            font_name= self.FUENTE,
            font_size= self.ALT_FUENTE,
            size_hint=(.5, None),
            height=20)
        self.stack_naranja.add_widget(self.tiempo_lbl_naranja)
        self.tiempo_pts_naranja = Label(text_size= self.size,
            halign= 'right',
            text= str(self.tiempo0),
            font_name= self.FUENTE,
            font_size= self.ALT_FUENTE,
            size_hint=(.5, None),
            height=20)
        self.stack_naranja.add_widget(self.tiempo_pts_naranja)
    #AÑADE LOS TIEMPOS AZULES
        self.tiempo_lbl_azul = Label(text_size= self.size,
            halign= 'left',
            text= 'TIEMPO RESTANTE:',
            font_name= self.FUENTE,
            font_size= self.ALT_FUENTE,
            size_hint=(.5, None),
            height=20)
        self.stack_azul.add_widget(self.tiempo_lbl_azul)
        self.tiempo_pts_azul = Label(text_size= self.size,
            halign= 'right',
            text= str(self.tiempo1),
            font_name= self.FUENTE,
            font_size= self.ALT_FUENTE,
            size_hint=(.5, None),
            height=20)
        self.stack_azul.add_widget(self.tiempo_pts_azul)
        crear_totales = Clock.schedule_once(self.init_pts_total, .5)

    def init_pts_total(self, dt):
    #AÑADE ESPACIOS
        self.stack_naranja.add_widget(ImageLabel(source='images/fondo_resaltado.png',size_hint=(1, None),height=20))
        self.stack_azul.add_widget(ImageLabel(source='images/fondo_resaltado.png',size_hint=(1, None),height=20))
    #AÑADE LOS LABELS
        self.total_lbl_naranja = Label(text_size= self.size,
            halign= 'left',
            text= 'TOTAL:',
            font_name= self.FUENTE,
            font_size= self.ALT_FUENTE,
            size_hint=(.5, None),
            height=20)
        self.stack_naranja.add_widget(self.total_lbl_naranja)
        self.total_pts_naranja = Label(text_size= self.size,
            halign= 'right',
            text= str(self.total0_actual),
            font_name= self.FUENTE,
            font_size= self.ALT_FUENTE,
            size_hint=(.5, None),
            height=20)
        self.stack_naranja.add_widget(self.total_pts_naranja)
    #AÑADE LOS TIEMPOS AZULES
        self.total_lbl_azul = Label(text_size= self.size,
            halign= 'left',
            text= 'TOTAL:',
            font_name= self.FUENTE,
            font_size= self.ALT_FUENTE,
            size_hint=(.5, None),
            height=20)
        self.stack_azul.add_widget(self.total_lbl_azul)
        self.total_pts_azul = Label(text_size= self.size,
            halign= 'right',
            text= str(self.total1_actual),
            font_name= self.FUENTE,
            font_size= self.ALT_FUENTE,
            size_hint=(.5, None),
            height=20)
        self.stack_azul.add_widget(self.total_pts_azul)
        #self.actualizando = True
        #self.actualizar_puntos()
        self.clock = Clock.schedule_interval(self.actualizar_puntos, 1/self.FPS)
        self.clock2 = Clock.schedule_interval(self.debug, .5)

    def actualizar_puntos(self, dt):
        if self.total0_actual < self.total0:
            self.total0_actual += dt*self.FPS
        else:
            self.total0_actual = self.total0
        if self.total1_actual < self.total1:
            self.total1_actual += dt*self.FPS
        else:
            self.total1_actual = self.total1
        if self.total0_actual >= self.total0 and self.total1_actual >= self.total1:
            self.total0_actual = self.total0
            self.total1_actual = self.total1
            print(f'current naranja: {self.total0_actual} y current azul {self.total1_actual}')
            self.clock.cancel()

    def debug(self, dt):
        if self.stack_azul.opacity == .2:
            self.stack_azul.opacity = 1
        else:
            self.stack_azul.opacity = .2

    def apretar_boton_salir(self, instance):
        self.parent.parent.salir_del_juego()



if __name__ == '__main__':

    class JugarRonda(App):
        def build(self):
            return crGamePuntos('Frutas y Prendas',(0, 15), (4, 9))

    JugarRonda().run()