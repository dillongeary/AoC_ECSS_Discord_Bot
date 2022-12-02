import discord
import requests
import json
import asyncio

TOKEN = open(".token","r").read()
ID = open(".guildid","r").read()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
def generateLeaderboard():
    URL = "https://adventofcode.com/2022/leaderboard/private/view/1667828.json"
    headers = {"cookie":"session=53616c7465645f5f9ab8a65ad69679c5f98977388ba2e108cd099a58c3de60865065ff96f1dffb6f50da0dae3566537016c1454a62c41d08b068c2747bad98bf","Accept":'application/xhtml+xml'}
    r = requests.get(URL,headers = headers)

    aocdict = r.json()
    memberInfo = aocdict["members"]

    leaderboard = {}

    for x in memberInfo:
        personInfo = memberInfo[x]
        name = personInfo["name"]
        score = personInfo["local_score"]
        if score != 0:
            leaderboard.update({name:score})

    leaderboard = {k: v for k, v in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)}

    prettyPrint = "```\nRank | Score | Name\n-----|-------|---------------------\n"
    i = 1

    for name in leaderboard:
        score = leaderboard[name]
        string = "{:02d}".format(i) + ")  |  " + "{:03d}".format(score) + "  | " + name + "\n"
        prettyPrint+= string
        i+=1

    prettyPrint+="```"

    return prettyPrint


@client.event
async def on_ready():
    channel = client.get_channel(int(ID))
    message = await channel.send(generateLeaderboard())
    while True:
        await asyncio.sleep(900)
        await message.edit(content=generateLeaderboard())

client.run(TOKEN)