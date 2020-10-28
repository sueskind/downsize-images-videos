import datetime as dt
import os

from .constants import LOGS_STDOUT_FILE


def generate_paths(parent, out_dir, filename, suffix, new_format):
    in_path = os.path.join(parent, filename)
    out_name = f"{os.path.splitext(filename)[0]}{suffix}.{new_format}"
    out_path = os.path.join(out_dir, out_name)

    return in_path, out_path, out_name


def log(message):
    msg = f"{dt.datetime.now().strftime('%X')} {message}"
    with open(LOGS_STDOUT_FILE, "a") as f:
        f.write(msg + "\n")
    print(msg)


def format_timedelta(seconds):
    return f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02}"


def format_size(bytes):
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024 * 1024:
        return f"{bytes // 1024} KB"
    elif bytes < 1024 * 1024 * 1024:
        return f"{bytes / 1024 / 1024:.1f} MB"
    else:
        return f"{bytes / 1024 / 1024 / 1024:.1f} GB"
