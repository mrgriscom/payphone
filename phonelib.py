#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import threading

class Phone(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.up = True
        self.poll_interval = .01
        self.subscribers = []

        self.on_hook = None
        self.button_down = None
        self.last_button = None
        self.coin = None
        self.first_press = False

        self.PINS = [4, 17, 18, 23, 24, 25, 27]
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for p in self.PINS:
            GPIO.setup(p, GPIO.IN)
        GPIO.add_event_detect(27, GPIO.FALLING)

    def terminate(self):
        self.up = False

    def run(self):
        while self.up:
            self.update()
            time.sleep(self.poll_interval)
        GPIO.cleanup()

    def update(self):
        pins = self.poll_pins()
        on_hook = bool(pins[0])
        button_down = bool(pins[1])
        button_row = 2*pins[5] + pins[4]
        button_col = 2*pins[3] + pins[2]
        button = ['123', '456', '789', '*0#'][button_row][button_col]
        # for reference, coin mech wiring:
        # G = common
        # W = quarter
        # R = dime
        # B = nickel
        coin = not pins[6]

        if on_hook != self.on_hook:
            self.broadcast(lambda s: s.hook(on_hook))
        self.on_hook = on_hook

        def button_press_change(s):
            if button_down:
                self.first_press = True
                s.buttonDown(button)
            else:
                if not self.first_press:
                    # swallow phantom event on init
                    return
                s.buttonUp(button)
        if button_down != self.button_down:
            self.broadcast(button_press_change)
        elif button != self.last_button:
            assert button_down
            self.broadcast(lambda s: s.buttonUp(self.last_button))
            self.broadcast(lambda s: s.buttonDown(button))
        self.button_down = button_down
        self.last_button = button

        if coin != self.coin:
            if coin:
                # only quarters right now
                self.broadcast(lambda s: s.money(.25))
        self.coin = coin

    def poll_pins(self):
        pins = [GPIO.input(pin) for pin in self.PINS]
        # coin event is very short so we use the monitoring capability of the GPIO lib
        if GPIO.event_detected(27):
            pins[6] = 0
        return pins

    def cur_state(self):
        return {
            'on_hook': self.on_hook,
            'button_pressed': self.button_down,
            'last_button': self.last_button,
        }

    def broadcast(self, event):
        for s in self.subscribers:
            event(s)

    def subscribe(self, s):
        self.subscribers.append(s)

    def unsubscribe(self, s):
        self.subscribers.remove(s)

class PhoneListener(object):
    def hook(self, on):
        print 'hook:', on

    def buttonDown(self, n):
        print 'button pressed:', n

    def buttonUp(self, n):
        print 'button released:', n

    def money(self, amt):
        print 'money:', amt

if __name__ == "__main__":

    ph = Phone()
    ph.start()

    listener = PhoneListener()
    ph.subscribe(listener)

    try:
        while True:
            time.sleep(.01)
    except KeyboardInterrupt:
        ph.terminate()
