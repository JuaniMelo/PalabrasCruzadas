from archivo_exterior import obtener_lista_niveles, obtener_lista_palabras, guardar_cambios_nivel, eliminar_info_nivel
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from color_label import ButtonBlue, ButtonOrange, ColorLabel, ImageLabel, LabelLeft
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup
from kivy.graphics import *
from functools import partial
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder

Builder.load_string('''
<EditorNivel>:
    BoxLayout:
        Label:
            text: 'hola'
        Label:
            text: 'chau'

<TabbedPanelHeaderEditable>:
    font_name: 'fonts/bebas_neue.ttf'
    font_size: 25

<ConfirmacionPopup>:
    BoxLayout:
        size_hint: (1, 1)
        ButtonBlue:
            id: no_eliminar
        ButtonOrange:
            id : eliminar
            font_size: 12
            pos_hint: {'center_x': .5, 'center_y': .5}
            text: 'Aceptar'
''')

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
FUENTE = 'fonts/bebas_neue.ttf'            #'fonts/merriweather-sans/MerriweatherSans-Bold.ttf'
FUENTE_BOLD = 'fonts/merriweather-sans/MerriweatherSans-ExtraBold.ttf'

class ConfirmacionPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.separator_height = 0
        self.title = '¿Está seguro que desea eliminar este nivel?\nSi lo hace no podrá recuperarlo'
        self.background = 'images/fondos/errorFondo2.png'
        self.size_hint = (None, None)
        self.size = (150, 200)
        self.pos_hint= {'center_x': .5, 'center_y': .5}
        self.ids.no_eliminar.bind(on_release=self.dismiss)

class MiTextInput(TextInput):
    def on_focus(self, *args):
        if self.focus:
            return       
        else:
            self.on_text_validate()

class MiTitulo(ImageLabel):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            self.editar_nombre()
        return super(MiTitulo, self).on_touch_down(touch)

    def editar_nombre(self):
        self.parent.parent.listo_para_guardar = False
        self.parent.nombre_input = MiTextInput(background_color=(1, 1, 1, 0),
            unfocus_on_touch=True,
            halign='center',
            text=self.parent.nombre_nivel,
            multiline=False,
            write_tab=False,
            foreground_color=BLANCO,
            font_name = 'fonts/bebas_neue.ttf',
            font_size = 30,
            on_text_validate = self.confirmar_nombre
            )            #, pos_hint={'center_x':.5, 'center_y':.5}
        self.parent.add_widget(self.parent.nombre_input, index=1)
        self.parent.lbl_nombre.opacity = 0
        self.parent.nombre_input.focus = True
        self.parent.nombre_input.select_all()

    def confirmar_nombre(self, instance):
        nombre=instance.text
        self.parent.lbl_nombre.text = nombre
        self.parent.nombre_nivel = nombre
        self.parent.lbl_nombre.opacity = 1
        self.parent.parent.listo_para_guardar = True
        self.parent.remove_widget(instance)

class TabbedPanelHeaderEditable(TabbedPanelHeader):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            self.editable = True
            self.editar_nombre()
        return super(TabbedPanelHeaderEditable, self).on_touch_down(touch)

    def editar_nombre(self):
        self.parent.parent.listo_para_guardar = False
        self.size_hint=(0, 1)
        self.input = MiTextInput(background_color=(1, 1, 1, 0),
            unfocus_on_touch=True,
            text=self.text, 
            halign='center',
            multiline=False,
            write_tab=False,
            foreground_color=BLANCO,
            font_name = 'fonts/bebas_neue.ttf',
            font_size = 25,
            on_text_validate = self.confirmar_nombre)
        self.parent.add_widget(self.input, index=1)
        self.input.focus = True
        self.input.select_all()
        self.opacity = 0
    
    def confirmar_nombre(self, instance):
        nombre=instance.text.upper()
        self.text = nombre
        self.opacity = 1
        self.parent.parent.listo_para_guardar = True
        self.parent.remove_widget(instance)
        self.size_hint = (1, 1)

class EditorNiveles(BoxLayout):
    def __init__(self, nivel, **kwargs):
        super().__init__(**kwargs)
        self.listo_para_guardar = True
        self.orientation = 'vertical'
        self.nivel = nivel
        self.titulo = TituloNivel(nivel[0])
        self.add_widget(self.titulo)
        self.editor_tabs = TabsEditor(self.nivel)
        self.add_widget(self.editor_tabs)
        self.botones = BotonesEditor()
        self.add_widget(self.botones)

