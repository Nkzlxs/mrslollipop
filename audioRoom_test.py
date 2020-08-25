import os
import json
import discord
import spuebox_example as sp
import asyncio


class AClient(discord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("llp.play"):
            # discord.opus.load_opus()
            full_command = message.content.split(" ")
            try:
                # media_path = os.path.join(os.path.dirname(os.path.realpath(
                #     __file__)), os.path.pardir, f"media/{full_command[1]}.raw")
                # media_src = open(media_path, "rb")
                # self.audio_source = discord.PCMAudio(media_src)
                result = await sp.audio_department().load_from_url(full_command[1])
                self.audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(result['url']),volume=1.0) # Nice fix on volume control
                self.audio_title = result['title']
            except Exception as e:
                print(e)
                await message.channel.send(content="Not found!")
                return

            msg = ""
            for x in self.get_all_channels():
                    if x.type == discord.ChannelType.voice:
                        for z in range(0, len(x.members)):
                            if x.members[z].id == message.author.id:
                                msg += f"Connected to {x.name}"
                                msg += f"\nNow playing: {self.audio_title}"
                                msg += f"\nUser limit: {x.user_limit}"
                                msg += f"\nYou are in this channel {message.author.mention} {x.members[z].name}"
                                self.user_channel = x
            try:
                self.voice_client = await self.user_channel.connect()
                print(self.user_channel,self.voice_client.channel)

                self.voice_client.play(self.audio_source)
                await message.channel.send(content=msg)
            except discord.ClientException as e:
                print(e)
                # print(self.user_channel,self.voice_client.channel)
                if(self.user_channel != self.voice_client.channel):
                    await self.voice_client.move_to(self.user_channel)
                    await message.channel.send(content=msg)
                if self.voice_client.is_connected():
                    if self.voice_client.is_playing():
                        self.voice_client.stop()
                        self.voice_client.play(self.audio_source)
                    else:
                        self.voice_client.play(self.audio_source)
                    await message.channel.send(content=msg)

        elif message.content.startswith("llp.stop"):
            self.voice_client.stop()
        elif message.content.startswith("llp.pause"):
            self.voice_client.pause()
        elif message.content.startswith("llp.resume"):
            self.voice_client.resume()
        elif message.content.startswith("llp.volume"):
            full_command = message.content.split(" ")
            print(full_command)
            volume_value = float(full_command[1]) / 100
            print(self.audio_source)
            try:
                self.audio_source.volume = volume_value #Nice fix on volume control
                    # ab = discord.PCMVolumeTransformer(
                        # self.audio_source, volume_value)
                    # self.voice_client.source = ab
                # print(self.audio_source.volume)
            except Exception as e:
                print(e)

        elif message.content.startswith("llp.dc"):
            await self.voice_client.disconnect()


class testAudio():
    def __init__(self):
        """ Zeroth, Get credentials """
        cred_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), os.pardir, "credential.json")
        # print(cred_path)
        cred_file = open(cred_path)
        self.credentials = json.load(cred_file)
        cred_file.close()
        # print(self.credentials)


if __name__ == "__main__":
    testAudioObj = testAudio()
    client = AClient()
    client.run(testAudioObj.credentials['DISCORD_BOT_ACCESS_TOKEN'])
