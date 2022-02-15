import discord
from discord.ext import commands, tasks
import commands_backend as cb
import threading

#token is stored in a blank file as plain text so we don't accidentely upload it to github
file = open('token')
token = file.read()
file.close()

bot = commands.Bot(command_prefix='!', intents=discord.Intents(messages=True), owner_id=482762949958696980, help_command=None, case_insensitive=True, allowed_mentions=discord.AllowedMentions().none())

#used for sending the a discordMessage object
async def send(ctx, discordMessage):
    if discordMessage.imediate != None:
        await ctx.send(discordMessage.imediate)

    if discordMessage.message == None:
        return

    if len(discordMessage.message) > 2000:
        if discordMessage.message.startswith('```') and discordMessage.message.endswith('```'):
            discordMessage.message = discordMessage.message[3:-3]
        await ctx.send('Message too long to send, creating a webpage link for the message instead')
        await ctx.send(cb.create_webpage(discordMessage.header, discordMessage.message))
    else:
        await ctx.send(discordMessage.message)

#disables command not found error in order to stop printing to the console
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

#logs to the console when the bot is on,
#sets the bot presence, and start webpage auto deletion
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!help"))
    cb.init_queue()
    threading.Thread(target=cb.webpage_deleter, daemon=True).start()
    print('{} ready'.format(bot.user))

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

@bot.command(name='help', help='!help *command_name', description='shows general help message or how to use a specific command')
async def help(ctx, arg=None):
    commands = bot.commands
    if arg == None:
        return await ctx.send('''```
Need a command list?
visit https://github.com/epicalex4444/4tccc_discord_bot

Need help with a specific command?
use !help commandName

Found a bug?
report bugs to epicalex4444#5552 on discord or make an issue on github

Still need help?
you can try visiting the github or contacting someone in the 4tccc server
```''')

    commandNotFound = True
    for command in commands:
        if command.name == arg or arg in command.aliases:
            helpMessage = '{}\nDescription: {}'.format(command.help, command.description)
            if len(command.aliases) != 0:
                helpMessage += '\nAliases: ' + ', '.join(command.aliases)
            commandNotFound = False
    if commandNotFound:
        return await ctx.send("that command doesn't exist, visit <https://github.com/epicalex4444/4tccc_discord_bot> for a command list")
    await ctx.send('```' + helpMessage + '```')

@bot.command(name='name', help='!name name', description="used to specify an name so you don't have to use the name parameter in submit", rest_is_raw=True)
async def name(ctx, *, arg):
    if arg == '':
        await ctx.send('You need to provide a name')
    else:
        await ctx.send(cb.set_name(ctx.author.id, arg[1:]))

@bot.command(name='find', help='!find *towers', description='finds all the combos remaining that have all of the specified towers')
async def find(ctx, tower0=None, tower1=None, tower2=None, tower3=None):
    towers = [tower0, tower1, tower2, tower3]
    towers = [tower for tower in towers if tower is not None]
    await send(ctx, cb.find4tc(towers))

@bot.command(name='submissions', help='!submisions *name', description='finds all submissions or submissions from name', rest_is_raw=True)
async def submissions(ctx, *, arg):
    if arg == '':
        await send(ctx, cb.get_submissions())
    else:
        await send(ctx, cb.get_submissions(arg[1:]))

@bot.command(name='leaderboard', help='!leaderboard *"name" *amount', description='shows the leaderboard', aliases=['lb'], rest_is_raw=True)
async def leaderboard(ctx, *, arg):
    if arg == '':
        await send(ctx, cb.get_leaderboard())
    elif arg[1:].isdigit():
        await send(ctx, cb.get_leaderboard(amount=arg[1:]))
    elif arg[1] != '"' or arg[-1] != '"':
        await ctx.send('Name must start and end with double quotes')
    elif arg == ' ""':
        await ctx.send('Name cannot be nothing')
    else:
        await send(ctx, cb.get_leaderboard(name=arg[2:-1]))

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
        await send(ctx, cb.submit4tc(code, name=name))
    else:
        await send(ctx, cb.submit4tc(arg[1:], discordId=ctx.author.id))

@bot.command(name='bot', help='!bot', description='shows bot invite link')
async def bot_invite(ctx):
    await ctx.send('https://discord.com/api/oauth2/authorize?client_id=790526190749745192&permissions=2048&scope=bot')

@bot.command(name='server', help='!server', description='shows server invite')
async def server_invite(ctx):
    await ctx.send('https://discord.gg/Gapyp6kw3b')

@bot.command(name='towerlb', help='!towerlb', description='shows how many combos each tower has left')
async def towerlb(ctx):
    await ctx.send(cb.towerlb_backend())

@bot.command(name='3towerlb', help='!3towerlb', description='shows how many combos each 3 tower combo has, not counting the 3 tower combos with 1')
async def threetowerlb(ctx):
    await send(ctx, cb.threetowerlb_backend())

bot.run(token)
