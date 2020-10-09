import os
import sys
from multiprocessing import Pool

import config
from downsize.constants import LOGS_DIR
from downsize.images import convert_image
from downsize.utils import log, format_timedelta, format_size, generate_paths
from downsize.videos import convert_video

if __name__ == '__main__':
    # initialize directories
    os.makedirs(LOGS_DIR, exist_ok=True)
    in_roots = [os.path.normpath(d) for d in config.INPUT_DIRECTORIES]
    out_root = os.path.normpath(config.OUTPUT_DIRECTORY)
    os.makedirs(out_root, exist_ok=True)

    in_size_videos = 0
    out_size_videos = 0
    in_size_images = 0
    out_size_images = 0

    for root in in_roots:
        for parent, dirs, files in os.walk(root):
            # otherwise not alphabetical order
            dirs.sort()
            files.sort()

            log(f"Browsing {parent}")

            image_files = [f for f in files if os.path.splitext(f)[1].lower() in config.FILE_FORMATS_IMAGE]
            video_files = [f for f in files if os.path.splitext(f)[1].lower() in config.FILE_FORMATS_VIDEO]

            # define respective output directory
            if config.OUTPUT_FLAT:
                out_dir = out_root
            else:
                relative_dir = parent[len(root) + 1:]  # where am I relative to root?

                if len(in_roots) == 1:
                    out_dir = os.path.join(out_root, relative_dir)
                else:
                    out_dir = os.path.join(out_root, os.path.basename(os.path.normpath(root)), relative_dir)
                os.makedirs(out_dir, exist_ok=True)

            # image files
            pool = Pool()
            try:
                task = [generate_paths(parent, out_dir, filename, config.OUTPUT_SUFFIX, config.OUTPUT_FORMAT_IMAGE)
                        + (config.OUTPUT_IMAGE_QUALITY, config.OUTPUT_IMAGE_MAX_DIM, config.OUTPUT_OVERWRITE)
                        for filename in image_files]
                res = pool.starmap(convert_image, task)
                in_size_images += sum(r[0] for r in res if r)
                out_size_images += sum(r[1] for r in res if r)
            finally:
                pool.close()
                pool.join()

            # video files
            for filename in video_files:
                in_path, out_path, out_name = generate_paths(parent, out_dir, filename, config.OUTPUT_SUFFIX,
                                                             config.OUTPUT_FORMAT_VIDEO)

                if config.OUTPUT_OVERWRITE or not os.path.exists(out_path):
                    try:
                        in_size, out_size, elapsed, duration = convert_video(in_path, out_path, filename,
                                                                             config.OUTPUT_VIDEO_BITRATE_FACTOR,
                                                                             config.OUTPUT_VIDEO_FALLBACK_CRF,
                                                                             config.ENABLE_GPU)

                        log(f"Converted {out_name} {format_size(in_size)} -> {format_size(out_size)} "
                            f"({out_size / in_size:.2%}), took {format_timedelta(elapsed)} "
                            f"({duration / elapsed:.1f}x @ {format_size(out_size / elapsed)}/s)")

                        in_size_videos += in_size
                        out_size_videos += out_size

                    except Exception as e:
                        log(e)
                        # Remove half-converted file
                        if os.path.exists(out_path):
                            os.remove(out_path)
                    except KeyboardInterrupt as e:
                        log(e)
                        if os.path.exists(out_path):
                            os.remove(out_path)
                        sys.exit()

            # log current compression rate if there were any files in the dir
            if in_size_videos and in_size_images and (video_files or image_files):
                log(f"Current compression rate: Videos: {format_size(in_size_videos)} -> "
                    f"{format_size(out_size_videos)} ({out_size_videos / in_size_videos:.2%}), "
                    f"Images: {format_size(in_size_images)} -> {format_size(out_size_images)} "
                    f"({out_size_images / in_size_images:.2%})")

            print()
