import sys

import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
# from discord.ext.commands import has_permissions, MissingPermissions
import random
import os
import shutil
#import youtube_dl
import yt_dlp
import platform
import asyncio
from datetime import datetime
from mcstatus import JavaServer
import socket
from discord import Interaction, app_commands

prefix = "C."
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)

convertRole = "Ditto"
maxNum = 100
spamMaxNum = 10000
developer = "Scarlet_blue72"
folderYT = "youtube"
folderQueue = "queue"
folderTech = "tech"
folderAudio = "genAudio"
folderMisc = "misc"
folderServers = "servers"
folderUserData = "userData"
folderSlash = "/"
queue = {}
pesterPeople = {}
pesterChance = 50
dmTriggerKeywords = {}
keywordResponses = {}
# This data splitter is used to parse through text data, with it being an identifying unique symbol
dataSplitter = ":::"


# Just saying "pass" in a method breaks the bot. Don't leave methods blank
# If something doesn't work:
#   make sure methods have async
#   make sure method calls have await
#   check error handling methods 

# Make folder structure based on server and have file related to that inside (roles, people, etc) -DONE
# Random gif picker that people will add to -DONE
# Have a game where ppl are randomly killed off until one remains -DONE
# have a betting system on whos gonna live
# Optimize the adding and removing to file methods -DONE

# add rpg game integration
@client.event
async def on_ready():
    global path
    global folderSlash
    global lastAudio
    print(platform.system())
    if platform.system() == "Windows":
        folderSlash = "\\"
        # await client.change_presence(activity=discord.Activity(type = discord.ActivityType.custom, name="under maintenance"))
    # path = os.getcwd()+folderSlash
    path = os.getcwd() + folderSlash
    # await setFolder(folderYT+folderQueue)
    # await setFolder(folderAudio)
    print(path)
    print("Online")


@client.command()
async def botOnline(ctx):
    if ctx.author.name == developer:
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="the world burn"))
        servers = client.guilds
        for s in servers:
            for c in s.channels:
                if c.name.count("bot") == 1:
                    await c.send("I am online now")
        await ctx.send("Notfied servers")

    else:
        await ctx.send("Only my master can use this command")


@client.event
async def on_message(message):
    print(f"\n{message.author} from {message.channel} in the server {message.guild} says:\n\"{message.content}\"\n")
    if not message.author.name == client.user.name:
        if message.author.bot:
            await message.channel.send(f"Hey {message.author.mention}, I'm the best bot")
        else:
            # only a chance for this one
            pester = random.randint(1, pesterChance)
            m = message.content.lower()
            if pester == 1:
                for person in pesterPeople:
                    if message.author.name == person:
                        await message.channel.send(pesterPeople[person])
            for word in dmTriggerKeywords:
                if word in m:
                    await message.channel.send(f"You made a bad joke, we taking this to dm's {message.author.mention}")
                    await message.author.send(dmTriggerKeywords[word])
            for keyword in keywordResponses:
                m = m.strip()
                if keyword in m:
                    # do an additional check to see if the word is embedded in another word (ex eachother has "hot" in it so itll respond)
                    preIndex = m[m.index(keyword) - 1]
                    # make sure there isnt an index out of range for the pos index
                    try:
                        postIndex = m[m.index(keyword) + len(keyword)]
                    except:
                        postIndex = m[m.index(keyword) + len(keyword) - 1]
                    print("pre:" + preIndex + ": post:" + postIndex + ":")
                    if preIndex == " " or keyword == m or postIndex == " " or m.index(keyword) - 1 < 0:
                        # if there's a negative index, that means the keyword is at the very beginning
                        await message.channel.send(keywordResponses[keyword])
    process = await client.process_commands(message)
    # if process == 1:
    # add points here when someone uses a command
    # This is VERY IMPORTANT. No commands will be avaliable if this line isnt here

@client.command()
async def addPester(ctx, member: discord.Member, response):
    pesterPeople[member.name] = response
    await ctx.send(f"Watch out {member.name}, I'm listening")

@client.command()
async def addDmTrigger(ctx, word, response):
    dmTriggerKeywords[word] = response
    await ctx.send(f"Listening for \"{word}\" and will send a direct message!")

@client.command()
async def addKeywordTrigger(ctx, word, response):
    keywordResponses[word] = response
    await ctx.send(f"Listening for \"{word}\"")

@client.command()
async def intro(ctx):
    await ctx.send("THE DAY HAS COME MY BRETHREN FOR I, QUAZI CLONE, WILL BAN YOU ALL")


@client.tree.command()
async def testslash(interaction: Interaction):
    await interaction.response.send_message("Testy")


@client.command()
async def showCustomEmojis(ctx):
    emojis = ctx.guild.emojis
    for emote in emojis:
        await ctx.send(emote)


