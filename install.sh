#!/bin/bash
# Installs python package dependencies

# Note: Make sure conda environment is active before running
# To run: "bash install.sh"

set -e
echo 'installing packages from requirements.txt'
pip install -r requirements.txt

echo 'installing pytorch'
pip install torch==1.0.0 torchvision==0.2.1 -f https://download.pytorch.org/whl/torch_stable.html

echo 'installing ffmpeg using conda'
conda install ffmpeg -c conda-forge