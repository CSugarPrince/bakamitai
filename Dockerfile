FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

MAINTAINER Anna Shcherbina <annashch@stanford.edu>

#
# Install Miniconda in /opt/conda
#

ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

ENV PATH /opt/conda/bin:$PATH
ENV LD_LIBRARY_PATH /usr/local/cuda-10.0/lib64:/usr/local/cuda-10.0/extras/CUPTI/lib64:$LD_LIBRARY_PATH

RUN conda create -n bakamitai python=3.6.8 && \
conda install -n bakamitai ffmpeg imageio matplotlib numpy pandas Pillow pytorch PyYAML scikit-image scikit-learn scipy tqdm && \
conda install -n bakamitai -c pytorch torchvision && \
conda install -n bakamitai -c conda-forge imageio-ffmpeg

WORKDIR /app

ADD https://drive.google.com/file/d/1G9MLhGANhc3gE85OvdeRBSIa8TFj8CuJ/view?usp=sharing ./data/checkpoints/vox-adv-cpk.pth.tar
ADD https://drive.google.com/file/d/1ETVI7n_sNGFj4hL-EdRAh5yWnVV3m0T7/view?usp=sharing ./data/checkpoints/vox-cpk.pth.tar

COPY . .