@client.command(aliases=["mcServer", "mcserver"])
async def minecraftServer(ctx):
    await ctx.send("Fetching server info")
    try:
        if platform.system() == "Windows":
            server = JavaServer.lookup("localhost")
        else:
            server = JavaServer.lookup("")
        status = server.status()
        onlinePlayers = status.players.sample
        textPlayerList = ""
        if status.players.online > 0:
            for p in onlinePlayers:
                textPlayerList += p.name+" "
        await ctx.send(f"The server is online with {status.players.online} player(s) online.\n{textPlayerList}\n({status.latency} ms reply speed)")
    except ConnectionRefusedError:
        await ctx.send("The server is not online: refused connection")
    except socket.timeout:
        await ctx.send("The server is not online")
'''
@client.command()
async def setTimer(ctx, t, message="Time is up!"):
    # i think this one is currently broken :(
    if ":" in t:
        # parse through the string to find exact amount of seconds to wait
        now = datetime.now()
        tempList = t.split(":")
        hms = []
        for unit in tempList:
            hms.append(int(unit))
        print(hms)
        print(f"{now.hour} {now.minute} {now.second}")
        # FIX: check for negatives
        if hms[2] - now.second < 0:
            secTaken = 60 - now.second + hms[2]
            hms[1] -= 1
            print("fix")
        else:
            secTaken = hms[2] - now.second
        t = secTaken

        if hms[1] - now.minute < 0:
            minTaken = (60 - now.minute + hms[1])
            hms[0] -= 1
            print("fix")
        else:
            minTaken = (hms[1] - now.minute)
        t += minTaken * 60

        if hms[0] - now.hour < 0:
            hrTaken = (24 - now.hour + hms[0])
            print("fix")
        else:
            hrTaken = (hms[0] - now.hour)
        t += hrTaken * 120
        # check hours and min first cuz for ex 19:00:10 timer set at 18:58:8 is calculated to have to wait 2 minutes and 2 sec (should be 2 minutes and 62 seconds --> 3 minutes and 2)
        await ctx.send(f"Waiting for {hrTaken} hours, {minTaken} minutes and {secTaken} seconds")
    else:
        t = int(t)
        await ctx.send(f"Waiting for {t} seconds")
    await ctx.send(f"Waiting for {t} seconds")
    print(t)
    await asyncio.sleep(t)
    await ctx.send(message)
'''

@client.command()
async def increasePester(ctx, amount):
    global pesterChance
    pesterChance -= int(amount)
    if pesterChance < 1:
        pesterChance = 1
    await ctx.send("The new chance is 1 in " + str(pesterChance))


@client.command()
async def teleportVC(ctx, member: discord.Member, amount=5):
    voiceChannels = ctx.guild.voice_channels
    for c in voiceChannels:
        print(c.name)
    i = 0
    while i < amount:
        chosenChannel = random.choice(voiceChannels)
        await member.move_to(chosenChannel)
        i += 1
    await ctx.send("Done with teleports")


@client.command()
async def rename(ctx, name):
    # await member.edit(nick=False)
    await ctx.guild.me.edit(nick=name)
    await ctx.send("WHY? " + name + " is so lame :/")


'''
@client.command()
async def createPoll(ctx, question, options):
    i=0
    textList = displayOptions(options.split(","))        
    await ctx.send(question+"\n"+textList)
    addItemFile(ctx, "polls.txt", question+":"+options)
@client.command()
async def viewPolls(ctx):
    rawPollData = getItemsFile(ctx,"polls.txt")
    polls = {}
    for dataset in rawPollData:
        print(dataset)
        temp = dataset.split(":")
        question = temp[0]
        textList = displayOptions(temp[1])
        await ctx.send(question+"\n"+textList)
def displayOptions(data):
    display = ""
    i = 0
    for d in data:
        i += 1
        display += str(i)+". "+d+" "
    return display
'''

def gifStructure(ctx, member, otherUserText, sameUserText, gifFile):
    # this is a standard for all gif commands. It will return a string response and a gif string
    response = ["", ""]
    items = getItemsFile(ctx, gifFile)
    if len(items) == 0:
        response[
            0] = "You need to add gifs to the bot for this command to work! Use the corresponding addGif command to do this"
        return response
    if not ctx.author == member:
        response[0] = otherUserText
    else:
        response[0] = sameUserText
    response[1] = random.choice(getItemsFile(ctx, gifFile))
    return response


@client.command()
async def wheelSpin(ctx, doSpinOptions="T", item="NONE"):
    '''
S: show options, +: add item, -: remove item (must specfiy and item also with +/-)
    '''
    doSpinOptions = doSpinOptions.upper()
    options = getItemsFile(ctx, "wheel.txt")
    if doSpinOptions == "+":
        addItemFile(ctx, "wheel.txt", item)
        await ctx.send("Added item entry")
    elif doSpinOptions == "-":
        removeItemFile(ctx, "wheel.txt", item)
        await ctx.send("Removed item")
    elif doSpinOptions == "S":
        text = ""
        for d in options:
            text += d
            if not options[len(options) - 1] == text:
                text += " "
        await ctx.send("Options:\n" + text)
    else:
        if len(options) == 0:
            await ctx.send("No options available")
        else:
            await ctx.send("------------------------\n" + random.choice(options))


