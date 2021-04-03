## To manually create conda environment:

`conda create -n bakamitai python=3.6.8`

`conda install -n bakamitai ffmpeg imageio matplotlib numpy pandas Pillow pytorch PyYAML scikit-image scikit-learn scipy tqdm`

then manually install:
`conda install -n bakamitai -c pytorch torchvision` 
`conda install -n bakamitai -c conda-forge imageio-ffmpeg`

cd 

## For Dockerfile
Dockerfile:
RUN conda create -n bakamitai python=3.6.8 && \
conda install -n bakamitai ffmpeg imageio matplotlib numpy pandas Pillow pytorch PyYAML scikit-image scikit-learn scipy tqdm && \
conda install -n bakamitai -c pytorch torchvision && \
conda install -n bakamitai -c conda-forge imageio-ffmpeg

^ Works for running with cpu. Haven't tested GPU yet