class TituloNivel(RelativeLayout):
    def __init__(self, nombre_nivel, **kwargs):
        super().__init__(**kwargs)
        self.size_hint=(1, .1)
        self.nombre_nivel_original = nombre_nivel
        self.nombre_nivel = nombre_nivel
        self.init_layout()

    def init_layout(self):
        self.btn_editar = ButtonBlue(text='X', size_hint=(None, None), size=(25, 25),font_size=20, pos_hint={'right':.98, 'center_y':.5})
        self.btn_editar.bind(on_release=self.crear_popup)
        self.add_widget(self.btn_editar)
        self.lbl_nombre = MiTitulo(source='images/botones/btn_oscuro.png',
            text=self.nombre_nivel,
            size_hint=(1, 1),
            color=NARANJA_CLARO,
            font_name = FUENTE,
            font_size = 30
            )            #, pos_hint={'center_x':.5, 'center_y':.5}
        self.add_widget(self.lbl_nombre, index=1)
    
    def crear_popup(self, instance):
        self.conf_popup = ConfirmacionPopup()
        self.conf_popup.ids.eliminar.bind(on_release=self.apretar_eliminar_nivel)
        self.conf_popup.open()

    def apretar_eliminar_nivel(self, instance):
        self.conf_popup.dismiss()
        Clock.schedule_once(self.eliminar_nivel, .2)

    def eliminar_nivel(self, dt):
        self.parent.parent.parent.parent.source = 'images/fondos/sCruzadas_menu.png'
        eliminar_info_nivel(self.nombre_nivel_original)
        self.parent.parent.parent.parent.scroll_menu.niveles = obtener_lista_niveles()
        for boton in self.parent.parent.parent.parent.scroll_menu.scMenu.niveles.botones:
            if boton.text == self.nombre_nivel_original:
                self.parent.parent.parent.parent.scroll_menu.scMenu.niveles.remove_widget(boton)
                self.parent.parent.parent.parent.scroll_menu.scMenu.niveles.botones.remove(boton)
                self.parent.parent.parent.parent.fondo_lado.clear_widgets()

class BotonesEditor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding=5
        self.spacing=5
        self.size_hint=(1, None)
        self.height=50
        btn_cancelar = ButtonBlue(text='Cancelar', font_name=FUENTE, font_size=25, on_release=self.cancelar)
        self.add_widget(btn_cancelar)
        btn_guardar = ButtonBlue(text='Guardar', font_name=FUENTE, font_size=25,on_release=self.guardar)
        self.add_widget(btn_guardar)
    
    def cancelar(self, instance):
        #self.parent.remove_widget(menu)
        #del instance.parent
        self.parent.parent.remove_widget(self.parent)

    def guardar(self, instance):
        if self.parent.listo_para_guardar:
        #ARMA EL TEXTO A GUARDAR
            renglon = []
            for elemento in self.parent.editor_tabs.tab_ronda_1.content.hijo.elementos:
                renglon.append(f'{elemento.lbl_PP.text.upper()}&&{elemento.lbl_SP.text.upper()}&&{elemento.lbl_pista.text.upper()}\n')
            renglon.append('<fin>\n')
            txt_ronda_1 = ''.join(renglon)
            renglon = []
            for elemento in self.parent.editor_tabs.tab_ronda_2.content.hijo.elementos:
                renglon.append(f'{elemento.lbl_PP.text.upper()}&&{elemento.lbl_SP.text.upper()}&&{elemento.lbl_pista.text.upper()}\n')
            renglon.append('<fin>\n')
            txt_ronda_2 = ''.join(renglon)
            txt_a_guardar = f'<n>{self.parent.titulo.nombre_nivel.upper()}<n>\n<t>{self.parent.editor_tabs.tab_ronda_1.text.upper()}<t>\n{txt_ronda_1}<t>{self.parent.editor_tabs.tab_ronda_2.text.upper()}<t>\n{txt_ronda_2}\n'
        #GUARDA EL TEXTO GENERADO EN EL ARCHIVO TXT
            guardar_cambios_nivel(self.parent.titulo.nombre_nivel_original, txt_a_guardar)
        #CAMBIA EL NOMBRE DEL SELECTOR DE NIVELES
            for boton in self.parent.parent.parent.parent.scroll_menu.scMenu.niveles.botones:
                if self.parent.titulo.nombre_nivel_original == boton.text:
                    boton.text = self.parent.titulo.nombre_nivel.upper()
        #CAMBIA EL NOMBRE DEL NIVEL ANTERIOR AL ACTUAL
            self.parent.titulo.nombre_nivel_original = self.parent.titulo.nombre_nivel.upper()

