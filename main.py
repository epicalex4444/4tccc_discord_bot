from discord import Intents
from discord.ext import commands #discord.ext seems to be a different thing entirely from discord
from commands_backend import set_alias, find4tc, get_submissions, get_leaderboard, submit4tc, create_hastebin_link

token = 'NzkwNTI2MTkwNzQ5NzQ1MTky.X-B44w.k2yMT34LRq1a_Ex-LoKjOeex_OI'
ownerId = 482762949958696980

bot = commands.Bot(command_prefix='!', intents=Intents(messages=True), owner_id=ownerId, help_command=None)

#sends the message or if it is too long it creates a hastebin link
def send(ctx, message):
    if len(message) > 2000:
        await ctx.send('Message too long to send, ceating a hatebin link for the message instead')
        await ctx.send(create_hastebin_link(message))
    else:
        await ctx.send(message)

#logs to the console when the bot is on
@bot.event
async def on_ready():
    print('{0} ready'.format(bot.user))

#shows general help message or how to use a specific command
@bot.command(name='help', help='!help *command_name', description='shows general help message or how to use a specific command')
async def help(ctx, arg=None):
    commands = bot.commands
    if arg == None:
        helpMessage = '```* represents that the parameter is optional\n\nCommands:\n'
        for command in commands:
            helpMessage += 'Name: {0}\nUsage: {1}\nDescription: {2}\n'.format(command.name, command.help, command.description)
            if len(command.aliases) != 0:
                helpMessage += 'Aliases: {0}\n'.format(', '.join(command.aliases))
            helpMessage += '\n'
        helpMessage += '\nIf you have found a bug, report it to epicalex4444#5552 on discord\nFor more in depth info see https://github.com/epicalex4444/4tccc_discord_bot/blob/main/README.md```'
    else:
        commandNotFound = True
        for command in commands:
            if command.name == arg:
                helpMessage = 'Usage: {0}\nDescription: {1}'.format(command.help, command.description)
                if len(command.aliases) != 0:
                    helpMessage += '\nAliases: ' + ', '.join(command.aliases)
                commandNotFound = False
        if commandNotFound:
            return await ctx.send("that command doesn't exist, use !help with no arguments to see the commands")

    await ctx.send(helpMessage)

#used to specify an alias so you don't have to use the name parameter in submit
@bot.command(name='alias', help='!set_alias name', description="used to specify an alias so you don't have to use the name parameter in submit", rest_is_raw=True)
async def alias(ctx, *, arg):
    if arg == '':
        response = 'You need to give a name to set as your alias'
    else:
        response = set_alias(ctx.author.id, arg[1:])

    await ctx.send(response)

#finds all the combos remaining that have all of the specified towers
@bot.command(name='find', help='!find *towers', description='finds all the combos remaining that have all of the specified towers')
async def find(ctx, tower0=None, tower1=None, tower2=None, tower3=None):
    towers = [tower0, tower1, tower2, tower3]
    towers = [tower for tower in towers if tower is not None] #python smh, removes all None from the list
    response = find4tc(towers)
    await ctx.send(response)

#finds all submissions or submissions from name
@bot.command(name='submissions', help='!submisions *name', description='finds all submissions or submissions from name', rest_is_raw=True)
async def submissions(ctx, *, arg):
    if arg == '':
        response = get_submissions()
    else:
        response = get_submissions(arg[1:])

    await ctx.send(response)

#shows the leaderboard
@bot.command(name='leaderboard', help='!leaderboard *"name" *amount', description='shows the leaderboard', aliases=['lb'], rest_is_raw=True)
async def leaderboard(ctx, *, arg):
    if arg == '':
        response = get_leaderboard()
    elif arg[1:].isdigit():
        response = get_leaderboard(amount=arg[1:])
    elif arg[1] != '"' or arg[-1] != '"':
        response = 'Name must start and end with double quotes'
    elif arg == ' ""':
        response = 'Name cannot be nothing'
    else:
        response = get_leaderboard(name=arg[2:-1])

    await ctx.send(response)

#used to submit a combo, name is required if you haven't specified your alias with !alias
@bot.command(name='submit', help='!submit code *name', description="used to submit a combo, name is required if you haven't specified your alias with !alias", rest_is_raw=True)
async def submit(ctx, *, arg):
    if arg == '':
        return await ctx.send('Code must be provided for a submission')

    #if there is a name parameter
    if arg.count(' ') >= 2:
        spaceIndex = arg[1:].find(' ')
        code = arg[1:spaceIndex + 1]
        name = arg[spaceIndex + 2:]
        print(name.replace(' ', '/s'))
        response = submit4tc(code, name=name)
    else:
        response = submit4tc(arg[1:], discordId=ctx.author.id)
        
    await ctx.send(response)

bot.run(token)