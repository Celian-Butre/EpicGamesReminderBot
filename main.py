

# bot.py
import os

import discord
from discord.ext import commands

from dotenv import load_dotenv

from datetime import datetime, timedelta
from date_time_event import Untiltime

import threading
import asyncio

from EpicAPI import *

import discord,asyncio,os
from discord.ext import commands, tasks







subscribedFile = "subscribedFile.txt"
alreadyAnnouncedGames = "announcedGames.txt"
messageGameAssociation = "MessageGameAssociation.txt"

TOKEN = #put your bots Token here
BotId = #put your bots id here
intents = discord.Intents.all()
#client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="?",intents=intents)

def decodeBackup(backup):
    with open(backup) as f:
        text = f.read()
    textByUsers = text.split("\n")
    textByUsersByStat = []
    for x in textByUsers:
        textByUsersByStat.append(x.split(";"))

    categories = textByUsersByStat.pop(0)
    listOfUsers = []
    for x in textByUsersByStat:
        listOfUsers.append({})
        for y in range(len(x)):
            listOfUsers[-1][categories[y]] = x[y]
    return(listOfUsers, categories)

def uploadToBackup(modifiedBackup, categories, backup):
    modifiedBackupString = ""
    for x in categories:
        modifiedBackupString += x
        modifiedBackupString += ";"
    modifiedBackupString = modifiedBackupString[:-1]
    modifiedBackupString += "\n"
    for x in modifiedBackup:
        for y in x:
            modifiedBackupString += x[y]
            modifiedBackupString += ";"
        modifiedBackupString = modifiedBackupString[:-1]
        modifiedBackupString += "\n"
    modifiedBackupString = modifiedBackupString[:-1]
    with open(backup, 'w') as f:
        f.write(modifiedBackupString)
    return(backup)

@bot.command(name = "opt-in", help = "opt-in the author of the command, they will receive messages when new games are free on the Epic Games store")
async def optingIn(ctx):
    global subscribedFile
    users, categories = decodeBackup(subscribedFile)
    #print(1, ctx.message)
    username = str(ctx.message.author) #DiscordId#0000
    ID = str(ctx.message.author.id) #randomUniqueNumbers
    for x in users:
        if x["ID"] == ID:
            if x["username"] != username: #to change outdated username
                x["username"] = username
                await ctx.send(str(username+ ", it seems you used to be registered under a different username, I have updated my database to match your ID with your new username."))
            if x["in or out"] == "in": #if there is nothing to change
                await ctx.send(str(username+ ", it seems you are already opt-in for new Epic Games free games notifications, I have not modified your opt-in status."))
            elif x["in or out"] == "out": #if there is something to change
                x["in or out"] = "in"
                await ctx.send(str(username+ ", you are now opt-in to receive new Epic Games free games notifications!"))
            subscribedFile = uploadToBackup(users, categories, subscribedFile)
            return
    users.append({"ID": ID, "username" : username, "saved money" : "000", "in or out" : "in", "bought games" : "Cookie Clicker (easter egg)"})
    await ctx.send(str(username+ ", it seems like you aren't part of my database, so I created a profile for you, you are opt-in by default!")) #to add the user if they aren't part of the database
    subscribedFile = uploadToBackup(users, categories, subscribedFile)
    return

@bot.command(name = "opt-out", help = "opt-out the author of the command, they will no longer receive messages when new games are free on the Epic Games store")
async def optingOut(ctx): #mirror image of optingIn
    global subscribedFile
    users, categories = decodeBackup(subscribedFile)
    #print(1, ctx.message)
    username = str(ctx.message.author) #DiscordID#0000
    ID = str(ctx.message.author.id) #randomUniqueNumbers
    for x in users:
        if x["ID"] == ID:
            if x["username"] != username:
                x["username"] = username
                await ctx.send(str(username+ ", it seems you used to be registered under a different username, I have updated my database to match your ID with your new username."))
            if x["in or out"] == "out":
                await ctx.send(str(username+ ", it seems you are already opt-out and do not recieve new Epic Games free games notifications, I have not modified your opt-out status."))
            elif x["in or out"] == "in":
                x["in or out"] = "out"
                await ctx.send(str(username+ ", you are now opt-out and will no longer receive new Epic Games free games notifications!"))
            subscribedFile = uploadToBackup(users, categories, subscribedFile)
            return
    users.append({"ID": ID, "username" : username, "saved money" : "0", "in or out" : "out"})
    await ctx.send(str(username+ ", it seems like you aren't part of my database, so I created a profile for you, you are opt-out by default!"))
    subscribedFile = uploadToBackup(users, categories, subscribedFile)
    return

@bot.command(name = "leaderboard", help = "shows the top 10 worldwide leaderboard of the people who have saved the most money on Epic Games games thanks to this awesome bot")
async def leaderboard(ctx):
    global subscribedFile
    users, categories = decodeBackup(subscribedFile)
    #Selection sort to sort the players by money saved
    guildUsers = []
    for x in users:
    	if x['ID'] != '':
    		guildUsers.append(x)
    for i in range(len(guildUsers)):
        minimum = guildUsers[i]
        posmin = i
        for j in range(i,len(guildUsers)):
            if int(minimum["saved money"]) > int(guildUsers[j]["saved money"]):
                minimum = guildUsers[j]
                posmin = j
                save = guildUsers[i]
                guildUsers[i] = guildUsers[posmin]
                guildUsers[posmin] = save
    leaderboardString = ""
    for i in range(1,min(11,len(guildUsers)+1)):
        leaderboardString += str(guildUsers[-i]["username"] +"\t : \t" + guildUsers[-i]["saved money"] + "\n")

    await ctx.send(leaderboardString[:-1])
    return


