import yt_dlp

def download_youtube_video(video_url, output_path):
    ydl_opts = {
        'outtmpl': output_path, # ダウンロードした動画の保存先パス
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # ダウンロードするフォーマット
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# ダウンロードするYouTube動画のURLと保存先パスを指定
video_url = "https://www.youtube.com/watch?v=xpN7s65auUU"
output_path = "/home/youtube/movie/test.mp4"

download_youtube_video(video_url, output_path)
