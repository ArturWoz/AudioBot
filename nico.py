from niconico import NicoNico

client = NicoNico()

with client.video.get_video("https://www.nicovideo.jp/watch/sm15776260") as video:
    video.download(f"{video.video.id}.mp4")
