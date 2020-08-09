
 all_user = self.users
  # print(all_user)
  for a in all_user:
       if(a.bot == True):
            print(f"{a.name} is a bot, skipping")
        else:
            # print(f"Name:{a.name} Discriminator:{a.discriminator} ID:{a.id}")
            if(a.id == 520070392271077386 or a.id == 293181423060516864 or a.id == 498817814048538625):
                # await a.send(
                #     content="i luv you dont tell nkz"
                # )
                print(
                    f"Name:{a.name} Discriminator:{a.discriminator} ID:{a.id}")
    # async for message in self.channel.history(limit=1,oldest_first=False):
    #     print(message.content)
