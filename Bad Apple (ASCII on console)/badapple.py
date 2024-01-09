'''
Version 3 of my Bad Apple program
Bad Apple but in ASCII on console

Written from scratch after learning the theory behind "Bad Apple Programs" from:
- CalvinLoke's touhou_bad_apple_v4.0.py, Github: https://github.com/CalvinLoke/bad-apple
- LordTony's youtube video: https://www.youtube.com/watch?v=FkNkOVj7suo

mp4 and mp3 sourced from Bad Apple Youtube video: https://www.youtube.com/watch?v=FtutLA63Cp8
'''
import cv2
from PIL import Image
import os
import playsound
import fpstimer
import time
from inputvalidation import get_int

# Raw Video Stats
mp4 = 'assets/badapple.mp4'
mp3 = 'assets/badapple.mp3'
raw_video_width, raw_video_height = 480, 360
fps = 30
total_frames = 6572

# Dimensions (characters) of each console frame (referred to as viewport for ease of use)
console_frame_width, console_frame_height = 160, 45

def main():
    prepare_start()

    play_audio(mp3)
    global start_time
    start_time = time.time()
    play_video(mp4)


def prepare_start():
    '''
    Prompts user to adjust their terminal window and zoom level to fit viewport
    '''
    while True:
        draw_viewport(console_frame_width, console_frame_height)
        print(f'Viewport width: {console_frame_width}, height: {console_frame_height} (in characters)')
        print('*** Adjust your terminal window size and zoom level to fit the viewport above ***')
        print('To customise viewport dimensions, enter "c"')
        confirmation = input('Enter anything else when ready: ')

        if confirmation == 'c':
            new_width = get_int(f'New width of viewport (in characters) (0-{raw_video_width}): ', min=0, max=raw_video_width)
            new_height = get_int(f'New height of viewport (in characters) (0-{int(raw_video_height/2)}): ', min=0, max=raw_video_height/2)
            resize_viewport(new_width, new_height)
            continue
        else:
            return


def draw_viewport(width, height):
    '''
    Prints out a (width by height) characters ASCII box to allow user to adjust their console
    zoom to fit the viewport for the video to play in the console
    '''
    os.system('clear')
    viewport = ''
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            # Top and bottom of viewport
            if y == 1 or y == height:
                if x == 1 or x == width:
                    viewport += '+'
                else:
                    viewport += '-'

            else:
                if x == 1 or x == width:
                    viewport += '|'
                else:
                    viewport += ' '

        viewport += '\n' if y != height else ''
    
    print(viewport)


def resize_viewport(new_width, new_height):
    '''
    Resizes the viewport
    i.e. the console frame width and height in characters
    '''
    global console_frame_width, console_frame_height
    console_frame_width = new_width
    console_frame_height = new_height


def get_ASCII(pixel):
    '''
    Reads a pixel object gotten from PIL.Image's get_pixel()
    Returns an ASCII character depending on the average rgb of the pixel
    '''
    r, g, b = pixel
    grey = (r + g + b) / 3

    # These values are arbitrary
    if grey > 250:
        return '@'
    elif 220 < grey <= 250:
        return '#'
    elif 128 < grey <= 220:
        return '+'
    elif 48 < grey <= 128:
        return '~'
    elif 16 < grey <= 48:
        return '-'
    elif 8 < grey <= 16:
        return '.'
    elif grey <= 8:
        return ' '
    else:
        print(f"A pixel's average rgb has registered as {grey}")
        raise ValueError


def play_video(path):
    '''
    Plays the ASCII Version of Bad Apple on the console
    '''
    print('Reading video file...')
    video_capture = cv2.VideoCapture(path)

    os.system('clear')

    # Testing
    frame_times = []

    # Use the fpstimer library to ensure the video runs at 30 fps
    timer = fpstimer.FPSTimer(fps)

    # Interval between pixels in raw video converted to ASCII
    x_interval = round(raw_video_width / console_frame_width)
    y_interval = round(raw_video_height / console_frame_height)

    for frame_number in range(1, total_frames + 1):
        success, raw_frame = video_capture.read()
        
        try:
            image = Image.fromarray(raw_frame)
        except AttributeError:
            break # if video.mp4 finishes unexpectedly early

        buffer = ''
        for y in range(0, raw_video_height, y_interval):
            for x in range(0, raw_video_width, x_interval):
                # Add an ASCII character to the console frame buffer according to its darkness
                buffer += get_ASCII(image.getpixel((x, y)))
            buffer += '\n'

        # Puts the cursor at terminal position 0, 0 (bottom left)
        os.system(f'tput cup 0 0')
        print(buffer)
    
        # Delays so as to maintain 30fps to match audio if CPU is able to render faster than 30 fps
        timer.sleep()

        if frame_number == 1800:
            os.system('clear')

            with open('frame_times.txt', 'w') as file:
                total_frame_time = 0
                total_constrained_time = 0
                content = ''
                for dict in frame_times:
                    total_frame_time += dict['frame_time']
                    total_constrained_time += dict['frame_time_constrained']
                    content += f'frame: {dict['frame_num']}, frame_time: {round(dict['frame_time'], 3)}s\n'
                content += f'\nTotal frames: {len(frame_times)}\n'
                content += f'Total time: {round(total_frame_time, 2)}s\n'
                content += f'Average fps: {round(len(frame_times)/total_frame_time, 1)}\n'
                content += f'\nConstrained Total time: {round(total_constrained_time, 2)}s\n'
                content += f'Constrained fps: {round(len(frame_times)/total_constrained_time, 1)}\n'
                file.write(content)
                
            print(f"Testing concluded, stats of {frame_number} frames recorded in frame_times.txt")
            quit()
    
    # End of video playback
    os.system('clear')
    print("--- Video played for %s seconds ---" % (time.time() - start_time))


def play_audio(path):
    '''
    Plays the badapple.mp3 audio
    '''
    playsound


if __name__ == '__main__':
    main()