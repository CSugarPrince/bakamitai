# Dame Da Ne (Baka Mitai) App

だめだね・ばかみたい

If you want to conveniently create a bakamitai video from your local machine, here's what you need to do:

## Set up the repo
1. Clone this repository
2. Go to this [Google Drive folder](https://drive.google.com/drive/folders/1KicXQYrg5paoBXtHswuZKPtZq8ncgdqG)
  - Copy the contents of the checkpoints folder inside data/checkpoints
  - Copy the contents of the input folder inside input
3. To prep your picture, you can use this [website](https://photoshop.adobe.com/)
  - crop your image first, make sure the face is clearly visible and centered
  - then resize your image to 256 x 256
  - save this image in the input folder as a "input.jpg"

## Running the program on local machine
1. Install Anaconda ver 4.9.2 (or Miniconda 4.9.2)
2. Create a conda environment by first activating the conda base environment, then running this command:
  - `conda env create -f conda_environments/mac_local.yml` if on mac
  - `conda env create -f conda_environments/win_local.yml` if on windows
3. Activate the newly created environement using `conda activate bakamitai`
4. Run `python main.py`
5. After it's done processing, your video should show up in the output folder.

## Running the program using Docker (easier)