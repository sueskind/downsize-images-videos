import os
import time

import ffmpeg

from .utils import log, format_timedelta, format_size


def get_video_metadata(path):
    try:
        res = ffmpeg.probe(path)

        fps_frac = res["streams"][0]["avg_frame_rate"].split("/")
        return {
            "duration": float(res["format"]["duration"]),
            "size": int(res["format"]["size"]),
            "codec": res["streams"][0]["codec_name"],
            "height": int(res["streams"][0]["height"]),
            "width": int(res["streams"][0]["width"]),
            "framerate": int(fps_frac[0]) / int(fps_frac[1])
        }
    except Exception:
        return None


def convert_video(in_path, out_path, filename, bitrate_factor, fallback_crf, try_gpu):
    meta_in = get_video_metadata(in_path)

    if not meta_in:  # probe failed
        start_time = time.time()
        log(f"Converting {filename} using CPU (probe failed)")
        (ffmpeg
         .input(in_path)
         .output(out_path,
                 vcodec="libx264",
                 crf=fallback_crf)
         .global_args("-y", "-hide_banner", "-loglevel", "panic")
         .run())
        elapsed = time.time() - start_time
        in_size = os.path.getsize(in_path)
        meta_out = get_video_metadata(out_path)

        return in_size, meta_out["size"], elapsed, meta_out["duration"]

    else:
        # empirical values
        bitrate = bitrate_factor * meta_in["height"] * meta_in["width"] * meta_in["framerate"]
        b = f"{int(bitrate)}M"
        maxrate = f"{int(bitrate * 1.5)}M"
        bufsize = f"{int(bitrate * 2)}M"

        log(f"Converting {filename} {meta_in['codec']} {format_timedelta(meta_in['duration'])} "
            f"{meta_in['width']}x{meta_in['height']} {meta_in['framerate']:.2f} fps {format_size(meta_in['size'])}")

        if try_gpu and meta_in["codec"] == "h264":  # try use hw-accel/gpu
            log("Try using GPU")
            try:
                start_time = time.time()
                (ffmpeg
                 .input(in_path,
                        hwaccel="cuvid",
                        vcodec="h264_cuvid")
                 .output(out_path,
                         vcodec="h264_nvenc",
                         b=b, maxrate=maxrate, bufsize=bufsize)
                 .global_args("-y", "-hide_banner", "-loglevel", "panic")
                 .run())
                elapsed = time.time() - start_time
                out_size = os.path.getsize(out_path)

                return meta_in["size"], out_size, elapsed, meta_in["duration"]

            except Exception:  # Sometimes h264 not applicable to gpu
                # Remove half-converted file
                if os.path.exists(out_path):
                    os.remove(out_path)

        # use cpu
        log("Using CPU")
        start_time = time.time()
        (ffmpeg
         .input(in_path)
         .output(out_path,
                 vcodec="libx264",
                 b=b, maxrate=maxrate, bufsize=bufsize)
         .global_args("-y", "-hide_banner", "-loglevel", "panic")
         .run())
        elapsed = time.time() - start_time
        out_size = os.path.getsize(out_path)

        return meta_in["size"], out_size, elapsed, meta_in["duration"]
