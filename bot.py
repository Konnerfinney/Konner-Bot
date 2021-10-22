import discord
from discord.ext import commands, tasks
import secrets
import dj
import customs
import sys
import os
import datetime
import asyncio
import multiprocessing
from multiprocessing import Process
from keep_alive import keep_alive
import os


#Justin commented lines 249-252

# init seq for client
client = commands.Bot(command_prefix='.')
playerChannel = client.get_channel(577300822770188298)
playerChannelID = 577300822770188298
rs_channel_id = 741837451672420352
rs_channel = client.get_channel(rs_channel_id)

#global vars for classes
customInstance = customs.customGame()
customsChannel = client.get_channel(577300822770188298)
adminID = [159819435404820481, 277964604771008515]
customsChanID = 577300822770188298


emojiY = '✅'
emojiN = '🚫'

amount_players_queued = 0

# command to show bot is active
@client.event
async def on_ready():
    print('Bot is ready.')



#Will List the Customs commands
@client.command()
async def customCmds(ctx):
    await ctx.message.channel.send(customs.customCmds)

#Customs queue listing
@client.command()
async def newCustoms(ctx):
    print("\nstarting new custom")
    if (ctx.message.channel.id == customsChanID) and (ctx.message.author.id in adminID):
        customInstance.newCustom()
        sent_msg = await ctx.message.channel.send("**Starting New Custom Game**")
        print("custom game started")
        await asyncio.sleep(5)
        await del_msg(ctx.message)
        await del_msg(sent_msg)
        await listQueue(ctx)

#Customs Add to queue
@client.command()
async def queue(ctx):
    print("\nadding new player")
    # if the message is in an approved channel
    if ctx.message.channel.id == customsChanID:
        # create player object
        x = player(ctx.message.author.id)
        # send over the player objet
        alreadyAdded = customInstance.add(x)
        mention_string = x.get_mention_string()

        print("adding: " + mention_string + " to queue")

        # takes feedback from add method and prints out that person is added or already in queue
        if alreadyAdded == True:
            sent_msg = await ctx.message.channel.send(mention_string +" is already in the queueList")
        else:
            sent_msg = await ctx.message.channel.send(mention_string + " added to the queue")
        await asyncio.sleep(5)
        await del_msg(sent_msg)
        await del_msg(ctx.message)
        await listQueue(ctx)


#Customs delete from queue
@client.command()
async def delSelf(ctx):
    print("\ndeleting player")
    if ctx.message.channel.id == customsChanID:

        wasInQueue = customInstance.remove(ctx.message.author.id)
        print("deleting: " + ctx.message.author.mention + " from queue")
        if wasInQueue:
            sent_msg = await ctx.message.channel.send("Removing " + ctx.message.author.mention + " from queue")
        else:
            sent_msg = await ctx.message.channel.send(ctx.message.author.mention + " was not in queue")
        print("deleted player")
        await asyncio.sleep(5)
        await del_msg(sent_msg)
        await del_msg(ctx.message)
        await listQueue(ctx)

#Customs list queue
async def listQueue(ctx):
    customs_list_message = await ctx.fetch_message(846969296583393300)
    print("\nlisting customs queue")
    if ctx.message.channel.id == customsChanID:
      queueList = customInstance.list()
      counter = 1
      ret_str = "**Customs Queue:**\n"
      for i in queueList:
          user = i.get_mention_string()
          ret_str += str(counter) + ": " + str(user) + "\n"
          counter += 1
      await customs_list_message.edit(content = ret_str)
      print("queue listed")
      await ctx.channel.edit(topic = ret_str)



#Customs add other to queue
@client.command()
async def queue_other(ctx):
    print("\nadding other to queue")
    if ctx.message.channel.id == customsChanID:
        other = player(ctx.message.mentions[0].id)
        other_mention = other.get_mention_string()
        print("adding: " + other_mention + " to queue")

        alreadyAdded = customInstance.add(other)
        if alreadyAdded == True:
            sent_msg = await ctx.message.channel.send(other_mention + " is already in the queueList")
        else:
            sent_msg = await ctx.message.channel.send(other_mention + " added to the queue")
        await asyncio.sleep(5)
        await del_msg(sent_msg)
        await del_msg(ctx.message)
        await listQueue(ctx)




#Customs del other to queue
@client.command()
async def delOther(ctx, args):
    print("\ndeleting other from queue")
    if (ctx.message.channel.id == customsChanID) and (ctx.message.author.id in adminID):
        other = player(ctx.message.mentions[0].id)
        other_mention = other.get_mention_string()
        #print("deleting: " + other + " from queue")
        wasInQueue = customInstance.remove(other.get_id())
        if wasInQueue:
            sent_msg = await ctx.message.channel.send("Removing " + other_mention + " from queue")
            print("was in queue")
        else:
            sent_msg = await ctx.message.channel.send(other_mention + " was not in queue")
        print("other deleted from queue")
        await asyncio.sleep(5)
        await del_msg(sent_msg)
        await del_msg(ctx.message)
        await listQueue(ctx)


#meme command
@client.command()
async def micro(ctx):
    print("\ntest")
    sentChannel = ctx.message.channel
    await sentChannel.send('')

