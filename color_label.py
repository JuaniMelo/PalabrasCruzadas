from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout

Builder.load_string('''
<ColorLabel>:
    bg_color: (0,0,0,1)
    canvas.before:
        Color:
            rgba: self.bg_color
        Rectangle:
            pos: self.pos
            size: self.size
<BoxColor>:
    bg_color: (0,0,0,1)
    canvas.before:
        Color:
            rgba: self.bg_color
        Rectangle:
            pos: self.pos
            size: self.size
<BoxImage>:
    source: self.source
    canvas.before:
        Rectangle:
            source: self.source
            pos: self.pos
            size: self.size
<ImageLabel>:
    source: self.source
    canvas.before:
        Rectangle:
            source: self.source
            pos: self.pos
            size: self.size
''')

class BoxColor(RelativeLayout):
    def __init__(self, color=[0, 0, 0, 1], **kwargs):
        super().__init__(**kwargs)
        self.bg_color = color

class BgImage(RelativeLayout):
    def __init__(self, source=None, **kwargs):
        super().__init__(**kwargs)
        self.source = source

class ColorLabel(Label):
    def __init__(self, color=[0, 0, 0, 1], **kwargs):
        super().__init__(**kwargs)
        self.bg_color = color

class ImageLabel(Label):
    def __init__(self, source=None, **kwargs):
        super().__init__(**kwargs)
        self.source = source

class ButtonOrange(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = 'images/botones/btn2_orange_normal.png'
        self.background_down = 'images/botones/btn2_orange_down.png'
        self.background_disabled_normal = 'images/botones/btn2_orange_disabled_normal.png'
        self.background_disabled_down = 'images/botones/btn2_orange_disabled_down.png'

class ButtonGreen(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = 'images/botones/btn2_green_normal.png'
        self.background_down = 'images/botones/btn2_green_down.png'
        self.background_disabled_normal = 'images/botones/btn2_green_disabled_normal.png'
        self.background_disabled_down = 'images/botones/btn2_green_disabled_down.png'

class ButtonMagenta(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = 'images/botones/btn2_magenta_normal.png'
        self.background_down = 'images/botones/btn2_magenta_down.png'
        self.background_disabled_normal = 'images/botones/btn2_magenta_disabled_normal.png'
        self.background_disabled_down = 'images/botones/btn2_magenta_disabled_down.png'

class ButtonRed(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = 'images/botones/btn2_red_normal.png'
        self.background_down = 'images/botones/btn2_red_down.png'
        self.background_disabled_normal = 'images/botones/btn2_red_disabled_normal.png'
        self.background_disabled_down = 'images/botones/btn2_red_disabled_down.png'

class ButtonBlue(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = 'images/botones/btn2_blue_normal.png'
        self.background_down = 'images/botones/btn2_blue_down.png'
        self.background_disabled_normal = 'images/botones/btn2_blue_disabled_normal.png'
        self.background_disabled_down = 'images/botones/btn2_blue_disabled_down.png'

class LabelLeft(Label):
   def on_size(self, *args):
      self.text_size = self.size