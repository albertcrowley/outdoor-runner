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

# from game_utils import params
# from game_utils import Sprite
# from game_utils import SpriteAtlas
# from game_utils import Background
# from game_utils import Blank

import math
from random import randint

# kivy.require('1.10.0')

class Runner(App):
    def build(self):
        game = Widget()
        return game


if __name__ == '__main__':
    Runner().run()
