# ------- Input options -------

INPUT_DIRECTORIES = ["/path/to/source1", "/path/to/source2"]
INCLUDE_SUBDIRECTORIES = True

# ------- Output options -------

OUTPUT_DIRECTORY = "/path/to/target"

# Attention! Using OUTPUT_FLAT might lead to files being overwritten (if OUPUT_OVERWRITE is True) or files not being
# converted (if OUTPUT_OVERWRITE is False).
OUTPUT_FLAT = False  # False: Keep directory structure, True: Output all to the same directory
OUTPUT_OVERWRITE = False  # False: Keep existing files instead of converting, True: Overwrite existing files

# File formats to be recognized/included
# case ignored, but '.' is necessary!
FILE_FORMATS_VIDEO = [".mp4", ".mov", ".avi", ".mts", ".wmv", ".mvi"]
FILE_FORMATS_IMAGE = [".jpg", ".png", ".jpeg"]

OUTPUT_SUFFIX = "_c"  # Added to each filename, empty "" for none

# Image options
OUTPUT_FORMAT_IMAGE = "jpg"
OUTPUT_IMAGE_QUALITY = 85  # jpeg percentage
OUTPUT_IMAGE_MAX_DIM = 4000  # The longer side of an image gets resized to this value if greater

# Video options
OUTPUT_FORMAT_VIDEO = "mp4"
OUTPUT_VIDEO_BITRATE_FACTOR = 14 / (1920 * 1080 * 60)  # quality, based on 14 MBit/s for 1920x1080 @ 60 fps
OUTPUT_VIDEO_FALLBACK_CRF = 26  # if video metadata can't be determined, use this crf value

# Performance options
ENABLE_GPU = True
