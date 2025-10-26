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
from tqdm import tqdm
from typing import List

def get_frame_size() -> int:
    """
    Determine an appropriate frame width based on the terminal size.

    Returns:
        int: Width of the terminal for ASCII frames.
    """
    try:
        columns, _ = shutil.get_terminal_size(fallback=(150, 40))
        return max(10, columns - 5)
    except Exception:
        return 150
DOWN_URL:str = "https://raw.githubusercontent.com/AbhinavMangalore16/badapple-terminal/main/badapple_terminal/assets/badapple.mp4"
VIDEO_FILE:str = "badapple.mp4"

RED:str = "\033[31m"
GREEN:str = "\033[32m"
YELLOW:str = "\033[33m"
BLUE:str = "\033[34m"
MAGENTA:str = "\033[35m"
CYAN:str = "\033[36m"
RESET:str = "\033[0m"
ASCII_CHARS: List[str] = [" ", ".", "`", ":", "-", "~", "+", "*", "=", "%", "#", "@"]
FRAME_SIZE:int = get_frame_size()
FRAME_RATE:float = 1/30

TERMINAL_VIDEO:List[str] = []

apple_frames: List[str] = [
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
 
    
def ensure_video() -> str:
    """
    Ensure the Bad Apple video exists locally.
    Downloads the video if not present.

    Returns:
        str: Path to the video file.
    """
    VIDEO_FILE = "./assets/badapple.mp4"
    if not os.path.exists(VIDEO_FILE):
        # Ensure directory exists
        os.makedirs(os.path.dirname(VIDEO_FILE), exist_ok=True)
        print("Downloading Bad Apple video (~200MB)...")
        urllib.request.urlretrieve(DOWN_URL, VIDEO_FILE)
        print("Download complete!")
    return VIDEO_FILE

def rotate_apple(frames: List[str], loops:int=5, delay:float=0.15):
    """
    Display a simple apple ASCII animation in the terminal.

    Args:
        frames (list[str]): List of ASCII frames.
        loops (int, optional): Number of loops to repeat. Defaults to 5.
        delay (float, optional): Delay between frames in seconds. Defaults to 0.15.
    """
    for _ in range(loops):
        for frame in frames + frames[::-1]:  
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.stdout.write(RED + frame + RESET)
            sys.stdout.flush()
            time.sleep(delay)

def show_credits(user_name:str="You!"):
    """
    Display the credits at the end of the animation.

    Args:
        user_name (str, optional): Name of the user. Defaults to "You!".
    """
    print("\n" + CYAN + "="*70 + RESET)
    print(CYAN + "                           **CREDITS**" + RESET)
    print(CYAN + "="*70 + RESET)
    print(GREEN + "Code Author: " + YELLOW + "Abhinav Mangalore [GitHub: @AbhinavMangalore16]" + RESET)  
    print(GREEN + "Original Animation: " + MAGENTA + "Alstroemeria Records (Bad Apple!! MV)" + RESET)
    print(GREEN + "Source / Game Video: " + BLUE + "Touhou Project (ZUN)" + RESET)
    print("Inspired by open-source Bad Apple!! terminal projects by the community.")
    print(GREEN + f"And {user_name}! {getpass.getuser()}! Hope you enjoyed playing this on your terminal.." + RESET)  
    print(CYAN + "="*70 + RESET + "\n")

def signal_handler(sig:int, frame)-> None:
    """
    Handle keyboard interrupts gracefully, showing credits before exit.
    """
    print("\nI'm sorry, but did you interrupt?")
    show_credits()
    sys.exit(0)

def resize_image(image_frame:Image.Image)-> Image.Image:
    """
    Resize an image while maintaining aspect ratio for terminal display.

    Args:
        image_frame (PIL.Image.Image): Image to resize.

    Returns:
        PIL.Image.Image: Resized image.
    """
    width, height = image_frame.size
    aspect_ratio = (height/float(width * 2.5)) 
    new_height = int(aspect_ratio*FRAME_SIZE)
    resized_image = image_frame.resize((FRAME_SIZE, new_height))
    return resized_image

def characterize(img:Image.Image)-> str:
    """
    Convert a grayscale image into ASCII characters.

    Args:
        img (PIL.Image.Image): Grayscale image.

    Returns:
        str: ASCII representation of the image.
    """
    pixies = img.getdata()
    chars = "".join([ASCII_CHARS[pixy * len(ASCII_CHARS) // 256] for pixy in pixies])
    return chars

def extractor(video_path:str, start_frame:int, nf:int = 1000) -> None:
    """
    Extract frames from a video and convert them to ASCII art.

    Args:
        video_path (str): Path to video.
        start_frame (int): Frame to start extraction.
        nf (int, optional): Number of frames to extract. Defaults to 1000.
    """
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    ret, img_frame = cap.read()
    c = 1

    for _ in tqdm(range(nf), desc="Extracting frames"):
        if not ret:
            break
        try:
            img = Image.fromarray(img_frame)
            ASCII_chars = characterize(resize_image(img.convert("L")))
            pixels = len(ASCII_chars)
            video_frame = "\n".join([ASCII_chars[i:i+FRAME_SIZE] for i in range(0, pixels, FRAME_SIZE)])
            TERMINAL_VIDEO.append(video_frame)
        except Exception:
            pass
        
        c += 1
        ret, img_frame = cap.read()  

    cap.release()

def play_audio(path:str) -> None:
    """
    Play audio in the background using pygame.

    Args:
        path (str): Path to audio file.
    """
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def play_terminal()-> None:
    """
    Play ASCII video in the terminal with a fixed framerate.
    """
    os.system('mode 150, 500')
    timer = fpstimer.FPSTimer(30)
    
    for frame_number in range(len(TERMINAL_VIDEO)):
        sys.stdout.write("\r" + TERMINAL_VIDEO[frame_number])
        timer.sleep()

def preprocessing(video: str) -> int:
    """
    Preprocess the video to extract frames and generate audio.

    Args:
        video (str): Path to the video file.

    Returns:
        int: Total number of frames in the video.
    """
    if os.path.exists(video):
        vid = video.strip()
        cap = cv2.VideoCapture(vid)
        TOTAL = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        VIDEO = mp.VideoFileClip(vid)
        audio = 'assets/badapple.mp3'
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
    """
    Main entry point for the Bad Apple!! terminal player.
    Handles user prompts, video download, preprocessing, and playback.
    """
    try:
        rotate_apple(apple_frames, loops=3)
        sys.stdout.write('\n')
        sys.stdout.write(CYAN + '========================================================\n' + RESET)
        sys.stdout.write(MAGENTA + '                     BAD APPLE!!                \n' + RESET)
        sys.stdout.write(CYAN + '========================================================\n' + RESET)
        sys.stdout.write(YELLOW + "A terminal rendition of the classic Touhou shadow video!\n\n" + RESET)

        while True:
            sys.stdout.write(CYAN + "Lessgo!? (Y/N): " + RESET)
            ch = input().strip().lower()

            if ch == 'y':
                VIDEO_FILE = ensure_video()
                fragments = preprocessing(VIDEO_FILE)
                countdown_colors = [RED, YELLOW, GREEN]
                for i, color in zip(range(3, 0, -1), countdown_colors):
                    sys.stdout.write(f"\r{color}Starting video in {i}...{RESET}")
                    sys.stdout.flush()
                    time.sleep(1)
                sys.stdout.write(f"\r{GREEN}Starting now!        {RESET}\n")
                time.sleep(0.75)
                play_audio('assets/badapple.mp3')
                play_terminal()
                break

            elif ch == 'n':
                sys.stdout.write(YELLOW + "Alright, exiting...\n" + RESET)
                break

            else:
                sys.stdout.write(RED + "I couldn't get you! Please enter Y or N.\n" + RESET)
                continue

    finally:
        show_credits()


if __name__ == '__main__':
    main()
