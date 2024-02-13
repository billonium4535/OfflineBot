import asyncio
from datetime import timedelta
import discord
from discord.ext import commands
import os

deletedMessagesFile = "./deletedMessages.txt"
active = True

try:
    with open(deletedMessagesFile, "r"):
        pass
except FileNotFoundError:
    with open(deletedMessagesFile, "w"):
        pass

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

last_member = []


async def remove_member_id(member_id):
    await asyncio.sleep(60)
    try:
        last_member.remove(member_id)
    except:
        pass


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your status"))
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    global active
    if message.author.bot:
        return

    if message.content.lower() == "!StartOfflineBot":
        active = True
    elif message.content.lower() == "!StopOfflineBot":
        active = False

    if message.content == "timeout":
        print(message.author)
        if message.author.id == 296371822381891586:
            member = message.guild.get_member(364476443578728459)
            await member.timeout(timedelta(days=28), reason="fuck you")

    if isinstance(message.channel, discord.TextChannel):
        member = message.guild.get_member(message.author.id)
        if member and member.status == discord.Status.offline:
            with open(deletedMessagesFile, "a") as f:
                f.write(f"Message: {message.content}, Author: {message.author}, Channel: {message.channel}\n")
            f.close()
            # Commented out to not delete messages from users
            # try:
            #     await message.delete()
            # except discord.errors.NotFound:
            #     pass
            last_member.append(member.id)
            bot.loop.create_task(remove_member_id(member.id))
            if last_member.count(member.id) >= 5:
                try:
                    last_member.remove(member.id)
                    await member.timeout(timedelta(seconds=30), reason="you were warned")
                    await message.channel.send(f"{member.mention} I FUCKIN WARNED YOU")
                    with open(deletedMessagesFile, "a") as f:
                        f.write(f"Log: Timed out {message.author}\n")
                    f.close()
                except:
                    pass
            elif last_member.count(member.id) == 3:
                await message.channel.send(f"{member.mention} keep being a bitch, see what happens")
            elif last_member.count(member.id) == 4:
                await message.channel.send(f"{member.mention} istg fuck off")
            else:
                # await message.channel.send(f"{member.mention}, you cannot send messages while offline.")
                await message.channel.send(f"{member.mention} has sent a message while offline.")

    await bot.process_commands(message)


token = open("./token.txt")
bot.run(token.read())
