import os
# conda test env or bakamitai
# cd output folder
# ffmpeg -i result.mp4 -i bakamitai_sound_clip.mp3 -map 0 -map 1:a -c:v copy -shortest output.mp4
# nice

os.system("ffmpeg -i temp/baka_mitai_no_sound.mp4 -i input/bakamitai_sound_clip.mp3 -map 0 -map 1:a -c:v copy -shortest output/output.mp4")