# gif commands starts here
@client.command(aliases=["gifCategory", "sendGifC"])
async def sendGif(ctx, category="NONE"):
    '''
send a gif from a category
    '''
    if category == "NONE":
        possibleGifs = getItemsFile(ctx, "gifs.txt")
        if len(possibleGifs) == 0:
            await ctx.send("There are no gifs to send! Why not add some?")
        else:
            await ctx.send(random.choice(possibleGifs))
    else:
        rawData = getItemsFile(ctx, "gifCategory.txt")
        possibleGifs = []
        categoryList = []
        for d in rawData:
            currentData = d.split(dataSplitter)
            print(currentData)
            if currentData[1] == category:
                possibleGifs.append(currentData[0])
        if len(possibleGifs) == 0:
            await ctx.send("There is nothing in that category. Why don't you add a gif with the category " + category)
        else:
            await ctx.send(random.choice(possibleGifs))


@client.command(aliases=["addGifC"])
async def addGif(ctx, gif, category="NONE"):
    '''
add a gif alongside a category
    '''
    if category == "NONE":
        # Add gif to the corresponding server file
        addItemFile(ctx, "gifs.txt", gif)
        await ctx.send("Added gif")
    else:
        addItemFile(ctx, "gifCategory.txt", gif + dataSplitter + category)
        await ctx.send("Added gif")


@client.command(aliases=["viewGifs"])
async def viewGifCategories(ctx):
    '''
see all currently made categories
    '''
    rawData = getItemsFile(ctx, "gifCategory.txt")
    categoryList = []
    # parse through raw data
    for d in rawData:
        currentCata = d.split(dataSplitter)[1]
        print(currentCata)
        for c in categoryList:
            if c == currentCata:
                break
        else:
            categoryList.append(currentCata)
            await ctx.send(currentCata)

    await ctx.send("Thats all folks")


# end of gif commands

@client.command()
async def sup(ctx):
    await ctx.send("Sup nerd")

@client.command()
async def convert(ctx, member: discord.Member):
    await member.edit(nick=convertRole)
    displayName = ctx.author.nick
    if not displayName:
        displayName = ctx.author.name
    if member.name == convertRole:
        await ctx.send(f"This user is already a {convertRole}")
    else:
        await ctx.send(f"Hey {member.name}, {displayName} just made you a {convertRole}.")
    # test to see if the convert role exists or not. Create the role if not
    role = get(ctx.guild.roles, name=convertRole)
    if not get(ctx.guild.roles, name=convertRole):
        await ctx.guild.create_role(name=convertRole, mentionable=True)
    for r in member.roles:
        if r.name == convertRole:
            await ctx.send(f"{member.name} is already a {convertRole}!")
            break
    else:
        print("adding role")
        await member.add_roles(role)
        await ctx.send(f"{role.mention} you have a new member!")


@client.command()
async def unconvert(ctx, member: discord.Member):
    change = False
    for r in member.roles:
        if r.name == convertRole:
            contains = True
            break
        else:
            contains = False
    if member.nick == convertRole:
        await member.edit(nick=False)
        change = True
    if contains:
        await member.remove_roles(get(ctx.guild.roles, name=convertRole))
        change = True
    if change:
        await ctx.send(f"You have been cured {member.mention}")
    else:
        await ctx.send("This user has never been converted yet")


@client.command()
async def spam(ctx, member: discord.Member, amount=10):
    if await badSpamInput(amount):
        await ctx.send("That is wayyyyy to much")
        return
    maximum = maxNum
    if ctx.channel.name == "spam":
        i = spamMaxNum
    if amount > maximum:
        await ctx.channel.send(
            "Hold on buddy, that a little too much. The max is " + str(maxNum) + " spams in this channel.")
    else:
        i = 0
        while i < amount:
            await ctx.channel.send(member.mention)
            i += 1


@spam.error
async def spamError(ctx, error):
    if isinstance(error, commands.UserInputError):
        await ctx.send("You need to mention a user for this command. If you want to spam a word, use spamWord command")
        if ctx.author == "PineCone":
            await ctx.send("Alexii i know yur trying to break my code, smh")
    else:
        print("Something went very wrong")
        print(error)


@client.command(aliases=["spamword"])
async def spamWord(ctx, string, amount=10):
    if await badSpamInput(amount):
        await ctx.send("That is wayyyyy to much")
        return
    maximum = maxNum
    if ctx.channel.name == "spam":
        maximum = spamMaxNum
    if amount > maximum:
        await ctx.channel.send("Hold on buddy, that a little too much. The max is " + str(maxNum) + " spams.")
    else:
        i = 0
        while i < amount:
            await ctx.channel.send(string)
            i += 1


