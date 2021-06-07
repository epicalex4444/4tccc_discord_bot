# 4tccc_discord_bot
4 towers chimps community challenge is a challenge in which  
you find and complete chimps with 4 or less towers,   
to find things that haven't been done you use the !find command  
once you have completed a challenge you must get it's challenge code  
and submit it with the !submit command, this command also requires you  
have a name which you can set with the !name command  

### rules:
submissions must have a challenge code  
the challenge must be a regular chimps game  
except that you can only have a max of 4 towers  

### invites:
bot invite: https://discord.com/api/oauth2/authorize?client_id=790526190749745192&permissions=2048&scope=bot  
4tccc server: https://discord.gg/Gapyp6kw3b  

### bug reports:
open up an issue on github or message epicalex4444#5552 on discord  

### commands:
note that * means that the parameter is optional  

__help command:__  
usage: !help \*command_name  
shows general help message or how to use a specific command  

__submit command:__  
usage: !submit code \*name  
used to submit a combo, name is required if you haven't specified your name with !name  

__submissions command:__  
usage: !submissions \*name  
finds all submissions or submissions from name  

__find command:__  
usage: !find \*towers  
finds all the combos remaining that have all of the specified towers  

__name command:__  
usage: !name name  
used to specify an name so you don't have to use the name parameter in submit  

__leaderboard command:__  
usage: !leaderboard \*"name" \*amount  
aliases: lb  
shows the leaderboard  

__towerlb command:__
usage: !towerlb  
shows how many combos each tower has left  

__bot command:__  
usage: !bot  
shows bot invite link  

__server command:__  
usage: !server  
shows 4tccc server invite link  

### misc:
commands are set to ignore things past the last arguement  
name arguements can have spaces but they can't start or end with spaces because discord removes them  
discord has a message limit of 2000 charecters so any message after that is sent as a webpage link instead  
