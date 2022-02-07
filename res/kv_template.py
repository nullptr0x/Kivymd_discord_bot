kivy = '''
```py
from kivy.app import App
from kivy.lang import Builder


KV = \'\'\'
\'\'\'


class MyApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    MyApp().run()  
```
'''

kivymd = '''
```py
from kivymd.app import MDApp
from kivy.lang import Builder


KV = \'\'\'
\'\'\'


class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    MyApp().run()
```
'''