@spamWord.error
async def spamWordError(ctx, error):
    if isinstance(error, commands.UserInputError):
        await ctx.send("You need add a word for this command. If you want to spam a user, use the spam command")
        if ctx.author == "PineCone":
            await ctx.send("Alexii i know yur trying to break my code, smh")
    else:
        print("Something went very wrong")
        print(error)


@client.command()
async def moveAlong(ctx):
    await spamWord(ctx, "https://tenor.com/view/the-goon-star-wars-stormtrooper-move-along-move-gif-12464798")


async def badSpamInput(i):
    if i > 10000:
        return True
    else:
        return False


@client.command()
async def sendEmbed(ctx, content="TEXT HERE"):
    myEmbed = discord.Embed(description=content)
    await ctx.send(embed=myEmbed)


@client.command(aliases=["joinVC", "joinvoice", "joinvc", "joinVc"])
async def joinVoice(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("I'm in >:)")
    else:
        await ctx.send("Hop in a call so I can join dude, smh")


@client.command(aliases=["leaveVC", "leavevoice"])
async def leaveVoice(ctx):
    # check to see if bot in in a voice chat and disconnects if so
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Bye bye!")
    else:
        await ctx.send("Bro I\'m not even in a vc. Do you want me to leave that badly?")


@client.command(aliases=["voiceAt", "voiceTo", "VCat", "sendvoiceat"])
async def sendVoiceTo(ctx, member: discord.Member):
    if member.voice:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        await member.voice.channel.connect()
        await ctx.send("I'm in >:)")
    else:
        await ctx.send("That user isn't in a voice chat. I can\'t harrass them!")


@client.command(aliases=["playrandaudio", "randAudio", "randaudio", "playRand","playAudio"])
async def playRandAudio(ctx):
    if ctx.voice_client:
        audio = await getAudioFiles(folderAudio)
        # if there are no audio files, stop the command and tell the user
        if len(audio) == 0:
            await ctx.send("There are currently no audio files to play! Why dont you add some to play with the YouTube command?")
            return
        selectedAudio = random.choice(audio)
        print(selectedAudio)
        '''
        source = FFmpegPCMAudio(path + folderAudio + folderSlash + selectedAudio)
        voice = await setVoiceClient(ctx, ctx.author)
        voice.play(source)
        '''
        playSound(path + folderAudio + folderSlash + selectedAudio, await setVoiceClient(ctx, ctx.author))
        await ctx.send("Playing " + str(selectedAudio))
        # await AddToQueue(ctx, selectedAudio);
    else:
        await ctx.send("I need to be in a voice channel to do this!")


# This is a general audio playing method that will catch if FFmpeg is installed
def playSound(p, voiceClient):
    source = FFmpegPCMAudio(p)
    voiceClient.play(source)


@client.command(aliases=["attackvc", "attackVc"])
async def attackVC(ctx, member: discord.Member):
    if member.voice:
        voice = await setVoiceClient(ctx, member)
        source = FFmpegPCMAudio(path + folderAudio + folderSlash + "Lego yoda death sound.mp3")
        voice.play(source)
    else:
        await ctx.send("Not yet...")


@client.command(aliases=["stopPlaying", "stopvc", "svc"])
async def stopVC(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    else:
        await ctx.send("I am not saying anything!")


@client.command()
async def pauseVC(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("I am not saying anything!")


@client.command()
async def resumeVC(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("You have not paused anything")



@client.command(aliases=["youTube", "YouTube"])
async def youtube(ctx, url: str):
    # if not await FFmpegCheck(ctx):
    #    return
    voice = await setVoiceClient(ctx, ctx.author)
    await clearYoutube()
    if voice.is_playing():
        await ctx.send("Please wait until audio is finished. Use the stopVC command to stop the audio")
        return
    ''' I am going to remove this for now to work on queue system
    for file in os.listdir(path+folderYT):
        if file.endswith(".mp3") or file.endswith(".m4a"):
            os.remove(path+folderYT+file)
    '''
    if voice:
        channel = voice.channel
        newAudio = await downloadVideo(ctx, url)
        voice = await setVoiceClient(ctx, ctx.author)
        source = FFmpegPCMAudio(path + folderYT + folderSlash + newAudio)
        player = voice.play(source)
        await ctx.send("Playing your audio")
    else:
        await ctx.send("I need to be in a voice channel to do this!")
    '''
    voice = await setVoiceClient(ctx)
    if voice:
        path = "E:\\SanDiskSecureAccess\\Programming\\Discord bot\\"
        folder = "youtube\\"
        channel = ctx.message.author.voice.channel
        for file in os.listdir(path+folder):
            if file.endswith(".mp3"):
                os.remove(path+folder+file)
        ydl_opts = {

            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
        }],
            }
        lastAudio = await getAudioFiles()
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        newAudio = await getAudioFiles()
        for file in lastAudio:
            newAudio.remove(file)
        print(newAudio)
        shutil.copyfile(path+newAudio[0],path+folder+newAudio[0])
        os.remove(newAudio[0])
        source = FFmpegPCMAudio(path+folder+newAudio[0])
        player = voice.play(source)
    else:
        await ctx.send("I need to be in a voice channel to do this!")
    '''


async def downloadVideo(ctx, url):
    await verifyFiles()
    ydl_opts = {

        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }], 'noplaylist': True
    }
    lastAudio = await getAudioFiles()
    print("last:")
    print(lastAudio)
    await ctx.send("Preparing the audio")
    with yt_dlp.YoutubeDL(ydl_opts) as y:
        y.download([url])
    newAudio = await getAudioFiles()
    for file in lastAudio:
        newAudio.remove(file)
    print("New:")
    print(newAudio)
    for file in newAudio:
        shutil.copyfile(path + file, path + folderYT + folderSlash + file)
        os.remove(file)
    return newAudio[0]

'''
async def downloadVideoOld(ctx, url):
    ydl_opts = {

        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredquality': '192'
        }], 'noplaylist': True
    }
    lastAudio = await getAudioFiles()
    print("last:")
    print(lastAudio)
    await ctx.send("Preparing the audio")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    newAudio = await getAudioFiles()
    for file in lastAudio:
        newAudio.remove(file)
    print("New:")
    print(newAudio)
    return newAudio[0]
'''

async def verifyFiles():
    blackListTypes = [".mp3", ".m4a",".webm"]
    directory = os.listdir(path)
    audioRemoved = []
    for file in directory:
        for ending in blackListTypes:
            if file.endswith(ending):
                audioRemoved.append(file)
                os.remove(file)
    print("Removed "+str(len(audioRemoved))+": "+str(audioRemoved))


@client.command()
async def saveLastAudio(ctx):
    for file in await getAudioFiles(folderYT):
        shutil.copyfile(path + folderYT + folderSlash + file, path + folderAudio + folderSlash + file)
    await ctx.send("Copied")


@client.command()
async def becomeGamer(ctx, role: discord.Role):
    # role = get(ctx.guild.roles, name=roleName)
    # check if user is becoming a valid role
    if not role.name in getGamerRoles(ctx):
        await ctx.send("That is not a gamer role!")
        # heres a something i thought would be funny
        if role.is_bot_managed():
            await ctx.send("Wait, why would you want to become a bot? Do you want to be like me...?")
    elif role in ctx.author.roles:
        await ctx.send("You are already a " + role.name + " gamer")
    else:
        await ctx.author.add_roles(role)
        await ctx.send(f"{role.name} gamers, you have a new member!")


@client.command()
async def removeGamer(ctx, role: discord.Role):
    if not role.name in getGamerRoles(ctx):
        await ctx.send("Tht is not a gamer role")
    elif role in ctx.author.roles:
        await ctx.author.remove_roles(role)
        await ctx.send("You are no longer a " + role.name + " gamer. Sad to see you go :(")
    else:
        await ctx.send("You aren't a " + role.name + " gamer anyways. Do you really hate them that much?")


@client.command(aliases=["showRoles"])
async def showGamerRoles(ctx):
    gamerRoles = getGamerRoles(ctx)
    if not gamerRoles:
        await ctx.send("There are no gamer roles on this server! Why don't you make some with the command?")
    else:
        message = ""
        for r in gamerRoles:
            message += r
            if r != gamerRoles[len(gamerRoles) - 1]:
                message += ", "
        await ctx.send("Here are all the gamer roles:\n" + message)


@client.command()
async def addGamerRole(ctx, roleName, c=discord.Colour.random()):
    print(ctx.author.name + " is adding a " + roleName + " role.")
    print(c)
    # maybe have an anti-spam check where every person can only create a role every 180 seconds. Probably do this using coroutines if python has them
    # check if role exists
    if roleName in getGamerRoles(ctx):
        await ctx.send("There is already a role for that game!")
    else:
        newRole = await ctx.guild.create_role(name=roleName, mentionable=True, colour=c)
        await ctx.send(f"A new gamer role called {newRole.mention} was created by {ctx.author.mention}")
        # In order for the bot to know which role is a gamer role in a server, theres a couple of things i can do:
        # I can write to a file here so that way any new roles will be saved there <--
        # I could also give a list of non gamer roles in the server and have the bot assume any other role is a gamer role (blacklist)
        roleFile = open(constructGamerRolePath(ctx), "a")
        roleFile.write(roleName + "\n")
        roleFile.close()


@client.command()
async def removeGamerRole(ctx, role: discord.Role):
    # Only i can use this command
    if ctx.author.name == developer:
        # removing the role in discord
        if role.name in getGamerRoles(ctx):
            print("Deleting gamer role " + role.name)
            await role.delete()
        else:
            await ctx.send("That is not a gamer role!")
            return
        # removing the role from file
        roleFile = open(constructGamerRolePath(ctx), "r")
        content = roleFile.read()
        content = content.replace(role.name + "\n", "")
        roleFile.close()
        roleFile = open(constructGamerRolePath(ctx), "w")
        roleFile.write(content)
        roleFile.close()
        await ctx.send("Deleted role " + role.name + " successfully")
    else:
        await ctx.send("Only my master can use this command")


def getGamerRoles(ctx):
    # check to see if file exists
    p = constructGamerRolePath(ctx)
    print(p)
    if not os.path.exists(p):
        f = open(p, "x")
        f.close()
    file = open(p, "r")
    content = file.read().splitlines()
    file.close()
    print(content)
    return content


def constructGamerRolePath(ctx):
    setFolder(path + folderServers + folderSlash + ctx.guild.name)
    return path + folderServers + folderSlash + ctx.guild.name + folderSlash + "GamerRoles.txt"


def contructServerPath(ctx):
    setFolder(path + folderServers + folderSlash + ctx.guild.name + folderSlash)
    return path + folderServers + folderSlash + ctx.guild.name + folderSlash


def addItemFile(ctx, f, item):
    setFolder(contructServerPath(ctx))
    if not os.path.exists(path + folderServers + folderSlash + ctx.guild.name + folderSlash + f):
        file = open(path + folderServers + folderSlash + ctx.guild.name + folderSlash + f, "x").close()
    file = open(contructServerPath(ctx) + folderSlash + f, "a")
    file.write(item + "\n")
    file.close()
    print("Added " + item + " to " + ctx.guild.name + "'s " + f + " file")


def removeItemFile(ctx, f, item):
    setFolder(contructServerPath(ctx))
    # Maybe check if file exists first to avoid an error
    if not os.path.exists(path + folderServers + folderSlash + ctx.guild.name + folderSlash + f):
        file = open(path + folderServers + folderSlash + ctx.guild.name + folderSlash + f, "x").close()
    file = open(contructServerPath(ctx) + folderSlash + f, "r")
    content = file.read()
    content = content.replace(item + "\n", "")
    file.close()
    file = open(contructServerPath(ctx) + folderSlash + f, "w")
    file.write(content)
    file.close()
    print("Removed " + item + " from " + ctx.guild.name + "'s " + f + " file")


def getItemsFile(ctx, f):
    setFolder(path + folderServers + folderSlash + ctx.guild.name)
    # Maybe check if file exists first to avoid an error
    if not os.path.exists(path + folderServers + folderSlash + ctx.guild.name + folderSlash + f):
        file = open(path + folderServers + folderSlash + ctx.guild.name + folderSlash + f, "x").close()
    file = open(path + folderServers + folderSlash + ctx.guild.name + folderSlash + f, "r")
    content = file.read().splitlines()
    file.close()
    return content


@client.command(aliases=["changeGamerRoleColor", "changeRoleColour", "changeRoleColor"])
async def changeGamerRoleColour(ctx, role: discord.Role, c):
    if role.name in getGamerRoles(ctx):
        print(role.colour)
        await role.edit(colour=c)
        await ctx.send("Changed info for " + role.name + " gamers")
    else:
        await ctx.send("That is not a gamer role! You trying to hack me?")


@client.command(aliases=["randDm", "randDM", "randomDM"])
async def randomDm(ctx, message, seePerson=True, onlineOnly=True):
    selection = []
    for member in ctx.guild.members:
        if not member.bot:
            selection.append(member)
    if onlineOnly:
        '''
        tempList = selection
        totalCount = 0
        for member in tempList:
            totalCount += 1
            print("Number "+str(totalCount))
            print(member.name)
        print("There are "+str(totalCount)+" members in total")
        print(tempList)
        print("\nChecking for status\n")
        removedCount = 0
        i = 1
        #BUG HERE: it wont check all elements in the list. It completely skips everything tp do with them, not even writing their name
        #My ONLY guess as to why this doesnt work is cuz the member data type was too complex at times and python had to skip certain items in the list
        for member in tempList:
            print("Number "+str(i))
            i += 1
            print(member.name)
            print(member.status)
            if not member.status == discord.Status.online:
                print("Removing "+member.name)
                selection.remove(member)
                removedCount += 1
            print("\n")
        print("Removed "+str(removedCount)+" people from list.\nHere is the final list:")
        for member in selection:
            print(member.name)
        print("There are "+str(totalCount-removedCount)+" people left") 
        '''
        # to fix bug above, maybe theres something too complex with a member data type? So ill try to have a list of their id's (strings) instead
        tempList = []
        totalCount = 0
        for member in selection:
            totalCount += 1
            print("Number " + str(totalCount))
            print(member.name)
            tempList.append(member.id)
        print("There are " + str(totalCount) + " members in total")
        print(tempList)
        print("\nChecking for status\n")
        removedCount = 0
        i = 1
        for memID in tempList:
            print("Number " + str(i))
            i += 1
            # get member using their id
            member = ctx.guild.get_member(memID)
            print(member.name)
            print(member.status)
            if not member.status == discord.Status.online:
                print("Removing " + member.name)
                selection.remove(member)
                removedCount += 1
            print("\n")
        print("Removed " + str(removedCount) + " people from list.\nHere is the final list:")
        for member in selection:
            print(member.name)
        print("There are " + str(totalCount - removedCount) + " people left")

    # for error checking, check if the list is empty
    if not selection:
        await ctx.send("There is nobody i can send a message to?!!!!!")
    else:
        luckyPerson = random.choice(selection)
        print(f"{luckyPerson.name} was chosen!")
        await luckyPerson.send(message)
        if seePerson:
            await ctx.send(f"{luckyPerson.name} was the lucky winner!")


@client.command(aliases=["silentDM"])
async def silentDm(ctx, name, message):
    # In order for no ping to happen when u mention a member, this command need the user to spell the username or nickname to send
    # Convert everything to lower case that way its not case sensitve
    await ctx.message.delete()
    name = name.lower()
    for member in ctx.guild.members:
        # nickname will return nontype if there is none, so i cant treat this the same as member.name
        # fun fact: the "is" keyword checks if two things are the same object. Returns False if they are not the same object, even if the two objects are 100% equal.
        if not type(member.nick) is str:
            nickname = False
        else:
            nickname = member.nick
        if member.name.lower() == name or nickname == name:
            print("Person found!")
            print(member.name)
            await member.send(message + " -From a secret admirer")
            break
    else:
        await ctx.author.send("I couldn't find the person you were trying to dm. Perhaps you have a typo?")


@client.command()
async def ban(ctx, member: discord.Member):
    if ctx.author.name != developer:
        await ctx.send("Nope.")
        return
    await ctx.send("You're gonna get BANNED kid")
    banRoleName = "BANNED"
    validServer = False
    roles = ctx.guild.roles
    for r in roles:
        print(r)
        if r.name == banRoleName:
            validServer = True
            banRole = r
            break
    if not validServer:
        await ctx.send("Set up a " + banRoleName + " in your server to make this command work")
    else:
        print("\n" + str(banRole))
        for r in member.roles:
            print(r)
            if r.name == "@everyone":
                continue
            await member.remove_roles(r)
        await member.add_roles(banRole)
        await ctx.send(f"Hey everyone, {member.mention} is banned!")


@client.command()
async def resetGame(ctx):
    if ctx.guild.member_count == 1:
        await ctx.send("You can't play this alone... get some friends")
    else:
        gameFile = open(contructServerPath(ctx) + "killGame.txt", "w")
        gameFile.write("")
        gameFile.close()
        for member in ctx.guild.members:
            addItemFile(ctx, "killGame.txt", member.name)
        await ctx.send("Reseting game")


@client.command()
async def gameKill(ctx):
    memberList = getItemsFile(ctx, "killGame.txt")
    chosenOne = random.choice(memberList)
    memberList.remove(chosenOne)
    message = ""
    for name in memberList:
        print(name)
        message += name
        if not name == memberList[len(memberList) - 1]:
            message += ", "
    print("Chosen: " + chosenOne)
    # Remove person after from file
    removeItemFile(ctx, "killGame.txt", chosenOne)
    # check to see if only one survivor remains
    if len(memberList) == 1:
        await ctx.send("-->" + chosenOne + " was killed off!\nOnly one person remains...\n")
        await sendEmbed(ctx, "\n" + memberList[0] + " is the winner!")
        await resetGame(ctx)
    else:
        await ctx.send("-->" + chosenOne + " was killed off!\nThere are " + str(
            len(memberList)) + " people remaining\n" + message + "\n")


@client.command()
async def gameSimulate(ctx):
    # This command merely simulates a game instead of making manual gameKill commands
    await resetGame(ctx)
    i = 0
    memberCount = ctx.guild.member_count
    while i < memberCount - 1:
        i += 1
        await gameKill(ctx)


@client.command(aliases=["sendReact"])
async def sendReactableMessage(ctx, text, optString):
    # hoping that people use emojis lmao
    options = optString.strip().split()
    # collect message id so we can check in events if it was reacted
    print(options)
    message = await ctx.send(text)
    for emoji in options:
        await message.add_reaction(emoji)


@client.command()
async def seeQueue(ctx):
    serverId = ctx.message.guild.id
    if serverId in queue:
        localQueue = queue[serverId]
        for song in localQueue:
            await ctx.send(song)
    else:
        await ctx.send("nothing in queue")


'''
async def FFmpegCheck(ctx):
    #See if FFmpeg is installed. An easy way to do this is to try using the command
    try:
        test = await getAudioFiles()
        print(test)
        test = test[0]
        print(test)
        FFmpegPCAudio(test)
        return True
    except:
        await ctx.send("FFmpeg is not installed or not set up properly")
        return False
'''


async def AddToQueue(ctx, audioFile):
    serverId = ctx.message.guild.id
    source = FFmpegPCMAudio(audioFile)
    if serverId in queue:
        # Looks at the serverid key and adds another source to the value's list
        queue[serverId].append(source)
    else:
        # This means create a new key (serverId) and add the value of a list with a single value of source
        queue[serverId] = [source]
    await CheckQueue(ctx)
    print(queue)
    await ctx.send("Added to queue")
    await seeQueue(ctx)


async def CheckQueue(ctx):
    serverId = ctx.message.guild.id
    voice = ctx.guild.voice_client
    print(queue)
    # checks too if the list is empty in the serverid key
    if queue[serverId] != []:
        # Get the first song in queue: first come, first serve
        source = queue[serverId].pop(0)
        await PlayAudio(ctx, source)
    else:
        print("No more items in queue")


async def PlayAudio(ctx, source):
    voice = ctx.guild.voice_client
    voice.play(source, after=lambda x=None: CheckQueue(ctx))
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


async def hasRequiredFiles(filesNeeded):
    f = filesNeeded
    print(f)
    for file in await getAudioFiles(folderAudio):
        for element in filesNeeded:
            if element == file:
                f.remove(element)
                print(f)
                if not f:
                    return True, f
    else:
        return False, f


async def displayMissingFiles(ctx, filesNeeded):
    stringFiles = ""
    for file in filesNeeded:
        stringFiles += file
        if file != filesNeeded[-1]:
            stringFiles += ", "
    await ctx.send(f"You need the following files: {stringFiles}")


async def getAudioFiles(p=""):
    fileTypes = [".mp3", ".m4a"]
    print(p)
    setFolder(path + p)
    directory = os.listdir(path + p)
    audio = []
    for file in directory:
        for ending in fileTypes:
            if file.endswith(ending):
                audio.append(file)
    print(audio)
    return audio


async def setVoiceClient(ctx, member: discord.Member):
    # This will return the current voice client (basically where its in vc). If there is no voice client, join the member
    if ctx.voice_client:
        return ctx.voice_client
    # if the sender is in a vc, go there
    if member.voice:
        return await member.voice.channel.connect()
    # if the sender isn't in a vc, then send the bot to a place where there is someone
    channelsWithPeople = []
    for c in ctx.guild.voice_channels:
        if len(c.members) > 0:
            channelsWithPeople.append(c)
    if len(channelsWithPeople) > 0:
        return await random.choice(channelsWithPeople).connect()
    # if there is absolutely nobody, just join a random vc
    return await random.choice(ctx.guild.voice_channels).connect()


async def hasRole(memberRoles, roleName):
    for role in memberRoles:
        if role.name == roleName:
            return True
    else:
        return False


def setFolder(f):
    if not os.path.exists(f):
        os.makedirs(f)
        print("Made the folder " + f)


async def clearYoutube():
    for audio in await getAudioFiles(folderYT):
        os.remove(path + folderYT + folderSlash + audio)


async def checkDupeAudio(audioName):
    # check if this audio is already downloaded to skip downloading process
    print()


# RPG GAME INTEGRATION-------

'''
@client.event
async def on_raw_reaction_add(payload):
    pass
#this is when any command runs into an error. You can specify error methods specific to a command by using the decorator @commandNmame.error
#This makes all errors do this. If something doesn't work without giving you any idea why, check here just in case
#I think implementing this method stops all error text from poping up in window. We dont want that

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command doesn't exist")
@client.command()
async def hello(m):
    user = m.author
    print(user.name)
    if user.name == "FrozenLava04":
        await m.channel.send("Hello Bastille Geates")
    elif user.name == "Scarlet_blue71":
        await m.channel.send("Hello Austin Olmsted")
    elif user.name == "PineCone":
        await m.channel.send("Hello Alexii Saliken (I think i butchered yur last name I\'m srry)")
'''
# Random notes:
# guild means the server
# ctx can actually be anything, its a variable (as shown in the hello command)
# ctx is the context of the command, storing stuff like the channel it was called in, the user who called it among other things

#Gets the token from a text file. Needed to run the bot
def getToken():
    if os.path.exists("token.txt"):
        return open("token.txt", "r").readline()
    else:
        print("No token found, please provide a token.txt with a valid Discord bot token")
        sys.exit()
# for security purposes, the token is hidden. Use your own bot token to test
client.run(getToken())
