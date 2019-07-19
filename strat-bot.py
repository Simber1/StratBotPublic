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

#Let this command be run by people with the Testers role only.	
@client.command()
@commands.has_role('Testers')
async def strat(ctx,*args):
	#Not sure why this is global but I kept it because who knows.
	global stratDatabase
	stratDatabase = update_if_needed(stratDatabase)
	#I got tired of scrolling. Add your options here
	team_options_a = ['a','attack','attk','atk','attackers']
	team_options_d = ['d','defender','def','crim','t']
	tile_options_c = ['c','cs','cstore','store']
	tile_options_f = ['factory','f','fac']
	tile_options_k = ['k','kill','killhouse']
	teams_merged = team_options_a + team_options_d
	tiles_merged = tile_options_c + tile_options_f + tile_options_k
	#No arguments provided. Default to random.
	if len(args) == 0:
		validNum = randomGen("Both","All")
		await ctx.send(embed=post(validNum))
		return
	
	#One argument provided, check to see if it's a tile
	elif len(args) == 1 and args[0].lower() in tiles_merged:
		tile = args[0].lower()
		#A bunch of if's to determine what tile should be posted.
		if tile in tile_options_c:
			validNum = randomGen('Both',"C-Store")
			await ctx.send(embed=post(validNum))
			return
		if tile in tile_options_f:
			validNum = randomGen('Both',"Factory")
			await ctx.send(embed=post(validNum))
			return
		if tile in tile_options_k:
			validNum = randomGen('Both',"Killhouse")
			await ctx.send(embed=post(validNum))
			return

	#Like above, but for teams if this is the only argument passed
	elif len(args) == 1 and args[0].lower() in teams_merged:
		team = args[0].lower()
		if team in team_options_a:
			validNum = randomGen("Attackers","All")
			await ctx.send(embed=post(validNum))
			return
		else:
			validNum = randomGen("Defenders","All")
			await ctx.send(embed=post(validNum))
			return
		
	#tile was first argument, team was second
	elif len(args) == 2 and args[0].lower() in tiles_merged and args[1].lower() in teams_merged:
		tile = args[0].lower()
		team = args[1].lower()
		if tile in tile_options_c:
			if team in team_options_a:
				validNum = randomGen("Attackers","C-Store")
				await ctx.send(embed=post(validNum))
				return
			else:
				validNum = randomGen("Defenders","C-Store")
				await ctx.send(embed=post(validNum))
				return
		elif tile in tile_options_f:
			if team in team_options_a:
				validNum = randomGen("Attackers","Factory")
				await ctx.send(embed=post(validNum))
				return
			else:
				validNum = randomGen("Defenders","Factory")
				await ctx.send(embed=post(validNum))
				return
		elif tile in tile_options_k:
			if team in team_options_a:
				validNum = randomGen("Attackers","Killhouse")
				await ctx.send(embed=post(validNum))
				return
			else:
				validNum = randomGen("Defenders","Killhouse")
				await ctx.send(embed=post(validNum))
				return
			
	#Same as above, but team was the first argument and tile was second
	elif len(args) == 2 and args[1] in tiles_merged and args[0] in teams_merged:
		tile = args[1].lower()
		team = args[0].lower()
		if tile in tile_options_c:
			if team in team_options_a:
				validNum = randomGen("Attackers","C-Store")
				await ctx.send(embed=post(validNum))
				return
			else:
				validNum = randomGen("Defenders","C-Store")
				await ctx.send(embed=post(validNum))
				return
		elif tile in tile_options_f:
			if team in team_options_a:
				validNum = randomGen("Attackers","Factory")
				await ctx.send(embed=post(validNum))
				return
			else:
				validNum = randomGen("Defenders","Factory")
				await ctx.send(embed=post(validNum))
				return
		elif tile in tile_options_k:
			if team in team_options_a:
				validNum = randomGen("Attackers","Killhouse")
				await ctx.send(embed=post(validNum))
				return
			else:
				validNum = randomGen("Defenders","Killhouse")
				await ctx.send(embed=post(validNum))
				return
	#No need to check to see if the amount of args provided is above 2 since we just wont use them. Also not caring how the list looks when posted.
	else:
		await ctx.send("You did not enter valid arguments. Valid arguments for team names are:\n`"+str(teams_merged)+"`\n\nValid arguments for tilesets are:\n`"+str(tiles_merged)+"`")
	return	


def randomGen(team,tileset):
	num = random.randint(0,len(stratDatabase))
	if team == "Both":
		return num

	if (not "Both" in stratDatabase[num][2]) and (not team in stratDatabase[num][2]):
		return False

	if (not "All" in stratDatabase[num][3]) and (not tileset in stratDatabase[num][3]):
		return False
	
	return num


	#random number gen from 1 to length of list
	#check the team is right, return false if not
	#check the tileset is right, return false if not
	#return number

def post(number):
	embed = discord.Embed(title="Title", description=stratDatabase[number][0], color=0x04ddfe)
	embed.add_field(name="Description", value=stratDatabase[number][1], inline=False)
	embed.add_field(name="Team", value=stratDatabase[number][2], inline=False)
	embed.add_field(name="TileSet", value=stratDatabase[number][3], inline=False)
	return embed


def attacker(message):
	if "atk" in message:
		return True
	if "attack" in message:
		return True
	if "cop" in message:
		return True
	return False

def defender(message):
	if "crim" in message:
		return True
	if "def" in message:
		return True
	return False

def cstore(message):
	if "cs" in message:
		return True
	return False

def factory(message):
	if "fac" in message:
		return True
	return False

def killhouse(message):
	if "kill" in message:
		return True
	if "kh" in message:
		return True
	return False


client.run(token.strip())
