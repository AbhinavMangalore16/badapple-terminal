import sys
import os
import time
import signal
import getpass
import shutil
import cv2
import pygame
import moviepy.editor as mp
import fpstimer
from PIL import Image
from multiprocessing import Pool, cpu_count, Process, Manager
import urllib.request

DOWN_URL = "https://github.com/AbhinavMangalore16/badapple-terminal/raw/main/assets/badapple.mp4"
VIDEO_FILE = "badapple.mp4"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"
ASCII_CHARS = [" ",",",":", ";","+","*","?","%","S","#","@",]
FRAME_SIZE = 150
FRAME_RATE = 1/30

TERMINAL_VIDEO = []

apple_frames = [
r"""
             .:'
         __ :'__
      .'`  `-'  ``.
     :             :
     :             :
      :           :
       `.__.-.__.'
""",
r"""
             .:'
         __ :'__
      .'`  `-'  ``.
     :          .-'
     :         :
      :         `-;
       `.__.-.__.'
""",
r"""
             .:'
         __ :'__
      .'`__`-'__``.
     :__________.-'
     :_________:
      :_________`-;
       `.__.-.__.'
""",

]
def ensure_video():
    if not os.path.exists(VIDEO_FILE):
        print("Downloading Bad Apple video (~200MB)...")
        urllib.request.urlretrieve(DOWN_URL, VIDEO_FILE)
        print("Download complete!")

    return VIDEO_FILE
def rotate_apple(frames, loops=5, delay=0.15):
    for _ in range(loops):
        for frame in frames + frames[::-1]:  
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.stdout.write(RED + frame + RESET)
            sys.stdout.flush()
            time.sleep(delay)
def show_credits(user_name="You!"):
    print("\n" + CYAN + "="*70 + RESET)
    print(CYAN + "                           **CREDITS**" + RESET)
    print(CYAN + "="*70 + RESET)
    print(GREEN + "Code Author: " + YELLOW + "Abhinav Mangalore [GitHub: @AbhinavMangalore16]" + RESET)  
    print(GREEN + "Original Animation: " + MAGENTA + "Alstroemeria Records (Bad Apple!! MV)" + RESET)
    print(GREEN + "Source / Game Video: " + BLUE + "Touhou Project (ZUN)" + RESET)
    print("Inspired by open-source Bad Apple!! terminal projects by the community.")
    print(GREEN + f"And {user_name}! {getpass.getuser()}! To play on your terminal.." + RESET)  
    print(CYAN + "="*70 + RESET + "\n")
def signal_handler(sig, frame):
    print("\nI'm sorry, but did you interrupt?")
    show_credits()
    sys.exit(0)
def resize_image(image_frame):
    width, height = image_frame.size
    aspect_ratio = (height/float(width * 2.5)) 
    new_height = int(aspect_ratio*FRAME_SIZE)
    resized_image = image_frame.resize((FRAME_SIZE, new_height))
    return resized_image
def characterize(img):
    pixies = img.getdata()
    chars = "".join([ASCII_CHARS[pixy//25] for pixy in pixies])
    return chars
def extractor(video_path, start_frame, nf=1000):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    c = 1
    ret, img_frame = cap.read()
    
    while ret and c <= nf:
        try:
            img = Image.fromarray(img_frame)
            ASCII_chars = characterize(resize_image(img.convert("L")))
            pixels = len(ASCII_chars)
            video_frame = "\n".join([ASCII_chars[i:i+FRAME_SIZE] for i in range(0, pixels, FRAME_SIZE)])
            TERMINAL_VIDEO.append(video_frame)
        except Exception:
            pass
        c += 1
        ret, img_frame = cap.read()  # read next frame
    cap.release()
def play_audio(path):
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
def play_terminal():
    os.system('mode 150, 500')
    timer = fpstimer.FPSTimer(30)
    
    for frame_number in range(len(TERMINAL_VIDEO)):
        sys.stdout.write("\r" + TERMINAL_VIDEO[frame_number])
        timer.sleep()
def preprocessing(video):
    if os.path.exists(video):
        vid = video.strip()
        cap = cv2.VideoCapture(vid)
        TOTAL = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        VIDEO = mp.VideoFileClip(vid)
        audio = 'badapple.mp3'
        VIDEO.audio.write_audiofile(audio)
        frames_per_process = TOTAL // 4
        ranges = [(i * frames_per_process + 1, (i + 1) * frames_per_process) for i in range(4)]
        ranges[-1] = (ranges[-1][0], TOTAL - 1)  # ensure last range hits final frame

        start_time = time.time()
        sys.stdout.write('Preprocessing...\n')
        extractor(vid, 1, TOTAL - 1)
        sys.stdout.write(f'Preprocessing completed in {time.time() - start_time:.2f} seconds!\n')
        return TOTAL
    else:
        sys.stdout.write("FILE NOT FOUND")
        raise FileNotFoundError("File was not found!")

signal.signal(signal.SIGINT, signal_handler)
def main():
    try:
        rotate_apple(apple_frames, loops=3)

        sys.stdout.write('\n')
        sys.stdout.write('============================================\n')
        sys.stdout.write('                 BAD APPLE!!                \n')
        sys.stdout.write('============================================\n')
        sys.stdout.write("A terminal rendition of the classic Touhou shadow video!\n\n")

        while True:
            sys.stdout.write("Lessgo!? (Y/N): ")
            ch = input().strip().lower()

            if ch == 'y':
                VIDEO_FILE = ensure_video()
                frags = preprocessing(VIDEO_FILE)
                play_audio('badapple.mp3')
                play_terminal()
                break

            elif ch == 'n':
                sys.stdout.write("Alright, exiting...\n")
                break

            else:
                sys.stdout.write("I couldn't get you! Please enter Y or N.\n")
                continue

    finally:
        show_credits()

if __name__ == '__main__':
    main()
