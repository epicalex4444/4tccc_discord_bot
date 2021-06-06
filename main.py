import discord
from discord.ext import commands, tasks #discord.ext seems to be a different thing entirely from discord
from commands_backend import set_name, find4tc, get_submissions, get_leaderboard, submit4tc, create_webpage, towerlb_backend

#token is stored in a blank file as plain text so we don't accidentely upload it to github
file = open('token')
token = file.read()
file.close()

bot = commands.Bot(command_prefix='!', intents=discord.Intents(messages=True), owner_id=482762949958696980, help_command=None, case_insensitive=True)

#response = [immediate, message, header]
#immediate is always sent as a discord message, message is sent as a discord message if it is
#short enough else it is the body of the webpage, header is the header off the webpage if it exists
async def send(ctx, discordMessage):
    #some messages don't need to send anything immediately
    if discordMessage.imediate != None:
        await ctx.send(discordMessage.imediate)

    #used for messages that guaranteed won't exceed 2000 chars
    if discordMessage.message == None:
        return

    if len(discordMessage.message) > 2000:
        if discordMessage.message.startswith('```') and discordMessage.message.endswith('```'):
            discordMessage.message = discordMessage.message[3:-3]
        await ctx.send('Message too long to send, creating a webpage link for the message instead')
        await ctx.send(create_webpage(discordMessage.header, discordMessage.message))
    else:
        await ctx.send(discordMessage.message)

#disables command not foun error in order to stop printing to the console
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

#logs to the console when the bot is on
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!help"))
    print('{0} ready'.format(bot.user))

#randy memes
myDayBeSoFine = False
@bot.event
async def on_message(message):
    global myDayBeSoFine
    if message.author.id == 279126808455151628:
        if myDayBeSoFine and message.content.lower() == 'then bam':
            ctx = await bot.get_context(message)
            await ctx.send('randy opens his mouth to speak')
        if message.content.lower() == 'my day be so fine':
            myDayBeSoFine = True
        else:
            myDayBeSoFine = False
    await bot.process_commands(message)

#shows general help message or how to use a specific command
@bot.command(name='help', help='!help *command_name', description='shows general help message or how to use a specific command')
async def help(ctx, arg=None):
    commands = bot.commands
    if arg == None:
        helpMessage = '```* represents that the parameter is optional\n\nCommands:\n'
        for command in commands:
            helpMessage += '{0}\nDescription: {1}\n'.format(command.help, command.description)
            if len(command.aliases) != 0:
                helpMessage += 'Aliases: {0}\n'.format(', '.join(command.aliases))
            helpMessage += '\n'
        helpMessage += '\nIf you have found a bug, report it to epicalex4444#5552 on discord\nFor more in depth info see https://github.com/epicalex4444/4tccc_discord_bot```'
    else:
        commandNotFound = True
        for command in commands:
            if command.name == arg or arg in command.aliases:
                helpMessage = '{0}\nDescription: {1}'.format(command.help, command.description)
                if len(command.aliases) != 0:
                    helpMessage += '\nAliases: ' + ', '.join(command.aliases)
                commandNotFound = False
        if commandNotFound:
            return await ctx.send("that command doesn't exist, use !help with no arguments to see the commands")

    await ctx.send(helpMessage)

#used to specify an name so you don't have to use the name parameter in submit
@bot.command(name='name', help='!name name', description="used to specify an name so you don't have to use the name parameter in submit", rest_is_raw=True)
async def name(ctx, *, arg):
    if arg == '':
        response = 'You need to provide a name'
    else:
        response = set_name(ctx.author.id, arg[1:])

    await ctx.send(response)

#finds all the combos remaining that have all of the specified towers
@bot.command(name='find', help='!find *towers', description='finds all the combos remaining that have all of the specified towers')
async def find(ctx, tower0=None, tower1=None, tower2=None, tower3=None):
    towers = [tower0, tower1, tower2, tower3]
    towers = [tower for tower in towers if tower is not None] #python smh, removes all None from the list
    discordMessage = find4tc(towers)
    await send(ctx, discordMessage)

#finds all submissions or submissions from name
@bot.command(name='submissions', help='!submisions *name', description='finds all submissions or submissions from name', rest_is_raw=True)
async def submissions(ctx, *, arg):
    if arg == '':
        discordMessage = get_submissions()
    else:
        discordMessage = get_submissions(arg[1:])

    await send(ctx, discordMessage)

#shows the leaderboard
@bot.command(name='leaderboard', help='!leaderboard *"name" *amount', description='shows the leaderboard', aliases=['lb'], rest_is_raw=True)
async def leaderboard(ctx, *, arg):
    if arg == '':
        discordMessage = get_leaderboard()
    elif arg[1:].isdigit():
        discordMessage = get_leaderboard(amount=arg[1:])
    elif arg[1] != '"' or arg[-1] != '"':
        return await ctx.send('Name must start and end with double quotes')
    elif arg == ' ""':
        return await ctx.send('Name cannot be nothing')
    else:
        discordMessage = get_leaderboard(name=arg[2:-1])

    await send(ctx, discordMessage)

#used to submit a combo, name is required if you haven't specified your name with !name
@bot.command(name='submit', help='!submit code *name', description="used to submit a combo, name is required if you haven't specified your name with !name", rest_is_raw=True)
async def submit(ctx, *, arg):
    if arg.startswith(' Can you beat this Bloons TD 6 challenge? https://join.btd6.com/Challenge/'):
        arg = ' ' + arg[74:]
    if arg == '':
        return await ctx.send('Code must be provided for a submission')

    #if there is a name parameter
    if arg.count(' ') >= 2:
        spaceIndex = arg[1:].find(' ')
        code = arg[1:spaceIndex + 1]
        name = arg[spaceIndex + 2:]
        discordMessage = submit4tc(code, name=name)
    else:
        discordMessage = submit4tc(arg[1:], discordId=ctx.author.id)

    await send(ctx, discordMessage)

@bot.command(name='bot', help='!bot', description='shows bot invite link')
async def bot_invite(ctx):
    await ctx.send('https://discord.com/api/oauth2/authorize?client_id=790526190749745192&permissions=2048&scope=bot')

@bot.command(name='server', help='!server', description='shows server invite')
async def server_invite(ctx):
    await ctx.send('https://discord.gg/Gapyp6kw3b')

@bot.command(name='towerlb', help='!towerlb', description='shows how many combos each tower has left')
async def towerlb(ctx):
    await ctx.send(towerlb_backend())

bot.run(token)
