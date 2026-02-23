from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivy.lang import Builder

KV = '''
MDScreen:
    MDIconButton:
        icon: "plus"
        pos_hint: {"center_x": .5, "center_y": .5}
        icon_size: "64sp"
'''

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

MainApp().run()