import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")
FORUM_CHANNEL_ID = 1458881043653197896  # вставь ID форум-канала

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Бот запущен: {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    # Игнорируем сообщения бота
    if message.author.bot and message.webhook_id is None:
        return

    # Если это не webhook — просто даём работать командам
    if message.webhook_id is None:
        await bot.process_commands(message)
        return

    # Проверяем что это нужный форум-канал
    if message.channel.id != FORUM_CHANNEL_ID:
        return

    if not message.embeds:
        return

    embed = message.embeds[0]
    if embed.title != "Новая заявка":
        return

    # Ищем Discord ID
    discord_id = None
    for field in embed.fields:
        if field.name == "Discord ID":
            discord_id = ''.join(c for c in field.value if c.isdigit())

    if not discord_id:
        await message.channel.send("❌ Неверный Discord ID")
        return

    try:
        user = await bot.fetch_user(int(discord_id))
    except:
        await message.channel.send("❌ Пользователь не найден")
        return

    forum = message.channel

    # Берём тег "На уточнении"
    tag = discord.utils.get(forum.available_tags, name="На уточнении")

    thread = await forum.create_thread(
        name=f"Заявка {user.name}",
        content="Новая заявка получена.",
        applied_tags=[tag] if tag else []
    )

    await message.delete()

    await thread.send(f"Заявка от {user.mention} создана.")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(TOKEN)
