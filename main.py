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
from kivy.atlas import Atlas, Logger
import os
import json
from os.path import dirname, join
from kivy.core.image import Image as CoreImage


import math
from random import randint

class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(allow_stretch=True, **kwargs)
        self.size = (self.texture.width, self.texture.height)
        self.texture.mag_filter = 'nearest'


class SpriteAtlas(Atlas):
    def _load(self):
        # must be a name finished by .atlas ?
        filename = self._filename
        assert(filename.endswith('.atlas'))
        filename = filename.replace('/', os.sep)

        Logger.debug('Atlas: Load <%s>' % filename)
        with open(filename, 'r') as fd:
            meta = json.load(fd)

        Logger.debug('Atlas: Need to load %d images' % len(meta))
        d = dirname(filename)
        textures = {}
        for subfilename, ids in meta.items():
            subfilename = join(d, subfilename)
            Logger.debug('Atlas: Load <%s>' % subfilename)

            # load the image
            ci = CoreImage(subfilename)

            # <RJ> this is the fix for pixel art
            ci.texture.mag_filter = 'nearest'

            # for all the uid, load the image, get the region, and put
            # it in our dict.
            for meta_id, meta_coords in ids.items():
                x, y, w, h = meta_coords
                textures[meta_id] = ci.texture.get_region(*meta_coords)

        self.textures = textures


class Player(Sprite):

    def __init__(self, pos):
        self.images = SpriteAtlas('RUN.atlas')
        super(Player, self).__init__(texture=self.images['1'], pos=pos)
        self.tick = 1.0/60.0
        self.ticks = 0;
        self.height *= 2
        self.width *= 2

    def update(self, dt):
        self.ticks += 1
        frame = int(math.floor( self.ticks / 10)) % 8
        self.texture = self.images[str(frame)]



class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source=source)
        self.add_widget(self.image)
        self.size = self.image.size
        self.image_dupe = Sprite(source=source, x=self.width)
        self.add_widget(self.image_dupe)
        self.speed = 3;
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
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.background = Background(source="background.png")
        self.add_widget(self.background)
        self.player = Player(pos=(100,-0.1))
        self.add_widget(self.player)


    def update(self, dt):
        self.background.update(dt=dt)
        self.player.update(dt=dt)






class Runner(App):
    def build(self):
        game = Game()
        return game


if __name__ == '__main__':
    Runner().run()
