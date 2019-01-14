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
import time

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
BG_COLOR = (0, 0, 0)
DELAY = 0.02

# Adapted from https://bsou.io/posts/color-gradients-with-python
def linear_gradient(start, end, n):
    """Returns a gradient list of n colors between RGB tuples start and end."""
    # Initilize a list of the output colors with the starting color
    RGB_list = [start]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = tuple(int(start[j] + (float(t)/(n-1))*(end[j]-start[j])) for j in range(3))
        # Add it to our list of output colors
        RGB_list.append(curr_vector)
    return RGB_list

CHUNK = 2048
# FFT_SIZE_MULTIPLIER should always be >= 2 (Nyquist's theorem)
# FFT_SIZE_MULTIPLIER = 3 uses the first third of data (0 to ~14kHz)
FFT_SIZE_MULTIPLIER = 2

parser = argparse.ArgumentParser(description='Plays music and projects a visualization onto an LED matrix.')
parser.add_argument('filename', type=str, help='file to play')
parser.add_argument('boardsize', type=int, help='the width and height of the LED matrix')
parser.add_argument('gpionum', type=int, help='the target GPIO pin')
parser.add_argument('--verbose', '-v', action='store_true', help='enables verbose output')
parser.add_argument('--top-color', '-tc', type=str, default='255,255,255')
parser.add_argument('--bottom-color', '-bc', type=str, default='255,255,255')
args = parser.parse_args()

# Convert from "255,255,255" etc. to (255, 255, 255)
start_color = tuple(map(int, args.top_color.split(',')))
end_color = tuple(map(int, args.bottom_color.split(',')))
assert len(start_color) == 3
assert len(end_color) == 3

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

next_data = None
next_data_lock = threading.Lock()   # only one thread can read/write next_data
next_data_ready = threading.Event() # set when next_data is ready
want_next_data = threading.Event()  # set when do_fft has finished drawing + a small delay

def do_fft():
    while True:
        next_data_lock.acquire()
        if next_data is None:
            print('Waiting for fft data (initial)')
            next_data_lock.release()
            next_data_ready.wait()
            next_data_lock.acquire()

        print('reading next_data')
        np_arr = np.frombuffer(next_data, dtype=np.int16)
        fft = np.fft.fft(np_arr, n=args.boardsize*2)
        fft = fft[:int(len(fft)/(FFT_SIZE_MULTIPLIER))]  # use first half of data
        fft = np.abs(fft)
        for x, value in enumerate(fft):
            print('On x=%s, value=%s' % (x, value))
            if value > 0:
                # XXX need a better algorithm
                num_bars = int((np.log(value) / args.boardsize) ** 2 * args.boardsize)
            else:
                num_bars = 0
            #print('num_bars=%s' % num_bars)

            # RPI/ GPIO specific stuff
            if PixelStrip:
                y = args.boardsize-1
                # Use a gradient for color unless start and end are the same
                if start_color != end_color:
                    bar_colors = linear_gradient(start_color, end_color, (num_bars+1))
                else:
                    bar_colors = [start_color] * (num_bars+1)
                while y > 0:
                    #print('Setting grid (%s, %s)' % (x, y))
                    if num_bars > 0:
                        #print('Setting (%s, %s) to %s' % (x, y, str(BAR_COLOR)))
                        my_grid.set(x, y, bar_colors[num_bars], allowOverwrite=True)
                        num_bars -= 1
                    else:
                        #print('Setting (%s, %s) to %s' % (x, y, str(BG_COLOR)))
                        my_grid.set(x, y, BG_COLOR, allowOverwrite=True)
                    y -= 1
                pixelstrip.show()
            else:
                print('#' * num_bars)
        time.sleep(DELAY)
        next_data_ready.clear()
        print('Done drawing bars')
        next_data_lock.release()
        want_next_data.set()

        #if terminal_output and my_grid:
        #    terminal_output.print_led_grid(my_grid)

        print('Waiting for fft data')
        next_data_ready.wait()

fft_thread = threading.Thread(target=do_fft, daemon=True).start()

want_next_data.set()

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

    if want_next_data.is_set():
        with next_data_lock:
            next_data = data
            #print('Sending in new data', next_data)
            print('Sending in new data')
            want_next_data.clear()
            next_data_ready.set()

    stream.write(data)

print('Done')
stream.stop_stream()
stream.close()
p.terminate()
