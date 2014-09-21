from phonelib import *
from subprocess import Popen, PIPE
import sys

class SIPClientListener(PhoneEventHandler):
    def __init__(self):
        self.p = Popen('twinkle -c', shell=True, stdin=PIPE)

    def cmd(self, s):
        print '>>', s
        self.p.stdin.write(s + '\n')

    def hook(self, on):
        if not on:
            self.cmd('call %s' % sys.argv[1])
        else:
            self.cmd('bye')

    def buttonDown(self, n):
        self.cmd('dtmf %s' % n)

    def money(self, amt):
        assert amt == .25
        self.cmd('dtmf -r a')



if __name__ == "__main__":

    ph = Phone()
    ph.start()
    ph.subscribe(DTMFEcho(False))

    listener = SIPClientListener()
    ph.subscribe(listener)

    try:
        while True:
            time.sleep(.01)
    except KeyboardInterrupt:
        pass

    ph.terminate()
