#!/usr/bin/env python
# encoding: utf-8

import urwid
import sys
from dump import serialize
from timer import Timer

class UserInterrupt(Exception):
    pass

def unhandled_input(key):
    if key in ('q', 'Q'):
        raise UserInterrupt

def update_timer(loop, timer):
    if not timer.started:
        return
    if timer.update():
        loop.set_alarm_in(0.1, update_timer, timer)

def start_update_timer(timer, loop):
    update_timer(loop, timer)

def end_timer(timer, loop):
    raise urwid.ExitMainLoop

def run(timer):
    timer_pad = urwid.Padding(timer, align='center', width='clip')
    timer_fill = urwid.Filler(timer_pad)
    loop = urwid.MainLoop(timer_fill, unhandled_input=unhandled_input)
    urwid.connect_signal(timer, 'started', start_update_timer, loop)
    urwid.connect_signal(timer, 'ended', end_timer, loop)
    loop.run()

def main():
    try:
        # Se ejecuta el cronómetro
        timer = Timer()
        run(timer)
    except urwid.ExitMainLoop:
        # Salida por finalización del programa
        print('Fin del MainLoop')
    except UserInterrupt:
        # Salida estándar con la tecla 'Q'
        print("Detenido por el usuario")
        print("Tiempo restante:", timer.format_text(timer.remaining))
    except KeyboardInterrupt:
        # Salida por interrupción de teclado (CTRL+C)
        print("Detenido por el teclado")
        print("Tiempo restante:", timer.format_text(timer.remaining))
    finally:
        # Pase lo que pase, se crea una copia del valor del tiempo
        # para reanudar su ejecución en caso de que falle
        serialize('time', timer.remaining)

if __name__ == '__main__':
    sys.exit(main())
