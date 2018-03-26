#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.image import Image

# from game_utils import params
# from game_utils import Sprite
# from game_utils import SpriteAtlas
# from game_utils import Background
# from game_utils import Blank

import math
from random import randint

class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(allow_stretch=True, **kwargs)
        self.size = (self.texture.width, self.texture.height)
        self.texture.mag_filter = 'nearest'


class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.background = Sprite(source="background.png", pos=(0,0))
        self.background.pos = (0,0)
        self.add_widget(self.background)

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        print ("done")


    def update(self, dt):
        pass






class Runner(App):
    def build(self):
        game = Game()
        return game


if __name__ == '__main__':
    Runner().run()
