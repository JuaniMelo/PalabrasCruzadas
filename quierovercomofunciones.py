from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.app import App

class MyTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.unfocus_on_touch = True

    def on_focus(self, instance, value):
        if not value:   # DEFOCUSED
            print('Focus is off')

class MainLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
    #First row
        self.top_label = Label(text = 'No text')
        self.add_widget(self.top_label)
        self.top_input = MyTextInput(on_text_validate=self.change_top_label)
        self.top_input.bind(on_focus=self.top_input.on_text_validate)
        self.add_widget(self.top_input)
    #Second row
        self.bottom_label = Label(text='Bottom Label')
        self.add_widget(self.bottom_label)
        self.bottom_input = MyTextInput(on_text_validate=self.create_popup)
        self.bottom_input.bind(on_focus=self.bottom_input.on_text_validate)
        self.add_widget(self.bottom_input)

    def change_top_label(self, instance):
        self.top_label.text = instance.text
        instance.text = ''

    def create_popup(self, instance):
        self.my_popup = Popup(title=instance.text, size_hint=(.5, .5))
        self.my_popup.content = Button(text='CLOSE', on_release=self.my_popup.dismiss)
        self.my_popup.open()
        instance.text = ''

if __name__ == '__main__':
    class MainApp(App):
        def build(self):
            return MainLayout()
    MainApp().run()


