# image sequence blender

Convert an image sequence to a movie, with weighted smoothing.

Say you have a sequence of images, from a surveillance camera which takes photos at 1fps. If you convert these to a movie, you will see "fast forward artifacts", tiny jumpcuts, if you will. This script attempts to blend neighboring images of a frame to minimize/hide this effect.

## Prerequisites

* Python
* numpy
* PIL
* ffmpeg
* imagemagick (for test.sh)

## Usage

```
usage: windowblend.py [-h] [--inglob INGLOB] [--windowsize WINDOWSIZE]
                      [--attack ATTACK] [--ffmpegoutopts FFMPEGOUTOPTS]
                      outfile

positional arguments:
  outfile               output file

optional arguments:
  -h, --help            show this help message and exit
  --inglob INGLOB       input files glob
  --windowsize WINDOWSIZE
                        window size
  --attack ATTACK       attack and release length
  --ffmpegoutopts FFMPEGOUTOPTS
                        ffmpeg output options, like c:v. comma-separated.
```

Unfortunately, I do not remember how `attack` relates to `windowsize`. Default is 0, so probably ignore it, run some tests or try to read the source.

## Examples, tests

Run test.sh, which creates a sequence of test images and runs the script.
