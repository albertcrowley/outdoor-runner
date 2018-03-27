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
from kivy.uix.button import Button
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

class Obstacles():
    def __init__(self):
        self.rocks = []
        self.ticks_with_no_rocks = 0
        self.vx = -360
        self.vy = 0

    def addrock(self):
        sprite = Sprite(source='rock.png')
        sprite.pos = (1000,0)
        self.rocks.append(sprite)
        App.get_running_app().root.add_widget(sprite)

    def update(self, dt):
        player = App.get_running_app().game.player
        for sprite in self.rocks:
            sprite.x += self.vx * dt
            sprite.y += self.vy * dt
            if sprite.x < -50:
                App.get_running_app().root.remove_widget(sprite)
            if sprite.collide_widget(player):
                App.get_running_app().game.gameOver()


        self.ticks_with_no_rocks += 1
        if self.ticks_with_no_rocks > 60:
            rand = randint(1, 100)
            if rand < 3:
                self.addrock()
                self.ticks_with_no_rocks = 0



class Player(Sprite):

    def __init__(self, pos):
        self.images = SpriteAtlas('RUN.atlas')
        super(Player, self).__init__(texture=self.images['1'], pos=pos)
        self.velocity_y = 0
        self.gravity = -900;
        self.tick = 1.0/60.0
        self.ticks = 0;
        self.height *= 2
        self.width *= 2

    def update(self, dt):
        self.ticks += 1
        if self.y < 0:
            self.velocity_y = 0
            self.y = -0.1
        else:
            self.velocity_y += self.gravity * dt
            self.velocity_y = max(self.velocity_y, -600)
            self.y += self.velocity_y * dt
        frame = int(math.floor( self.ticks / 10)) % 8
        self.texture = self.images[str(frame)]

    def jump(self):
        if self.y < 0:
            self.velocity_y = 400;
            self.y = 1


class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source=source)
        self.add_widget(self.image)
        self.size = self.image.size
        self.image_dupe = Sprite(source=source, x=self.width)
        self.add_widget(self.image_dupe)
        self.speed = 4;
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
        self.obstacles = Obstacles()

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.game_running = False

    def setGameState(self, state):
        self.game_running = state

    def update(self, dt):
        if self.game_running:
            self.background.update(dt=dt)
            self.player.update(dt=dt)
            self.obstacles.update(dt=dt)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'spacebar':
            self.player.jump()
        return True

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def gameOver(self):
        self.game_over = True
        self.setGameState(False)


class ScreenMan(Widget):
    def __init__(self):
        super(ScreenMan,self).__init__()


class Menu(Widget):
    def __init__(self):
        super(Menu,self).__init__()
        self.back = Sprite(source='background.png')
        self.add_widget(self.back)

        start_button = Button(text='Start')
        self.add_widget(start_button)

    def start(self):
        app = App.get_running_app()
        app.start()
        App.get_running_app().game.setGameState(True)



class Runner(App):
    def build(self):
        self.menu = Menu()
        self.sm = ScreenMan()
        self.sm.add_widget(self.menu)
        return self.sm

    def start(self):
        print ("starting")
        self.sm.clear_widgets()
        self.game = Game()
        self.sm.add_widget(self.game)



if __name__ == '__main__':
    Runner().run()
