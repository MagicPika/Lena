import discord
from discord.ext import commands
from modules.applications import Applications
import config

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Подключаем обработчик заявок
bot.add_cog(applications.Applications(bot))

@bot.event
async def on_ready():
    print(f"Бот готов → {bot.user}")
    await bot.tree.sync()
    print("Слэш-команды синхронизированы")


bot.run(config.TOKEN)

