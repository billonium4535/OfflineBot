import discord
from discord.ext import commands

deletedMessagesFile = "./deletedMessages.txt"

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


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your status"))
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.TextChannel):
        member = message.guild.get_member(message.author.id)
        if member and member.status == discord.Status.offline:
            with open(deletedMessagesFile, "a") as f:
                f.write(f"Message: {message.content}, Author: {message.author}, Channel: {message.channel}\n")
            # Commented out to not delete messages from users
            # try:
            #     await message.delete()
            # except discord.errors.NotFound:
            #     pass
            # await message.channel.send(f"{member.mention}, you cannot send messages while offline.")
            await message.channel.send(f"{member.mention} has sent a message while offline.")

    await bot.process_commands(message)


token = open("./token.txt")
bot.run(token.read())