class TabsEditor(TabbedPanel):
    BG_NORMAL = 'images/botones/btn2_orange_normal.png'
    BG_DOWN = 'images/botones/btn2_orange_down.png'
    COLOR_FONDO = (198/255, 120/255, 37/255, 1)

    def __init__(self, nivel, **kwargs):
        super().__init__(**kwargs)
        self.tab_width = self.width * 4 - 26
        self.do_default_tab = False
        self.background_color = (0, 0, 0, 0)
        self.tab_ronda_1 = TabbedPanelHeaderEditable(text=nivel[1], background_normal=self.BG_NORMAL, background_down=self.BG_DOWN, size_hint=(.95, 1))
        self.tab_ronda_1.content = Scroller(lista=obtener_lista_palabras(nivel[0],nivel[1]))
        self.add_widget(self.tab_ronda_1)
        self.tab_ronda_2 = TabbedPanelHeaderEditable(text=nivel[2], background_normal=self.BG_NORMAL, background_down=self.BG_DOWN, size_hint=(.95, 1))
        self.tab_ronda_2.content = Scroller(lista=obtener_lista_palabras(nivel[0],nivel[2]))
        self.add_widget(self.tab_ronda_2)

class Scroller(ScrollView):
    def __init__(self, lista=[], **kwargs):
        super(Scroller, self).__init__(**kwargs)
        self.lista = lista
        self.scroll_timeout = 0
        self.hijo = ListBox(self.lista)
        self.hijo.size_hint = (1, None)
        self.hijo.height = self.hijo.minimum_height
        self.add_widget(self.hijo)

