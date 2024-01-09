'''
copied from LordTony's youtube video: https://www.youtube.com/watch?v=FkNkOVj7suo
'''

import cv2
from PIL import Image
import os

mp4 = 'assets/badapple.mp4'

video_capture = cv2.VideoCapture(mp4)

still_playing = True
while still_playing:
    still_playing, frame = video_capture.read()
    img_pil = Image.fromarray(frame)
    width, height = img_pil.size

    buffer = ''
    for y in range(0, height, 4):
        for x in range(0, width, 2):
            r, g, b = img_pil.getpixel((x, y))
            grey = (r + g + b) / 3
            buffer += '#' if grey > 128 else ' '
        buffer += '\n'
    
    os.system(f'tput cup 0 0')
    print(buffer)

    # os.system('clear')
    # print(buffer)
    

os.system('clear')
print('Playback ended')