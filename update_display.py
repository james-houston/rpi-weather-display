import time
import sys
from queue import Queue

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import time
from datetime import time as ti
from datetime import datetime

# Matrix size
size = 32, 64

update_interval_seconds = 10

def set_static_image(matrix, image_file):
    im = Image.open(image_file)
    matrix.SetImage(im.convert('RGB'), unsafe=False)

def display_gif(matrix, gif_image):
    frames = Image.open(gif_image)
    # Get gif frames
    frames.seek(0)
    timeout = time.time() + update_interval_seconds
    try:
        while True:
            if time.time() > timeout:
                break
            # Gif loop. Break out when update time occurs
            for frame in range(0, frames.n_frames):
                frames.seek(frame)
                matrix.SetImage(frames.convert('RGB'), 32, unsafe=False)
                time.sleep(.2)
    except Exception as e:
        # Rarely there is an error in updating the display. Usually it can be ignored and will be fixed on next iteration
        print(e)
        print("recovering display in 10 seconds...")
        time.sleep(10)


def update_display(gif_image, static_image, out_q):
    # Configuration matrix for the matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'regular'
    options.brightness = 25 # start at 25% brightness by default
    matrix = RGBMatrix(options = options)
    while True:
        try:
            b = out_q.get(block = False)
            print("got %d from queue" % b)
            #matrix = matrix_setup(b)
            matrix.brightness = b
        except Exception as e:
            # an empty queue is expected, we only want to take new values if there are any
            pass
        # Main display loop. Reopens image files each loop
        set_static_image(matrix, static_image)
        display_gif(matrix, gif_image)
