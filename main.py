import asyncio
from datetime import timedelta
import discord
from discord.ext import commands
import os

local_current_directory = os.path.dirname(__file__)
local_file_path = os.path.join(local_current_directory, "deletedMessages.txt")
deletedMessagesFile = local_file_path
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

bot = commands.Bot(command_prefix="ol!", intents=intents)

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

    if message.content.lower() == "!startofflinebot" and not active:
        active = True
        await message.channel.send("Started offline bot")
    elif message.content.lower() == "!stopofflinebot" and active:
        active = False
        await message.channel.send("Stopped offline bot")

    if isinstance(message.channel, discord.TextChannel) and active:
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
                    for list_member in last_member:
                        if list_member == member.id:
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


current_directory = os.path.dirname(__file__)
file_path = os.path.join(current_directory, "token.txt")
token = open(file_path)
bot.run(token.read())
