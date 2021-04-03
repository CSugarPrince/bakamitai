import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", message="numpy.dtype size changed")

import imageio
import numpy as np
import torch
from skimage import img_as_ubyte
from skimage.transform import resize
from animate import normalize_kp
from tqdm import tqdm

from demo import load_checkpoints
from add_music import add_music

def permutate(im):
    # Convert the image (256,256,3) to the familiar [1,3,256,256] format
    return torch.tensor(im[np.newaxis].astype(np.float32)).permute(0, 3, 1, 2)


image_path = './input/input.jpg'
video_path = './input/bakamitai_template.mp4'
temp_out_path = './temp/baka_mitai_no_sound.mp4'
music_path = './input/bakamitai_sound_clip.mp3'
final_out_path = './output/output.mp4'
cpu = True

source_image = imageio.imread(image_path)
# Should fix memory error by feeding frame by frame opposed to whole video at once
driving_video = imageio.get_reader(video_path)

# Resize image to 256x256
source_image = resize(source_image, (256, 256))[..., :3]

fps = driving_video.get_meta_data()['fps']
ttl = driving_video.get_meta_data()['duration'] * fps
relative = True
print(fps, ttl)

generator, kp_detector = load_checkpoints(config_path='config/vox-adv-256.yaml',
                                          checkpoint_path='./data/checkpoints/vox-adv-cpk.pth.tar',
                                          cpu=cpu)

# Create Video Writer for output
writer = imageio.get_writer(temp_out_path, fps=fps)


with torch.no_grad():
    source = permutate(source_image)
    first_frame = permutate(
        resize(driving_video.get_data(0), (256, 256))[..., :3])

    # Keypoints
    kp_source = None
    kp_driving_initial = None

    if cpu:
        kp_source = kp_detector(source)
        kp_driving_initial = kp_detector(first_frame)
    else:
        kp_source = kp_detector(source.cuda())
        kp_driving_initial = kp_detector(first_frame.cuda())

    # Loop over the driving video
    for frame in tqdm(driving_video, total=int(ttl)):
        driving_frame = permutate(resize(frame, (256, 256))[..., :3])

        # get the current keypoints
        kp_driving = None

        if cpu:
            kp_driving = kp_detector(driving_frame)
        else:
            kp_driving = kp_detector(driving_frame.cuda())

        # normalize
        kp_norm = normalize_kp(kp_source=kp_source,
                               kp_driving=kp_driving,
                               kp_driving_initial=kp_driving_initial,
                               use_relative_movement=relative,
                               use_relative_jacobian=relative,
                               adapt_movement_scale=True)
        # create the fake output
        out = generator(source, kp_source=kp_source, kp_driving=kp_norm)

        pred = np.transpose(
            out['prediction'].data.cpu().numpy(), [0, 2, 3, 1])[0]
        writer.append_data(img_as_ubyte(pred))
    writer.close()

# Add music to video
add_music(src=temp_out_path, dest=final_out_path, music=music_path)