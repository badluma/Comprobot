import discord
import os
import dotenv

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
