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

class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source=source)
        self.add_widget(self.image)
        self.size = self.image.size
        self.image_dupe = Sprite(source=source, x=self.width)
        self.add_widget(self.image_dupe)
        self.speed = 6;
        self.tick = 1.0/60.0

    def update(self, dt):
        self.image.x -= self.speed * (dt / self.tick)
        self.image_dupe.x -= self.speed * (dt / self.tick)
        if self.image.right <= 0:
            self.image.x = 0
            self.image_dupe.x = self.width


class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.background = Background(source="background.png")
        self.add_widget(self.background)

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        print ("done")


    def update(self, dt):
        self.background.update(dt=dt)






class Runner(App):
    def build(self):
        game = Game()
        return game


if __name__ == '__main__':
    Runner().run()
