import cv2
import os
import sys
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame
from moviepy import VideoFileClip
import time

# Get the source file path.
if len(sys.argv) > 1:
    file_path = os.path.abspath(sys.argv[1])
else:
    print("Error enter file path in argument")
    sys.exit(1)

with open(file_path, 'r', newline="") as f:
    code = f.read()     # return a string 
    token_set = set(code.split())
    tokens = sorted(token_set, key=len)


## Take care of video and audio file paths relative to this script, not the
## current working directory of the VS Code extension host.
base_dir = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(base_dir, 'Asset', 'Bad-apple.mp4')
audio_path = os.path.join(base_dir, 'Asset', 'temp_audio.mp3')


## Create the audio file once. Extracting it on every launch delays the video.
if not os.path.exists(audio_path):
    video_clip = VideoFileClip(video_path)
    try:
        if video_clip.audio is None:
            raise RuntimeError("The video does not contain an audio track")
        video_clip.audio.write_audiofile(audio_path, logger=None)
    finally:
        video_clip.close()


## initialisations 
cam = cv2.VideoCapture(video_path)
if not cam.isOpened():
    raise RuntimeError("Unable to open video: " + video_path)
fps = cam.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    raise RuntimeError("Unable to read the video's frame rate")
pygame.mixer.init()
pygame.mixer.music.load(audio_path)


w = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
aspect_ratio = h/w;
cell_height, cell_width = 9, int(9/aspect_ratio)-8

def binary_search(ln):
    start , end = 0, len(token_set)-1
    ans = 0
    while(start <= end):
        mid = (end + start)//2
        if(len(tokens[mid]) == ln):
            return mid;
        elif len(tokens[mid]) > ln:
            end = mid-1
        elif len(tokens[mid]) < ln:
            ans = mid
            start = mid+1
    return ans

def fill(length):
    rem = length
    strings = []
    while rem != 0:
        # find string 
        ind = binary_search(rem)
        strings.append(tokens[ind])
        rem = rem - len(tokens[ind])
    return strings


def map(img):
    h, w = img.shape[:2]
    new_h, new_w = int(h/cell_height), int(w/cell_width)
    small_image = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    final_img = []
    for i in range(new_h):
        length = 0
        for j in range(new_w):
            if(small_image[i][j] == 0):
                if length != 0:
                    strings = fill(length)
                    final_img.extend(strings)
                
                final_img.append(' ')
                length = 0
            elif 0 < small_image[i][j] <= 85:
                if length != 0:
                    strings = fill(length)
                    final_img.extend(strings)
                final_img.append('.')
                length = 0
            else:
                length+=1
        if length != 0:
            strings = fill(length)
            final_img.extend(strings)
                        
        final_img.append('\n')
    result = "".join(final_img)
    return result                   

pygame.mixer.music.play()
start_time = time.time()


while True:
    succ, img = cam.read()
    if succ == False:
        break

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ascii = map(grey)

    print(ascii, flush=True)

    cv2.imshow("Img", img)

    expected_frame_time = (cam.get(cv2.CAP_PROP_POS_FRAMES))/fps
    process_delay = time.time() - start_time
    wait_ms = int((expected_frame_time - process_delay)*1000)
    if cv2.waitKey(max(1, wait_ms)) == ord('q'):
        break

pygame.mixer.music.stop()
with open(file_path, 'w', newline="") as f:
    f.write(code)
cam.release()
cv2.destroyAllWindows()
