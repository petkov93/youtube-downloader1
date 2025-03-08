import yt_dlp
import os
# if you don't have ffmpeg.exe, you need to install it and provide the correct path.
# Official releases: https://github.com/BtbN/FFmpeg-Builds/releases
FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-2025-02-02-git-957eb2323a-full_build\bin\ffmpeg.exe"

DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Desktop', 'YouTube')


def youtube_downloader(url, callback=None):
    """ func to download YouTube songs from url/song name (YouTube search) """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': FFMPEG_PATH,
        'noplaylist': True,
        'default_search': 'ytsearch',
        'quiet': True,
        'verbose': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if 'entries' in info:
            first_entry = info['entries'][0]  # Get the first search result
            title = first_entry.get('title')  # Extract the title of the first result
        else:
            title = info.get('title')  # Extract the title directly for direct links

    if callback:
        callback(title)
