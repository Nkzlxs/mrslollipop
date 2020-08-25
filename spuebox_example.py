import os
import youtube_dl
from youtube_dl.utils import DownloadError
import asyncio
import json


class audio_department:
    def __init__(self):
        pass

    def load_song(self, url: str):
        pass

    async def load_from_url(self, url: str):
        ydl = youtube_dl.YoutubeDL({
            'format': 'bestaudio/best',
            'noplaylist': True,
            'ignoreerrors': True,
            'nocheckcertificate': True,
            'logtostderr': False,
            'quiet': True
        })
        the_loop = asyncio.get_event_loop()
        return await the_loop.run_in_executor(None, self.extract_song, ydl, url)
        # bro =self.extract_song(ydl,url)
        # return bro
        pass

    def extract_song(self, ydl: youtube_dl.YoutubeDL, url: str):
        try:
            info = ydl.extract_info(url, download=False)
            # print(info)
            # media_path = os.path.join(os.path.dirname(os.path.realpath(
            #             __file__)),"test.json")
            # with open(media_path,"w") as j:
            #     json.dump(info,j,indent=2)
            # j.write(json.dumps(info))
            # print(f"Title: {info['title']}\nUrl: {info['url']}")
            result = {"title": info['title'], 'url': info['url']}
            return result
        except DownloadError as e:
            raise DownloadError("Data couldn't be retrieved")
        pass
        # asyncio.loop.run_in_executor()


if __name__ == "__main__":
    ad = audio_department()
    source = ad.load_from_url("https://www.youtube.com/watch?v=O_nPoLqbLfQ")
    print(source)
