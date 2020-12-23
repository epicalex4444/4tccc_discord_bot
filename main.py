import discord
from discord.ext import commands
import helpers

token = 'NzkwNTI2MTkwNzQ5NzQ1MTky.X-B44w.k2yMT34LRq1a_Ex-LoKjOeex_OI'
ownerId = 482762949958696980

intents = discord.Intents(messages=True)
bot = commands.Bot(command_prefix='!', intents=intents, owner_id=ownerId, help_command=None)

#logs to the console when the bot is on
@bot.event
async def on_ready():
    print('{0.user} ready'.format(bot))

#shows general help message or how to use a specific command
@bot.command(name='help', description='Usage: !help *command_name\nDescription: shows general help message or how to use a specific command')
async def help(ctx, arg=None):
    commands = bot.commands
    if arg == None:
        helpMessage = '```* represents that the parameter is optional\n\nCommands:\n'
        for command in commands:
            helpMessage += 'Name: ' + command.name + '\n' + command.description + '\n'
            if len(command.aliases) != 0:
                helpMessage += 'Aliases: ' + helpers.list_to_string(command.aliases) + '\n'
            helpMessage += '\n'
        helpMessage += '\nIf you have found a bug, report it to epicalex4444#5552 on discord\nFor more in depth info see (github documentation link)```'
        await ctx.send(helpMessage)
    else:
        commandFound = False
        for command in commands:
            if command.name == arg:
                helpMessage = command.description
                if len(command.aliases) != 0:
                    helpMessage += '\nAliases: ' + helpers.list_to_string(command.aliases)
                await ctx.send(helpMessage)
                commandFound = True
        if not commandFound:
            await ctx.send("that command doesn't exist, use !help with no arguments to see the commands")

#used to specify an alias so you don't have to use the name parameter in submit
@bot.command(name='set_alias', description="Usage: !set_alias name\nDescription: used to specify an alias so you don't have to use the name parameter in submit")
async def alias(ctx):
    await ctx.send('not implemented yet')

#finds all the combos remianing that have all of the specified towers
@bot.command(name='find', description='Usage: !find *tower *tower *tower *tower\nDescription: finds all the combos remaining that have all of the specified towers')
async def find(ctx, tower1, tower2, tower3, tower4):
    await ctx.send('not implemented yet')

#shows the leaderboard
@bot.command(name='leaderboard', description="Usage: !leaderboard\nDescription: shows the leaderboard", aliases=['lb'])
async def leaderboard(ctx):
    await ctx.send('not implemented yet')

#finds all the combos remianing that have all of the specified towers
@bot.command(name='submit', description="Usage: !submit code *name\nDescription: used to submit a combo, name is required if you haven't specified your alias with !alias")
async def submit(ctx):
    await ctx.send('not implemented yet')

bot.run(token)