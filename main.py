import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.TextChannel):
        member = message.guild.get_member(message.author.id)
        if member and member.status == discord.Status.offline:
            await message.delete()
            await message.channel.send(f"{member.mention}, you cannot send messages while offline.")

    await bot.process_commands(message)


token = open("./token.txt")

bot.run(token.read())
