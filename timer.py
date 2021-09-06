#!/usr/bin/env python
# encoding: utf-8

import time
import urwid
import math
from dump import deserialize

DEFAULT_TIME = 5*60

class Timer(urwid.BigText):
    signals = ['started', 'ended']
    _selectable = True
    # Se deserializa la variable de tiempo para conocer con que valor terminó
    # en la ejecución anterior
    def __init__(self, 
            t=deserialize('time', DEFAULT_TIME), 
            font=None, 
            no_ds=False, 
            no_title=False
        ):
        self.started = False
        self.t = t # Valor del tiempo de inicio del cronómetro
        self._remaining = t # Valor del tiempo restante
        self._elapsed = 0 # Valor del tiempo transcurrido
        self.no_ds = no_ds
        self.no_title = no_title
        self.set_text(self.format_text(t))
        if not font:
            self.font = urwid.HalfBlock6x5Font()
        self.__super.__init__(self.get_text()[0], self.font)

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, t):
        self._t = t

    @property
    def elapsed(self):
        return self._elapsed

    @elapsed.setter
    def elapsed(self, elapsed):
        self._elapsed = elapsed
    
    @property
    def remaining(self):
        return self._remaining
    
    @remaining.setter
    def remaining(self, remaining):
        self._remaining = remaining

    def to_hms(self, ss):
        hh = ss // 3600
        ss -= hh * 3600
        mm = ss // 60
        ss = (ss - mm * 60) * 10 / 10.0
        return hh, mm, ss

    def format_text(self, ss):
        fmt = '%02d:%02d:%02d' if self.no_ds else '%02d:%02d:%04.1f'
        return fmt % self.to_hms(ss)

    def start_pause(self):
        if self.started:
            self.t -= time.time() - self._started
            self.started = False
            self._emit('paused')
        else:
            self._started = time.time()
            self.started = True
            self._emit('started')

    def update(self):
        if self.started:
            self._elapsed = elapsed = time.time() - self._started
            self._remaining = self.t - elapsed
            if self.no_ds:
                self._remaining = math.ceil(self._remaining)
            if self._remaining <= 0:
                self.started = False
                self._remaining = 0
            self.set_text(self.format_text(self._remaining))
            if self._remaining:
                return True
            else:
                self._emit('ended')
    
    def set_text(self, text):
        super(Timer, self).set_text(text)
        if not self.no_title:
            print('\33]2;%s\007' % text, end='')

    def keypress(self, size, key):
        if key in ('up', '+'):
            self.t += 1;
        elif key in ('down', '-'):
            self.t -= 1;
        elif key in (' ', 'p', 'P'):
            self.start_pause()
        else:
            return key
        if not self.started:
            self.set_text(self.format_text(self.t))
        self._remaining = self.t

    def mouse_event(self, size, event, button, col, row, focus):
        p = self.pack()
        d = col < p[0] and row < p[1]
        if event == 'mouse press' and d:
            if button == 1:
                self.start_pause()
            if button == 4:
                self.t += 1
            if button == 5:
                self.t -= 1
        if not self.started:
            self.set_text(self.format_text(self.t))
        else:
            return False
        self._remaining = self.t