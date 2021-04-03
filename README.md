
# Dame Da Ne (Baka Mitai) App

だめだね・ばかみたい

If you want to conveniently create a bakamitai video from your local machine, here's what you need to do:

## 1. Prepare your picture
To prep your picture, you can use this [website](https://photoshop.adobe.com/)
1. Crop your image first, make sure the face is clearly visible and centered
2. Then resize your image to 256 x 256
3. Save this image in the input folder as a "input.jpg"

## 2. Run the code

**Option 1: Docker (the easiest way)**
1. Clone this repository
2. Install Docker
3. cd to this repo, `docker build -t baka-image .`
4. `docker run --name baka_container -i -t baka-image /bin/bash`
5. `conda activate bakamitai`
6. `python main.py`
7. `exit` to exit the docker container and return to a normal terminal on host machine
7. `docker cp baka_container:/app/output/output.mp4 ./output/d_output.mp4`
8. All done! Look in the output folder for your final video.


**Option 2: Run locally on your machine using Anaconda**
1. Clone this repository
2. Download two files and put them both in the "data/checkpoints/" folder
  - https://jhew-bakamitai.s3.amazonaws.com/data/checkpoints/vox-adv-cpk.pth.tar 
  - https://jhew-bakamitai.s3.amazonaws.com/data/checkpoints/vox-cpk.pth.tar
3. Install Anaconda ver 4.9.2 (or Miniconda 4.9.2)
4. Create a conda environment by first activating the conda base environment, then running this command:
  - `conda env create -f conda_environments/mac_local.yml` for mac
  - `conda env create -f conda_environments/win_local.yml` for windows
  - If this doesn't work, see the readme in conda environments for manually recreating the conda environment
5. Activate the conda env you just created (look up how to do this for your OS)
6. In the repo, with the conda env active, `python main.py`
7. The final video should show up in the output folder
8. All done! It was a little more work, but you should be good to go!

