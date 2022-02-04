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
        self.top_input.bind(focus=self.unfocus_top)
        self.add_widget(self.top_input)
    #Second row
        self.bottom_label = Label(text='Title of the Pop Up:')
        self.add_widget(self.bottom_label)
        self.bottom_input = MyTextInput(on_text_validate=self.create_popup)
        self.bottom_input.bind(focus=self.unfocus_bottom)
        self.add_widget(self.bottom_input)

    def unfocus_top(self, instance, value):
        if not value:   # DEFOCUSED
            self.change_top_label(instance)

    def unfocus_bottom(self, instance, value):
        if not value:   # DEFOCUSED
            self.create_popup(instance)

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


