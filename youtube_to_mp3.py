import yt_dlp
import os

# if you don't have ffmpeg.exe, you need to install it and provide the correct path.
# Official releases: https://github.com/BtbN/FFmpeg-Builds/releases
FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-2025-02-02-git-957eb2323a-full_build\bin\ffmpeg.exe"

DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Desktop', 'YouTube')


def youtube_downloader(url, callback=None):
    """ func to download YouTube songs from url/song name (YouTube search) """

    def download_progress_hook(data):
        name = os.path.basename(data['filename'])
        if data['status'] == 'downloading':
            percent = data.get('_percent_str').strip()
            if callback:
                download_str = f"\rDownloading >> {percent} >> {name}"
                callback(download_str)
        elif data['status'] == 'finished':
            if callback:
                finished_str = f'Finished downloading, now converting to mp3 >>\n{name}'
                callback(finished_str)
        elif data['status'] == 'processing':
            if callback:
                processing_str = f"\nConverting >>\n{data.get('postprocessor')}"
                callback(processing_str)

    def postprocessing_hook(data):
        if data['status'] == 'finished':
            information = data.get('info_dict', {})
            filename = os.path.basename(information.get('filepath') or
                                        information.get('_filename') or
                                        information.get('filename'))
            if callback and filename.endswith('.mp3'):
                postprocessing_finished = f"Converting finished ! >>\n{filename.strip('.mp3')}"
                callback(postprocessing_finished)

    ydl_opts = {
        'progress_hooks': [download_progress_hook],
        'postprocessor_hooks': [postprocessing_hook],
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
        'verbose': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # print(info)
        # if 'entries' in info:
        #     first_entry = info['entries'][0]  # Get the first search result
        #     title = first_entry.get('title')  # Extract the title of the first result
        # else:
        #     title = info.get('title')  # Extract the title directly for direct links

    # if callback:
    #     callback(title)
