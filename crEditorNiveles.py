from archivo_exterior import obtener_lista_niveles, obtener_lista_palabras
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from color_label import ButtonBlue, ColorLabel, LabelLeft
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import *
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
''')

class EditorNiveles(BoxLayout):
    def __init__(self, nivel, **kwargs):
        super().__init__(**kwargs)
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
        self.nombre_nivel = nombre_nivel
        self.init_layout()

    def init_layout(self):
        self.btn_editar = Button(text='CAMBIAR', size_hint=(None, None), size=(20, 20), pos_hint={'right':.98, 'center_y':.5})
        self.btn_editar.bind(on_release=self.editar_nombre)
        self.add_widget(self.btn_editar)
        self.init_label()
    
    def editar_nombre(self, instance):
        if instance.text == 'CAMBIAR':
            self.nombre_nivel = self.lbl_nombre.text
            self.remove_widget(self.lbl_nombre)
            self.input = TextInput(text=self.nombre_nivel, hint_text='NOMBRE DEL NIVEL', size_hint=(1, 1))
            self.add_widget(self.input, index=1)
            instance.text = 'OK'
        elif instance.text == 'OK':
            self.nombre_nivel = self.input.text.upper()
            self.remove_widget(self.input)
            self.init_label()
            instance.text = 'CAMBIAR'

    def init_label(self):
        self.lbl_nombre = Label(text=self.nombre_nivel,size_hint=(1, 1))            #, pos_hint={'center_x':.5, 'center_y':.5}
        self.add_widget(self.lbl_nombre, index=1)

class BotonesEditor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding=5
        self.spacing=5
        self.size_hint=(1, None)
        self.height=40
        btn_cancelar = Button(text='Cancelar', on_release=self.cancelar)
        #btn_cancelar.bind(on_release=self.cancelar)
        self.add_widget(btn_cancelar)
        btn_guardar = Button(text='Guardar',on_release=self.guardar)
        #btn_guardar.bind(on_release=self.guardar)
        self.add_widget(btn_guardar)
    
    def cancelar(self, instance):
        #self.parent.remove_widget(menu)
        #del instance.parent
        self.parent.parent.remove_widget(self.parent)

    def guardar(self, instance):
        pass

class TabsEditor(TabbedPanel):
    def __init__(self, nivel, **kwargs):
        super().__init__(**kwargs)
        self.default_tab_text = 'AGREGAR RONDA'
        self.default_tab_content = Label(size_hint=(1, 1),)
        self.do_default_tab = False
        self.tab_ronda_1 = TabbedPanelHeader(text=nivel[1])
        self.tab_ronda_1.content = Scroller(lista=obtener_lista_palabras('cr_files/niveles.txt',nivel[1]))
        self.add_widget(self.tab_ronda_1)
        self.tab_ronda_2 = TabbedPanelHeader(text=nivel[2])
        self.tab_ronda_2.content = Scroller(lista=obtener_lista_palabras('cr_files/niveles.txt',nivel[2]))
        self.add_widget(self.tab_ronda_2)

class Scroller(ScrollView):
    def __init__(self, lista=[], **kwargs):
        super(Scroller, self).__init__(**kwargs)
        self.lista = lista
        hijo = ListBox(self.lista)
        hijo.size_hint = (1, None)
        hijo.height = hijo.minimum_height
        self.add_widget(hijo)

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
        self.enter_register.PP_input = TextInput(multiline=False, size_hint=(0.1,1), font_name=self.FUENTE, font_size=self.ALT_FUENTE)
        self.enter_register.add_widget(self.enter_register.PP_input)
        self.enter_register.SP_input = TextInput(multiline=False, size_hint=(0.1,1), font_name=self.FUENTE, font_size=self.ALT_FUENTE)
        self.enter_register.add_widget(self.enter_register.SP_input)
        self.enter_register.pista_input = TextInput(font_name=self.font, font_size=self.ALT_FUENTE)
        self.enter_register.add_widget(self.enter_register.pista_input)
        self.enter_register.agregar = Button(text='Añadir', size_hint=(None,1), width=100, font_name=self.FUENTE, font_size=self.ALT_FUENTE)
        self.enter_register.agregar.bind(on_release=self.agregar_entrada)
        self.enter_register.add_widget(self.enter_register.agregar)
        self.add_widget(self.enter_register)
        self.size_hint = (1, None)
        self.bind(minimum_height = self.setter('height'))

    def agregar_entrada(self, instance):
        PP = self.enter_register.PP_input.text.upper()
        SP = self.enter_register.SP_input.text.upper()
        pista = self.enter_register.pista_input.text
        if PP == '' or SP == '' or pista == '':
            pass
        else:
            i = len(self.elementos)
            self.crear_elemento(i, PP, SP, pista)
            self.add_widget(self.elementos[i], index=1)
            self.enter_register.PP_input.text = ''
            self.enter_register.SP_input.text = ''
            self.enter_register.pista_input.text = ''

    def crear_elemento(self, i, textPP, textSP, textPista):
        self.elementos.append(BoxLayout(padding=5, spacing=5, size_hint=(1, None), height=50))
        self.elementos[i].index = i
        self.elementos[i].lbl_PP = Label(text=textPP, size_hint=(0.1,1), font_name=self.FUENTE, font_size=self.ALT_FUENTE, bold=True)
        self.elementos[i].add_widget(self.elementos[i].lbl_PP)
        self.elementos[i].lbl_SP = Label(text=textSP, size_hint=(0.1,1), font_name=self.FUENTE, font_size=self.ALT_FUENTE, bold=True)
        self.elementos[i].add_widget(self.elementos[i].lbl_SP)
        self.elementos[i].lbl_pista = LabelLeft(text=textPista, halign = 'left', valign = 'middle',  font_name=self.FUENTE, font_size=self.ALT_FUENTE)
        self.elementos[i].add_widget(self.elementos[i].lbl_pista)
        self.elementos[i].editar = Button(text='Editar', font_size=self.ALT_FUENTE, size_hint=(None, None), size=(60, 35), font_name=self.FUENTE)
        self.elementos[i].editar.bind(on_release=self.editar_elemento)
        self.elementos[i].add_widget(self.elementos[i].editar)
        self.elementos[i].borrar = Button(text='X', size_hint=(None, None), size=(35, 35), font_size=self.ALT_FUENTE, font_name=self.FUENTE)
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
            elemento.PP_input = TextInput(multiline=False, halign='center', text=PP_text, size_hint=(0.1,.6), font_name=self.FUENTE, font_size=self.ALT_FUENTE)
            elemento.add_widget(elemento.PP_input, index = 2)
            elemento.SP_input = TextInput(multiline=False, halign='center', text=SP_text, size_hint=(0.1,.6), font_name=self.FUENTE, font_size=self.ALT_FUENTE)
            elemento.add_widget(elemento.SP_input, index = 2)
            elemento.pista_input = TextInput(multiline=False, size_hint=(1,.6), text=pista_text, font_name=self.FUENTE, font_size=self.ALT_FUENTE)
            elemento.add_widget(elemento.pista_input, index = 2)
        elif instance.text == 'Aceptar' and self.editando == True:
            instance.text = 'Editar'
            self.editando = False
        #Salva el texto
            PP_text = elemento.PP_input.text
            SP_text = elemento.SP_input.text
            pista_text = elemento.pista_input.text
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

    nombre = 'mujeres'
    ruta_niveles = 'cr_files/niveles.txt'
    lista_palabras = obtener_lista_palabras(ruta_niveles, nombre)
    lista_niveles = obtener_lista_niveles(ruta_niveles)
    print(lista_niveles)
    print(lista_niveles[0])

    class MainApp(App):
        def build(self):
            return EditorNiveles(nivel=lista_niveles[0])

    MainApp().run()


