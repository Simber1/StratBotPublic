import discord
from discord.ext import commands
import random
from gsheet import Sheet
import datetime
# import asyncio

print(discord.version_info)
token = open("token.txt","r").readline()
#This should work? If not, idk
client = commands.Bot(command_prefix='!', case_insensitive=True, description='memer strat bot.')
client.remove_command('help')

UPDATE_RATE=30 #Minutes between updates

sheet = Sheet()
stratDatabase = sheet.get_table()

ARG_BINDINGS = {} #ARG_BINDINGS is a dictionary that binds command values to the search filters
INV_BINDS = {} # Inverse of ARG_BINDINGS. Mainly used for displaying valid commands
# Bind all values to point to the given key
def bind_opts(key, values):
	global ARG_BINDINGS
	global INV_BINDS
	INV_BINDS[key] = values
	ARG_BINDINGS.update({k: key for k in values})

ATK_KEY = "Attackers"
DEF_KEY = "Defenders"
CSTR_KEY = "C-Store"
FAC_KEY = "Factory"
KILL_KEY = "Killhouse"

TEAM_KEYS = [ATK_KEY, DEF_KEY]
TILE_KEYS = [CSTR_KEY, FAC_KEY, KILL_KEY]

bind_opts(ATK_KEY, ['a','attack','attk','atk','attackers'])
bind_opts(DEF_KEY, ['d','defender','def','crim','t'])
bind_opts(CSTR_KEY, ['c','cs','cstore','store'])
bind_opts(FAC_KEY, ['factory','f','fac'])
bind_opts(KILL_KEY, ['k','kh','kill','killhouse'])

last_update = datetime.datetime.now()
def update_if_needed(database):
	global last_update
	now = datetime.datetime.now()
	if (now - last_update).total_seconds() > UPDATE_RATE*60:
		print("Updating database")
		last_update = now
		return sheet.get_table()
	else:
		return database 


@client.event
async def on_ready():
	print("We have logged in as {0.user}".format(client))

@client.command()
async def strat(ctx,*args):

	global stratDatabase
	stratDatabase = update_if_needed(stratDatabase)
	i = 0
	while i < len(args):
		if args[i] == "help":
			valid_teams = ", ".join("%s: %s" % (key, str(INV_BINDS[key])) for key in TEAM_KEYS)
			valid_tiles = ", ".join("%s: %s" % (key, str(INV_BINDS[key])) for key in TILE_KEYS)
			await ctx.send("Bot Made by Simber, CADMonkey and Mailstorm.\n Source is available at https://github.com/Simber1/StratBotPublic.\n Valid arguments for team names are:\n`"+ valid_teams +"`\n\nValid arguments for tilesets are:\n`"+valid_tiles+"`")
			return
		i = i + 1

	try:
		filters = set(ARG_BINDINGS[arg] for arg in args) # Parse the options into filters. A set is used to prevent duplicates
	except KeyError:
		valid_teams = ", ".join("%s: %s" % (key, str(INV_BINDS[key])) for key in TEAM_KEYS)
		valid_tiles = ", ".join("%s: %s" % (key, str(INV_BINDS[key])) for key in TILE_KEYS)
		await ctx.send("You did not enter valid arguments. Valid arguments for team names are:\n`"+ valid_teams +"`\n\nValid arguments for tilesets are:\n`"+valid_tiles+"`")
		return

	if len(filters) != len(args):
		await ctx.send("Duplicate arguments provided. Please only specify up to one team and tileset.")
		return 

	if len(filters.intersection(TEAM_KEYS)) > 1:
		await ctx.send("Multiple Teams Specified. Only specify up to one team.")
		return
	
	if len(filters.intersection(TILE_KEYS)) > 1:
		await ctx.send("Multiple Tilesets Specified. Only Specify up to one tileset")
		return

	validNum = randomGen(filters)
	await ctx.send(embed=post(validNum))
	return
	

def randomGen(filters):
	while True:
		num = random.randint(0,len(stratDatabase))
		valid = True
		for f in filters:
			if(f in TEAM_KEYS) and not stratDatabase[num][2] in [f, "Both"]:
				valid = False
			elif (f in TILE_KEYS) and not stratDatabase[num][3] in [f, "All"]:
				valid = False
		if valid:
			return num

def post(number):
	embed = discord.Embed(title="Title", description=stratDatabase[number][0], color=0x04ddfe)
	embed.add_field(name="Description", value=stratDatabase[number][1], inline=False)
	embed.add_field(name="Team", value=stratDatabase[number][2], inline=False)
	embed.add_field(name="TileSet", value=stratDatabase[number][3], inline=False)
	return embed

client.run(token.strip())
