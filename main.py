import discord
from discord.ext import commands

token = 'NzkwNTI2MTkwNzQ5NzQ1MTky.X-B44w.k2yMT34LRq1a_Ex-LoKjOeex_OI'
ownerId = 482762949958696980

#in the future will take a guild input and search if that guild has a custom prefix else it returns '!'
def get_command_prefix():
    return '!'

intents = discord.Intents(messages=True)
bot = commands.Bot(command_prefix=get_command_prefix(), intents=intents, owner_id=ownerId)

#logs to the console when the bot is on
@bot.event
async def on_ready():
    print('{0.user} logged ready'.format(bot))

@bot.command(name='hello', help='help text long', brief='help text short', description='description text', ignore_extra=False, rest_is_raw=True)
async def hello(ctx, *, arg):
    await ctx.send(arg)

bot.run(token)