import os

def add_music(src, dest, music):
  os.system(f"ffmpeg -i {src} -i {music} -map 0 -map 1:a -c:v copy -shortest {dest}")

if __name__ == "__main__":
  src = "temp/baka_mitai_no_sound.mp4"
  dest = "output/output.mp4"
  music = "input/bakamitai_sound_clip.mp3"

  add_music(src, dest, music)