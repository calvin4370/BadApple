import cv2
from PIL import Image
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Prevents pygame's welcome message
import pygame
from moviepy.editor import *
import fpstimer
import time
from inputvalidate import get_int, get_string

# Raw Video Stats (Default for bad apple, play_video() will adjust these values)
mp4 = 'badapple.mp4'
mp3 = 'badapple.mp3'
raw_video_width, raw_video_height = 480, 360
fps = 30
total_frames = 6572

# Dimensions (characters) of each console frame (referred to as viewport for ease of use)
console_frame_width, console_frame_height = 160, 45


def main():
    prepare_start()

    get_mp3(mp4)

    # For debug purposes to measure how long the ascii video played to calculated delay
    global before_audio_start_time, after_audio_start_time, show_debug_info_at_end
    show_debug_info_at_end = True

    # Start playing mp3 asynchronously (i.e. start mp3 then immediately start mp4)
    play_audio(mp3)
    play_video(mp4)

    if show_debug_info_at_end:
        show_debug_info()


def prepare_start():
    '''
    Prompts user to adjust their terminal window and zoom level to fit viewport
    '''
    while True:
        draw_viewport(console_frame_width, console_frame_height)
        print(f'Viewport width: {console_frame_width}, height: {console_frame_height} (in characters)')
        print('*** Adjust your terminal window size and zoom level to fit the viewport above ***')
        print('To customise viewport dimensions, enter "c". To change video, enter "v"')
        print('Resizing the box bigger while zoomed in may lead to the box misshaping, enter "r" to redraw the box with selected dimensions')
        confirmation = input('Enter anything else when ready: ')

        if confirmation.lower() == 'c':
            print('\nThe default 160 by 45 characters is safe for most systems to run, 320 by 75 is possible for good systems')
            print('Anything higher may lead to <30fps and audio syncing issues')
    
            new_width = get_int(f'New width of viewport (in characters) (0-{raw_video_width}): ', min=0, max=raw_video_width)
            new_height = get_int(f'New height of viewport (in characters) (0-{int(raw_video_height/2)}): ', min=0, max=raw_video_height/2)
            resize_viewport(new_width, new_height)
            print('Resizing the box bigger while zoomed in may lead to the box misshaping, enter "r" to redraw the box with selected dimensions')
            continue

        elif confirmation.lower() == 'r':
            continue

        elif confirmation.lower() == 'v':
            global mp4
            print(f'\nCurrent video: {mp4}')
            new_video = get_string('Enter path to desired mp4: ')

            if os.path.exists(f'assets/{new_video}'):
                mp4 = new_video
            else:
                print("mp4 file not found")
                time.sleep(2)
                continue
        
        elif confirmation.lower() == 'd':
            show_debug_info_at_end = True
            print(f'\nExtra Debug Information will be displayed at the end of the video')
            time.sleep(2)
            continue

        else:
            return


