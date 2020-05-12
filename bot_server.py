# https://discord.gg/tkpv6q

import discord
from discord.ext import commands
from data import db_session
from config import *
from data.users import User

db_session.global_init(DB_NAME)


class CoronaCommandBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = db_session.create_session()

    @commands.command(name='ill')
    async def ill(self, ctx):
        name = str(ctx.author).split('#')[0]
        user = self.session.query(User).filter(User.chatname == name).first()
        if not user:
            await ctx.send("Вы не зарегистрировались в приложении!")
        else:
            user.is_ill = True
            self.session.commit()
            await ctx.send("Очень жаль, выздоравливайте!")

    @commands.command(name='heal')
    async def heal(self, ctx):
        name = str(ctx.author).split('#')[0]
        user = self.session.query(User).filter(User.chatname == name).first()
        if not user:
            await ctx.send("Вы не зарегистрировались в приложении!")
        else:
            user.is_ill = False
            self.session.commit()
            await ctx.send("Ура, очень рады за вас!")


bot = commands.Bot(command_prefix='$')
bot.add_cog(CoronaCommandBot(bot))
bot.run(TOKEN)