@bot.command(name = "guild-leaderboard", help = "shows the top 10 guild leaderboard of the people who have saved the most money on Epic Games games thanks to this awesome bot")
async def guildLeaderboard(ctx):
    global subscribedFile
    GUILD = ctx.guild

    users, categories = decodeBackup(subscribedFile)

    members = [str(member.id) for member in GUILD.members]
    #print(members)

    #make a users with only guild people

    guildUsers = []
    for x in users:
        if x["ID"] in members:
            guildUsers.append(x)

    #Selection sort to sort the players by money saved
    for i in range(len(guildUsers)):
        minimum = guildUsers[i]
        posmin = i
        for j in range(i,len(guildUsers)):
            if int(minimum["saved money"]) > int(guildUsers[j]["saved money"]):
                minimum = guildUsers[j]
                posmin = j
                save = guildUsers[i]
                guildUsers[i] = guildUsers[posmin]
                guildUsers[posmin] = save
    leaderboardString = ""
    for i in range(1,min(11,len(guildUsers)+1)):
        leaderboardString += str(guildUsers[-i]["username"] +"\t : \t" + guildUsers[-i]["saved money"] + "\n")

    await ctx.send(leaderboardString[:-1])
    return

#dummy command to see if bot responds
@bot.command(name = "ping")
async def pingTest(ctx):
    await ctx.send("pong 🏓")
    return
    
@bot.command(name = "pong")
async def pingTest(ctx):
    await ctx.send("ping 🏓")
    return

@bot.command(name = "my-savings", help = "shows how much money you have saved on Epic Games games thanks to this awesome bot")
async def mySavings(ctx):
    global subscribedFile
    users, categories = decodeBackup(subscribedFile)
    user = ctx.author
    for x in users:
        if x["ID"] == str(user.id):
            money = x["saved money"]
            money = money[:-2]+"."+money[-2:]
            await ctx.send(str("You have saved $"+ money + " with this awesome bot"))
            return
    await ctx.send(str("you do not have an account yet, use ?opt-in to create one"))



@bot.event
async def on_ready():
    checkStore.start()
    print(str(str(bot.user) + " is connected"))


@tasks.loop(seconds = 3600)
async def checkStore():
    global subscribedFile, alreadyAnnouncedGames
    gamesList = getGamesList()
    oldGamesList = []
    with open(alreadyAnnouncedGames) as f:
        text = f.read()
    oldGamesList = text.split("\n")
    list(filter(("").__ne__, oldGamesList))
    #print(oldGamesList)
    for x in gamesList:
        if not(x.title in oldGamesList):
            oldGamesList.append(x.title)
            #print(1)
            await sendAnnouncement(x)
            #print(2)
            with open(alreadyAnnouncedGames, 'w') as f:
                message = ''
                for y in oldGamesList:
                    message += (y+"\n")
                message = message[:-1]
                f.write(message)


async def sendAnnouncement(game):
    #print(3)
    treatedMember = []
    global subscribedFile, messageGameAssociation
    users, categories = decodeBackup(subscribedFile)
    for Guild in bot.guilds:
        for member in Guild.members:
            if not(member in treatedMember):
                treatedMember.append(member)
                for x in users:
                    #print(x["ID"], member.id)
                    if x["ID"] == str(member.id) and x["in or out"] == "in":
                        #print(4)
                        await member.create_dm()
                        message = await member.dm_channel.send(str(str(game) + "\nReact to this message with 🎉 once you have purchased the game for free"))
                        await message.add_reaction("🎉")
                        #adding message to list of messages
                        with open(messageGameAssociation, 'a') as f:
                            f.write(str("\n" + str(message.id)+ ";" + str(game.id) + ";"+ str(game.title) + ";" + str(game.savings)))
                        #message.attachments = [game.savings, game.title]

                        #print(5)


@bot.event
async def on_reaction_add(reaction, user):
    global messageGameAssociation, subscribedFile
    message = reaction.message
    if str(user.id) != BotId:
        messages, messageCategories = decodeBackup(messageGameAssociation)
        for x in messages:
            if x["messageID"] == str(message.id):
                gameTitle, savedMoney = x["gameTitle"], x["savedMoney"]

        users, categories = decodeBackup(subscribedFile)
        for x in users:
            if str(user.id) == x["ID"]:
                if not(gameTitle in x["bought games"].split("-_-")):
                    if x["bought games"].split("-_-") == ['']:
                        x["bought games"] += str(gameTitle)
                    else:
                        x["bought games"] += str("-_-" + str(gameTitle))
                    x["saved money"] = str(int(x["saved money"]) + int(savedMoney))
        subscribedFile = uploadToBackup(users, categories, subscribedFile)

bot.run(TOKEN)
#@client.event

#on_reaction_add

#client.run(TOKEN)