def draw_viewport(width, height):
    '''
    Prints out a (width by height) characters ASCII box to allow user to adjust their console zoom
    to fit the viewport for the video to play in the console
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
    avg = (r + g + b) / 3
    # NTSC formula for luminance
    grey = 0.299*r + 0.587*g + 0.114*b
    # `^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$

    # These values are arbitrary
    if grey > 250:
        return '@'
    elif 245 < grey <= 250:
        return 'B'
    elif 240 < grey <= 245:
        return '%'
    elif 235 < grey <= 240:
        return '8'
    elif 230 < grey <= 235:
        return '&'
    elif 225 < grey <= 230:
        return 'W'
    elif 220 < grey <= 225:
        return 'M'
    elif 215 < grey <= 220:
        return '#'
    elif 200 < grey <= 215:
        return '*'
    elif 180 < grey <= 200:
        return 'o'
    elif 144 < grey <= 180:
        return '?'
    elif 128 < grey <= 144:
        return '+'
    elif 96 < grey <= 128:
        return '~'
    elif 64 < grey <= 96:
        return 'I'
    elif 48 < grey <= 64:
        return 'i'
    elif 32 < grey <= 48:
        return '!'
    elif 24 < grey <= 32:
        return '-'
    elif 16 < grey <= 24:
        return ';'
    elif 10 < grey <= 16:
        return ':'
    elif 6 < grey <= 10:
        return '`'
    elif grey <= 6:
        return ' '
    else:
        print(f"A pixel's average rgb has registered as {grey}")
        raise ValueError


def play_video(path):
    '''
    Plays the ASCII Version of Bad Apple on the console
    '''
    # Reading video file
    video_capture = cv2.VideoCapture(f'assets/{path}')

    os.system('cls')

    # Confirm video information with the raw mp4
    global raw_video_width, raw_video_height, fps, total_frames, video_length
    raw_video_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    raw_video_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    video_length = total_frames / fps

    # Interval between pixels in raw video converted to ASCII
    x_interval = round(raw_video_width / console_frame_width)
    y_interval = round(raw_video_height / console_frame_height)

    # Use the fpstimer library to ensure the console video runs at raw video's fps
    timer = fpstimer.FPSTimer(fps)

    # Start timing ASCII video
    global video_start_time
    video_start_time = time.time()

    total_render_time = 0 # To measure time taken to render each frame so as to keep track of computed fps
    for frame_number in range(1, total_frames + 1):
        success, raw_frame = video_capture.read()

        # To measure time taken for computer to render 1 ascii frame from raw video, to calculate computated fps
        frame_start_time = time.time()
        
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

        # Puts the cursor at terminal position 0, 0 (top left) so next frame writes over the previous frame, equivalent to linux's tput cup 0 0
        print("\033[%d;%dH" % (0, 0), end="")
        print(buffer)

        # Measures time taken to render each frame to keep track of computed fps
        total_render_time += time.time() - frame_start_time
    
        # Delays so as to maintain raw video's fps to match audio if CPU is able to render faster than that
        timer.sleep()
    
    # End of video playback
    time_elapsed = time.time() - video_start_time
    show_video_info(time_elapsed, total_frames, total_render_time)


def get_mp3(path):
    '''
    Creates an mp3 file from an mp4 file, so only the mp4 file has to be provided at the start of the program
    '''
    global mp3

    video = VideoFileClip(f'assets/{path}')
    video.audio.write_audiofile("assets/audio.mp3")
    mp3 = "assets/audio.mp3"


def play_audio(path):
    '''
    Plays the mp3 audio
    '''
    global before_audio_start_time, after_audio_start_time
    before_audio_start_time = time.time()
    pygame.init()
    pygame.mixer.pre_init(buffer=2048) # Idk what this does, got this from CalvinLoke
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    after_audio_start_time = time.time()


def show_video_info(time_elapsed, total_frames, render_time):
    '''
    Prints to the console information about the raw mp4 used and computation information
    '''
    os.system('clear')

    # Raw Video Information
    print('-------- Raw Video Information --------')
    print(f'mp4 provided: {mp4}')
    print(f'Video length: {int(video_length // 60)} min {round(video_length % 60, 1)} s')
    print(f'Original resolution: {raw_video_width}x{raw_video_height}p')
    print(f'Original fps: {round(fps, 1)}')

    # Computation Information
    print('\n-------- Video Conversion Information --------')
    print(f'Video played for {int(time_elapsed // 60)} min {round(time_elapsed % 60, 1)} s')
    print(f'Computated fps: {round(total_frames/render_time, 1)}')
    print(f'Constrained (displayed) fps: {round(total_frames/time_elapsed, 1)}')


def show_debug_info():
    '''
    Prints to the console extra debug information for testing at the end of the video
    (Optional)
    '''
    print()
    print('-------- DEBUG INFORMATION --------')
    print(f'Time taken for play_audio to run asynchronously: {round(after_audio_start_time-before_audio_start_time, 3)}s')
    print(f'Time between audio start and video start (delay): {round(video_start_time-after_audio_start_time, 3)}s')


if __name__ == '__main__':
    main()