class ListBox(StackLayout):
    ALT_FUENTE = 15
    FUENTE = 'fonts/bebas_neue.ttf'

    def __init__(self, lista, **kwargs):
        super().__init__(**kwargs)
        self.editando=False
        self.font = self.FUENTE
        self.elementos= []
        self.lista = lista
        for i in range(len(self.lista)):
            self.crear_elemento(i, lista[i][0], lista[i][1], lista[i][2])
            self.add_widget(self.elementos[i])
    #CREAR INPUT
        self.enter_register = BoxLayout(padding=[5], spacing=5, size_hint=(1, None), height=40)
        self.enter_register.PP_input = TextInput(multiline=False, halign='center', size_hint=(0.1,1), font_name=self.FUENTE, font_size=self.ALT_FUENTE, write_tab = False, on_text_validate=self.agregar_entrada)
        self.enter_register.add_widget(self.enter_register.PP_input)
        self.enter_register.SP_input = TextInput(multiline=False, halign='center', size_hint=(0.1,1), font_name=self.FUENTE, font_size=self.ALT_FUENTE,write_tab = False, on_text_validate=self.agregar_entrada)
        self.enter_register.add_widget(self.enter_register.SP_input)
        self.enter_register.pista_input = TextInput(multiline=False, font_name=self.font, font_size=self.ALT_FUENTE,write_tab = False, on_text_validate=self.agregar_entrada)
        self.enter_register.add_widget(self.enter_register.pista_input)
        self.enter_register.agregar = ButtonBlue(text='Añadir', size_hint=(None,1), width=100, font_name=self.FUENTE, font_size=self.ALT_FUENTE)
        self.enter_register.agregar.bind(on_release=self.agregar_entrada)
        self.enter_register.add_widget(self.enter_register.agregar)
        self.add_widget(self.enter_register)
        self.size_hint = (1, None)
        self.bind(minimum_height = self.setter('height'))

    def agregar_entrada(self, instance):
        PP = self.enter_register.PP_input.text.upper()
        SP = self.enter_register.SP_input.text.upper()
        pista = self.enter_register.pista_input.text.upper()
        if PP != '' and SP != '' and pista != '':
            i = len(self.elementos)
            self.crear_elemento(i, PP, SP, pista)
            self.add_widget(self.elementos[i], index=1)
            self.enter_register.PP_input.text = ''
            self.enter_register.SP_input.text = ''
            self.enter_register.pista_input.text = ''

    def crear_elemento(self, i, textPP, textSP, textPista):
        self.elementos.append(BoxLayout(padding=5, spacing=5, size_hint=(1, None), height=40))
        self.elementos[i].index = i
        self.elementos[i].lbl_PP = Label(text=textPP, size_hint=(0.1,1), font_name=self.FUENTE, font_size=self.ALT_FUENTE, bold=True)
        self.elementos[i].add_widget(self.elementos[i].lbl_PP)
        self.elementos[i].lbl_SP = Label(text=textSP, size_hint=(0.1,1), font_name=self.FUENTE, font_size=self.ALT_FUENTE, bold=True)
        self.elementos[i].add_widget(self.elementos[i].lbl_SP)
        self.elementos[i].lbl_pista = LabelLeft(text=textPista, halign = 'left', valign = 'middle',  font_name=self.FUENTE, font_size=self.ALT_FUENTE)
        self.elementos[i].add_widget(self.elementos[i].lbl_pista)
        self.elementos[i].editar = ButtonBlue(text='Editar', font_size=self.ALT_FUENTE, size_hint=(None, None), size=(60, 35), font_name=self.FUENTE)
        self.elementos[i].editar.bind(on_release=self.editar_elemento)
        self.elementos[i].add_widget(self.elementos[i].editar)
        self.elementos[i].borrar = ButtonBlue(text='X', size_hint=(None, None), size=(35, 35), font_size=self.ALT_FUENTE, font_name=self.FUENTE)
        self.elementos[i].borrar.bind(on_release=self.eliminar_elemento)
        self.elementos[i].add_widget(self.elementos[i].borrar)

    def eliminar_elemento(self, instance):
        index = instance.parent.index
        self.remove_widget(self.elementos[index])
        del self.elementos[index]
        i = 0    
        for elem in self.elementos:        
            elem.index = i
            i += 1

    def editar_elemento(self, instance):
        elemento = instance.parent
        i = elemento.index
        if instance.text == 'Editar' and self.editando == False:
            self.parent.parent.parent.parent.listo_para_guardar = False
            instance.text = 'Aceptar'
            self.editando = True
        #Salva el texto
            PP_text = elemento.lbl_PP.text
            SP_text = elemento.lbl_SP.text
            pista_text = elemento.lbl_pista.text
        #Elimina los labels
            elemento.remove_widget(elemento.lbl_PP)
            elemento.remove_widget(elemento.lbl_SP)
            elemento.remove_widget(elemento.lbl_pista)
        #Crea los inputs
            elemento.PP_input = TextInput(multiline=False, halign='center', text=PP_text, size_hint=(0.1,1), font_name=self.FUENTE, font_size=self.ALT_FUENTE, write_tab = False, on_text_validate=self.editar_elemento)
            elemento.add_widget(elemento.PP_input, index = 2)
            elemento.SP_input = TextInput(multiline=False, halign='center', text=SP_text, size_hint=(0.1,1), font_name=self.FUENTE, font_size=self.ALT_FUENTE, write_tab = False, on_text_validate=self.editar_elemento)
            elemento.add_widget(elemento.SP_input, index = 2)
            elemento.pista_input = TextInput(multiline=False, size_hint=(1,1), text=pista_text, font_name=self.FUENTE, font_size=self.ALT_FUENTE, write_tab = False, on_text_validate=self.editar_elemento)
            elemento.add_widget(elemento.pista_input, index = 2)
        elif instance.parent.editar.text == 'Aceptar' and self.editando == True:
        #Salva el texto
            PP_text = elemento.PP_input.text
            SP_text = elemento.SP_input.text
            pista_text = elemento.pista_input.text
        #Prueba si hay espacios vacíos
            if PP_text != '' and SP_text != '' and pista_text != '':
                self.parent.parent.parent.parent.listo_para_guardar = True
                instance.parent.editar.text = 'Editar'
                self.editando = False
            #Elimina los inputs
                elemento.remove_widget(elemento.PP_input)
                elemento.remove_widget(elemento.SP_input)
                elemento.remove_widget(elemento.pista_input)
            #Crea los labels
                elemento.lbl_PP.text = PP_text.upper()
                elemento.lbl_SP.text = SP_text.upper()
                elemento.lbl_pista.text = pista_text
                elemento.add_widget(elemento.lbl_PP, index = 2)
                elemento.add_widget(elemento.lbl_SP, index = 2)
                elemento.add_widget(elemento.lbl_pista, index = 2)

if __name__ == '__main__':
    Window.size = (860, 540)
    Window.left = 200
    Window.top = 140

    ruta_niveles = 'cr_files/niveles.txt'
    lista_niveles = obtener_lista_niveles(ruta_niveles)
    print(lista_niveles)
    print(lista_niveles[0])

    class MainApp(App):
        def build(self):
            return EditorNiveles(nivel=lista_niveles[5])

    MainApp().run()


