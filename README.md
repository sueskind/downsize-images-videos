# Batch downsize images/videos

This script performs lossy compression on all image and video files in given directories (and sub-directories).

## Dependencies

Image conversion: Pillow (PIL)  
Video conversion: FFmpeg

Image conversion is parallelized on the CPU and if available, H.264 en-/decoding is accelerated by CUDA GPU.

## Installation

Prerequisites (must be installed separately):
 - [Python 3](https://www.python.org/) (Tested with Python 3.8 64-Bit)
 - [FFmpeg](https://ffmpeg.org/)

To install run:
```
pip3 install -r requirements.txt
```

## Usage

Duplicate `example-config.py` and rename it to `config.py`. Edit the configuration as you like, then run:
```
python3 main.py
```