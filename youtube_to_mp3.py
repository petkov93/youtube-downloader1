import yt_dlp
import os

# if you don't have ffmpeg.exe, you need to install it and provide the correct path.
# Official releases: https://github.com/BtbN/FFmpeg-Builds/releases

FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-2025-02-02-git-957eb2323a-full_build\bin\ffmpeg.exe"
DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Desktop', 'YouTube')


def youtube_downloader(url, callback=None):
    """
    function to download YouTube songs from url/song name (YouTube search)
    if you put song name, it searches YouTube and returns the first result.
    Then it converts the downloaded .webm/mp4 file to mp3.
    Final mp3 will be saved on Desktop, folder 'YouTube'
    """

    def download_progress_hook(data):
        """Function that returns the download info (%) on callback."""
        name = os.path.basename(data['filename'])
        if data['status'] == 'downloading':
            percent = data.get('_percent_str').strip()
            if callback:
                download_str = f"Downloading >> {percent} >>\n{name}"
                callback(download_str)
        elif data['status'] == 'finished':
            if callback:
                finished_str = f'Finished downloading, now converting to mp3 >>\n{name}'
                callback(finished_str)
        elif data['status'] == 'processing':
            if callback:
                processing_str = f"Converting >>\n{data.get('postprocessor')}"
                callback(processing_str)

    def postprocessing_hook(data):
        """Function that returns the conversion status on callback."""
        if data['status'] == 'finished':
            information = data.get('info_dict', {})
            filename = os.path.basename(information.get('filepath') or
                                        information.get('_filename') or
                                        information.get('filename'))
            if callback and filename.endswith('.mp3'):
                postprocessing_finished = f"Converting finished ! >>\n{filename.strip('.mp3')}"
                callback(postprocessing_finished)

    # options to be passed to the yt_dlp downloader/postprocessor
    ydl_opts: dict = {
        "progress_hooks": [download_progress_hook],
        "postprocessor_hooks": [postprocessing_hook],
        "format": "bestaudio/best",
        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        },
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"), # file name
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3", # output format -> mp3
            "preferredquality": "192",
        }],
        "ffmpeg_location": FFMPEG_PATH,
        "noplaylist": True,  # downloads the first song if it's a playlist
        "default_search": "ytsearch",
        "quiet": True,
        "verbose": False,
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