playerList = []
@client.command()
async def getPlayer(ctx):
    print("running test")

    # this calls the list to get next player
    # returns False (bool) if no players in list
    x = customInstance.getNext()
    print(x.get_user_name())
    # if x == player object then call them
    if x != False:
      playerList.append(x)
      await x.get_user(ctx)
    else:
      await ctx.channel.send("No players in queue")

@client.event
async def on_raw_reaction_add(reaction):
  reaction_message_id = reaction.message_id
  # get the message object that was reacted to
  reaction_channel = await client.fetch_channel(reaction.channel_id)
  reaction_message = await reaction_channel.fetch_message(reaction_message_id)
  if reaction_message.author.bot:
    # base var to hold player
    current_player_requested = 1

    #get the user_id of the reactor
    reactor_id = reaction.user_id

    # get the user mentioned by the message
    if len(reaction_message.mentions) > 0:
      mentioned_user_id = reaction_message.mentions[0].id

    # check if the message is a get_player message
    for i in playerList:
      if i.get_mention_id() == reaction_message_id:
        current_player_requested = i

    if (current_player_requested != 1):
      # checks if correct person reacted
      if (reactor_id == mentioned_user_id):
        reaction_emoji = str(reaction.emoji)
        if (reaction_emoji == emojiY):
          # user accepted w/ emoji
          print("user accepted")
          await current_player_requested.user_accepted(reaction_channel)
        elif (reaction_emoji == emojiN):
          # user declined w/ emoji
          print("no")
          await current_player_requested.user_declined(reaction_channel, False)
  
    # compare id's to verify correct person reacted
    # submit that to the player class

async def del_msg(msg):
  await msg.delete()

#dad joke finder
@client.event
async def on_message(message):
    if message.author != client.user and message.content != "" and message.channel != rs_channel:
        print("\nsender: " + str(message.author) + " sent: " +
              str(message.content))
        joke = " "
        joke = dj.isDadJoke(str(message.content))
        if joke != "null":
             await message.channel.send(joke)
    await client.process_commands(message)

class player(discord.User):
    def __init__(self, id):
        self.id = id
        self.message_list = []

    # returns string for mentioning user that player object is imitating
    def get_mention_string(self):
        z = self.mention
        return z

    async def get_user_name(self):
      x = await client.fetch_user(self.id)
      return x.name

    def get_id(self):
        return self.id

    async def get_user(self, ctx):
        # start process of getting user
        print("getting user")
        self.ctx = ctx
        # get the channel message was sent from
        channel = ctx.message.channel

        # gets user mention message
        user_mention_string = self.create_user_mention_string(self.get_mention_string())

        # send message to correct channel
        self.user_mention_message = await self.send_mention_user_message(channel, user_mention_string)

        # add reactions to message
        await self.add_user_reactions(self.user_mention_message)

        # start a timer 
        self.timer = 180

        convertedTime = str(datetime.timedelta(seconds=self.timer))

        # send timer message
        message_timer = await channel.send(convertedTime)

        self.message_list.append(message_timer)

        # call clock 
        while (self.timer > 0):
          #decrement timer
          self.timer = self.timer - 1
          convertedTime = str(datetime.timedelta(seconds=self.timer))
          await message_timer.edit(content=convertedTime)
          print("{} time left".format(self.timer))
          #check reactions
          await asyncio.sleep(1)
        # if the timer runs out, go to next
        if self.timer == 0:
          await self.user_declined(channel, True)

    async def user_declined(self, channel, outOfTime):
        # user declined or ran out of Time
        print("user declined or ran out of time")

        # prints either user ran out of time (timer hit 0)
        # or they declined the call via emoji
        if (outOfTime == True):
          declined_message_string = "{} ran out of time".format(self.get_mention_string())
        else:
          declined_message_string = "{} declined the invite".format(self.get_mention_string())

        # send message to tell them person ran out of time
        declined_message = await channel.send(declined_message_string)

        # stop timer
        self.timer = -1

        # delete messages
        for i in self.message_list:
          await i.delete()
        # and call the get next player function
        await getPlayer(self.ctx)

    async def user_accepted(self, channel):
        # user accepted
        print("user accepted within time")

        # send message that the person was accepted
        acceptance_message = await channel.send("{} is in!".format(self.get_mention_string()))

        # stop the timer
        self.timer = -1

        # delete messages
        for i in self.message_list:
          await i.delete()




    def create_user_mention_string(self,user_mention_string):
      # creates and returns string to mention user
      return "{0} You are in! Please respond in 3 minutes.".format(user_mention_string)

    async def send_mention_user_message(self, channel, user_message):
      # sends mention message to user in correct channel
      # returns message for deletion purposes
      user_message = await channel.send(user_message)
      self.message_list.append(user_message)
      return user_message
    async def add_user_reactions(self, user_message):
      print("adding reactions to user msg")
      await user_message.add_reaction(emojiY)
      await user_message.add_reaction(emojiN)
    
    def get_mention_id(self):
      return self.user_mention_message.id

keep_alive()
TOKEN = os.environ['DISCORD_BOT_SECRET']
client.run(TOKEN)
