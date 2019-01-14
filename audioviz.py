#!/usr/bin/env python3
"""
An attempt at audio visualizations on a LED matrix via GPIO.
"""
import sys
import io
import wave
import traceback
import threading
import argparse

import pyaudio
import numpy as np
import audioread

# RPI/GPIO libs - if not found, use fallback console output
try:
    from rpi_ws281x import PixelStrip
    from simplegrid import *
except ImportError:
    PixelStrip = None

# hexcolor terminal_output.py from https://github.com/shypre/rpi-light-show (optional)
try:
    import terminal_output
except ImportError:
    terminal_output = None
    traceback.print_exc()

LED_INTENSITY = 25
BAR_COLOR = (255, 255, 255)  # TODO: make dynamic based on height
BG_COLOR = (0, 0, 0)

CHUNK = 2048
# FFT_SIZE_MULTIPLIER should always be >= 2 (Nyquist's theorem)
# FFT_SIZE_MULTIPLIER = 3 uses the first third of data (0 to ~14kHz)
FFT_SIZE_MULTIPLIER = 3

parser = argparse.ArgumentParser(description='Plays music and projects a visualization onto an LED matrix.')
parser.add_argument('filename', type=str, help='file to play')
parser.add_argument('boardsize', type=int, help='the width and height of the LED matrix')
parser.add_argument('gpionum', type=int, help='the target GPIO pin')
parser.add_argument('--verbose', '-v', action='store_true', help='enables verbose output')
args = parser.parse_args()

# XXX not a very rigorous check
if not args.filename.lower().endswith('.wav'):
    # Decode other formats to WAV first in memory
    print('Decoding to WAV - this will be much faster if you convert it yourself beforehand!')
    wavebuf = io.BytesIO()
    with audioread.audio_open(args.filename) as f:
        samplerate = f.samplerate
        waveobj = wave.open(wavebuf, 'wb')
        waveobj.setnchannels(f.channels)
        waveobj.setframerate(f.samplerate)
        waveobj.setsampwidth(2)

        for buf in f:
            waveobj.writeframes(buf)
        waveobj.close()
    wavebuf.seek(0)
else:
    wavebuf = open(args.filename, 'rb')

p = pyaudio.PyAudio()
waveread = wave.open(wavebuf, 'rb')
stream = p.open(format=pyaudio.paInt16,
                channels=waveread.getnchannels(),
                rate=waveread.getframerate(),
                output=True)

my_grid = None
if PixelStrip:  # Init ws281x stuff if found
    pixelstrip = PixelStrip(args.boardsize**2, args.gpionum, brightness=LED_INTENSITY)
    pixelstrip.begin()
    my_grid = led_grid.LEDGrid(pixelstrip, grid.SerpentinePattern.TOP_RIGHT, args.boardsize, args.boardsize, default_value=BG_COLOR)

# Dump the frequency table for reference
freqtable = np.fft.fftfreq(args.boardsize*FFT_SIZE_MULTIPLIER, d=1/waveread.getframerate())
print("Bars on the visualizer will correspond to these frequency bins:")
for freq in freqtable[:int(len(freqtable)/FFT_SIZE_MULTIPLIER)]:
    print(freq, "Hz")

input("OK ready, press Enter to continue")
while True:
    data = waveread.readframes(CHUNK)
    if not data:
        break
    np_arr = np.frombuffer(data, dtype=np.int16)
    fft = np.fft.fft(np_arr, n=args.boardsize*FFT_SIZE_MULTIPLIER)
    # With fft the second half of the data does not map to a physical quantity (negative frequencies in freqtable),
    # so we always cut off at least half the data
    fft = fft[:int(len(fft)/FFT_SIZE_MULTIPLIER)]
    fft = np.abs(fft)

    median = np.median(fft)
    for x, value in enumerate(fft):
        if value > 0:
            # XXX need a better algorithm
            num_bars = int((np.log(value) / args.boardsize) ** 2 * args.boardsize)
        else:
            num_bars = 0

        # RPI/ GPIO specific stuff
        if PixelStrip:
            # Draw the bars left to right, bottom to top
            y = args.boardsize-1
            while y > 0:
                if num_bars > 0:
                    my_grid.set(x, y, BAR_COLOR, allowOverwrite=True)
                    num_bars -= 1
                else:
                    my_grid.set(x, y, BG_COLOR, allowOverwrite=True)
                y -= 1
            pixelstrip.show()
        else:
            # Fallback mode is just #'s
            print('#' * num_bars)

    if terminal_output and my_grid:
        terminal_output.print_led_grid(my_grid)

    stream.write(data)

print('Done')
stream.stop_stream()
stream.close()
p.terminate()
