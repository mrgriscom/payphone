import os

freqs1 = [1209, 1336, 1477, 1633]
freqs2 = [697, 770, 852, 941]
buttons = ['123a', '456b', '789c', 's0pd']

def generate(filename, freqs, duration, bits=16, rate=44100, mono=True):
    cmd = 'sox -b %s -n %s rate %s synth %s %s channels %s' % (bits, filename, rate, duration, ' '.join('sine %s' % f for f in freqs), 1 if mono else 2)
    os.popen(cmd)

for col, f1 in enumerate(freqs1):
    for row, f2 in enumerate(freqs2):
        generate('audio/DTMF-%s.wav' % buttons[row][col], [f1, f2], 1., rate=22050)
