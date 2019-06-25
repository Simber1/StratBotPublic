import discord
import random
from gsheet import Sheet
import datetime

print(discord.version_info)

client = discord.Client()
user = []
voices = []

token = open("token.txt","r").readline()

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

@client.event
async def on_message(message):
	global stratDatabase
	messageStr = message.content
	messageStr = messageStr.lower()

	if message.author == client.user:
		return


	if message.content.startswith("!strat"): #Checking if strat
		stratDatabase = update_if_needed(stratDatabase)
		validNum = False
		if attacker(messageStr):   #Checking if Attacker
			if cstore(messageStr):
				while validNum == False:
					validNum = randomGen("Attackers","C-Store")
				await message.channel.send(embed=post(validNum)) #Attacker CS
				print("att cs")
				return

			if factory(messageStr):
				while validNum == False:
					validNum = randomGen("Attackers","Factory")        		
				await message.channel.send(embed=post(validNum)) #Attacker Factory
				print("att fac")
				return

			if killhouse(messageStr):
				while validNum == False:
					validNum = randomGen("Attackers","Killhouse")

				await message.channel.send(embed=post(validNum)) #Attacker Killhouse
				print("att kh")
				return



		if defender(messageStr):   #Checking if Defender
			if cstore(messageStr):
				while validNum == False:
					validNum = randomGen("Defenders","C-store")
				
				await message.channel.send(embed=post(validNum)) #Defender CS
				print("def cs")
				return

			if factory(messageStr):
				while validNum == False:
					validNum = randomGen("Defenders","Factory")

				await message.channel.send(embed=post(validNum)) #Defender Factory
				print("def fac")
				return

			if killhouse(messageStr):
				
				while validNum == False:
					validNum = randomGen("Defenders","Killhouse")
					
				await message.channel.send(embed=post(validNum)) #Defender Killhouse
				print("def kh")
				return

		validNum = randomGen("Both","All")
		await message.channel.send(embed=post(validNum))
		print("general")



	if message.content.startswith("!help"):
		await message.channel.send("`!strat [team] [tile set]`. \n You can do just `!strat` for a general strat, or specify both a team and a tileset which can give you a strat for the map or the team.")
		


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