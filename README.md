# 4tccc_discord_bot
if you don't know what 4tccc is go here https://www.reddit.com/r/btd6/comments/eeqcn8/reintroducing_the_4tc_community_challenge_a/  

### invites:
bot invite: https://discord.com/api/oauth2/authorize?client_id=790526190749745192&permissions=2048&scope=bot  
4tccc server: https://discord.gg/Gapyp6kw3b  

### bug reports:
open up an issue on github or message me on discord  

### commands:
note that * means that the parameter is optional  

__help command:__  
usage: !help \*command_name  
using help with no parametres will give you a generalised help message  
using with a command name will give you help using that specific command  

__submit command:__  
usage: !submit code \*name  
used for submitting 4tccc challenge codes  
name is only optional if you have already set an alias using the !alias command  
tralining spaces are removed when discord messages are sent, so names can't contain them either  

__submissions command:__  
usage: !submissions \*name  
with no parametres you ca see all the past submissions  
you can include a name to see submissions only from a specific person  

__find command:__  
usage: !find \*towers  
towers represents 4 seperate tower parametres  
you can search with 0-4 different towers  
searching with no towers shows all of the remaining combos  

__alias command:__  
usage: !alias name  
this command is used so you can omit name in the submit function  
names are stored per discord user, you can only have 1 copy of each name, so if you want to submit with an alt you will need to put your name in
if a player existing in the leaderboard sets thier name to be wrong, they will need admins to fix this as allowing people to change there names to any existing person would be disastrous

__leaderboard command:__  
usage: !leaderboard \*"name" \*amount  
aliases: lb  
using without will return the whole leaderboard  
using with name will give you the points of a player  
using with amount will shorten the leaderboard to amount 

__bot command:__  
usage: !bot  
shows bot invite link  

__server command:__  
usage: !server  
shows 4tccc server invite link  

commands are set to ignore things past the last arguement, but the name arguements can have spaces so anything after a name will be part of the name  
discord has a character per message limit of 2000 so any message after that is sent as a hastebin link instead, this also keeps chats cleaner  
