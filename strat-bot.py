import discord
import random

client = discord.Client()
user = []
voices = []

stratsFile = open("strat-source.tsv")
token = open("token.txt","r").readline()

stratDatabase = [line.split('\t')[:4] for line in stratsFile.readlines()]



@client.event
async def on_ready():
	print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):

	messageStr = message.content
	messageStr = messageStr.lower()

	if message.author == client.user:
		return

	if message.content.startswith("!quit"):
		await message.channel.send("Quiting!")
		exit()

	if message.content.startswith("!strat"): #Checking if strat
		validNum = False

		if attacker(messageStr):   #Checking if Attacker
			if cstore(messageStr):
				while validNum == False:
					validNum = randomGen("Attackers","C-Store")
				await message.channel.send(embed=post(validNum)) #Attacker CS
				return

			if factory(messageStr):
				while validNum == False:
					validNum = randomGen("Attackers","Factory")        		
				await message.channel.send(embed=post(validNum)) #Attacker Factory
				return

			if killhouse(messageStr):
				while validNum == False:
					validNum = randomGen("Attackers","Killhouse")

				await message.channel.send(embed=post(validNum)) #Attacker Killhouse
				return



		if defender(messageStr):   #Checking if Defender
			if cstore(messageStr):
				while validNum == False:
					validNum = randomGen("Defenders","C-store")
				
				await message.channel.send(embed=post(validNum)) #Defender CS
				return

			if factory(messageStr):
				while validNum == False:
					validNum = randomGen("Defenders","Factory")

				await message.channel.send(embed=post(validNum)) #Defender Factory
				return

			if killhouse(messageStr):
				
				while validNum == False:
					validNum = randomGen("Defenders","Killhouse")
					
				await message.channel.send(embed=post(validNum)) #Defender Killhouse
				return

	validNum = randomGen("Both","All")
	await message.channel.send(embed=post(validNum))



	if message.content.startswith("!list"):
		await message.channel.send(stratDatabase[0][1])
		


def randomGen(team,tileset):
	num = random.randint(1,len(stratDatabase))
	if team == "Both":
		return num

	if (not "Both" in stratDatabase[num][2]) and (not team in stratDatabase[num][2]):
		print(num)
		print("Failed Team")
		return False

	if (not "All" in stratDatabase[num][3]) and (not tileset not in stratDatabase[num][3]):
		print(num)
		print("Failed map")
		return False
	return num


	#random number gen from 1 to length of list
	#check the team is right, return false if not
	#check the tileset is right, return false if not
	#return number

def post(number):
	embed = discord.Embed(title="Title", description=stratDatabase[number][0], color=0x04ddfe)
	embed.add_field(name="Desc", value=stratDatabase[number][1], inline=False)
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