from phonelib import *
from subprocess import Popen, PIPE
import sys

class SIPClient(PhoneEventHandler):
    def __init__(self, callout_ext=None):
        self.p = Popen(['twinkle', '-c'], stdin=PIPE, stdout=PIPE)
        self.reader = SIPClientListener(self)
        self.reader.start()

        self.callout_ext = callout_ext
        self.on_call = False
        self.incoming_from = None

    def cmd(self, s):
        print '>>', s
        self.p.stdin.write(s + '\n')

    def hook(self, on):
        if not on:
            if self.incoming_from:
                self.cmd('answer')
                self.incoming(None)
            else:
                self.cmd('call %s' % (self.callout_ext or ''))
            self.on_call = True
        else:
            self.cmd('bye')
            self.on_call = False

    def buttonDown(self, n):
        self.cmd('dtmf %s' % n)

    def money(self, amt):
        assert amt == .25
        self.cmd('dtmf -r a')

    def terminate(self):
        self.p.kill()

    def incoming(self, caller):
        if caller:
            self.ringer_start()
        else:
            self.ringer_stop()
        self.incoming_from = caller

    def ringer_start(self, type=None):
        print '**RING RING**'

    def ringer_stop(self):
        print '--silence--'        

    def on_output(self, ln):
        print '<<', ln
        if ln.startswith('Line 1:'):
            action = ln[len('Line 1:'):].strip()
            if action == 'incoming call':
                self.incoming_from = '_pending'
            elif action in ('far end cancelled call', 'answer timeout.'):
                self.incoming(None)
        elif ln.startswith('From:') and self.incoming_from == 'pending':
            caller = ln[len('From:'):].strip()
            self.incoming(caller)

class SIPClientListener(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        while True:
            ln = self.client.p.stdout.readline()
            if not ln:
                return
            ln = ln.strip()
            if ln:
                self.client.on_output(ln)


if __name__ == "__main__":

    try:
        callout_ext = sys.argv[1]
    except IndexError:
        raise Exception('callout # required')
        #callout_ext = None

    ph = Phone()
    ph.start()
    ph.subscribe(DTMFEcho(False))

    voip = SIPClient(callout_ext)
    ph.subscribe(voip)

    try:
        while True:
            time.sleep(.01)
    except KeyboardInterrupt:
        pass

    for e in [ph, voip]:
        e.terminate()

    
