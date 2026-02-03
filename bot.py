import os
import random
import discord
from discord.ext import commands
from datetime import datetime

# Наши модули
from pigs import pig_system
from stats import stats_db

# ===== ВАЖНО: ДЛЯ RAILWAY =====
# Получаем токен из переменных окружения Railway
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print("❌ DISCORD_TOKEN не найден в переменных окружения")
    exit()

print("=" * 50)
print("🤖 Запуск Аллах-бота для Discord...")
print(f"✅ Токен получен из окружения")

# Префикс команд
PREFIX = "аллах "

# Список гифок
GIFS = [
    "https://tenor.com/view/family-guy-fortnite-family-guy-chicken-popular-vibe-the-weeknd-gif-3449867671768307845",
    "https://tenor.com/view/edit-lettre-z-gif-27248169",
    "https://tenor.com/view/no-i%27m-not-a-human-pale-intruder-cute-happy-clapping-hands-gif-2155492940741471848",
    "https://tenor.com/view/zov-z-o-v-sin-sluhi-gif-1796216572950618958",
    "https://tenor.com/view/thukuna-sukuna-meme-jjk-gif-17866965436393542654",
    "https://tenor.com/view/lol-sus-troll-troll-face-face-gif-22065080",
    "https://tenor.com/view/silvers-rayleigh-one-piece-op-1088-gif-160280274124649959",
    "https://tenor.com/view/%D0%B2%D0%B0%D0%BD%D1%8F-%D1%85%D1%83%D0%B9%D0%BB%D0%B0%D0%BD-%D0%BB%D0%BE%D1%85-%D0%B4%D0%B0%D1%83%D0%BD-%D0%B2%D0%B0%D0%BD%D0%B5%D0%BA-gif-7575275907767741127",
    "https://tenor.com/view/boykisser-gif-5163203352201378626",
    "https://tenor.com/view/77-gif-17927864047465403784",
    "https://tenor.com/view/pig-pig-funny-pig-chewing-animal-animal-funny-gif-15291725007664352238",
    "https://tenor.com/view/pig-spin-circling-fat-pig-baby-pig-gif-17867804420670986053",
    "https://tenor.com/view/mujikcboro-seriymujik-gif-24361533"
]

# Настройки бота
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)

# ===================== СОБЫТИЯ =====================

@bot.event
async def on_ready():
    print(f"✅ Бот {bot.user} запущен и готов к работе!")
    print(f"🎮 Префикс команд: '{PREFIX}'")
    print(f"👥 Подключен к {len(bot.guilds)} серверам")
    print("=" * 50)
    
    # Устанавливаем статус
    await bot.change_presence(
        activity=discord.Game(name=f"{PREFIX}помощь")
    )

@bot.event
async def on_message(message):
    """Обработка всех сообщений"""
    # Игнорируем сообщения ботов
    if message.author.bot:
        return
    
    # Добавляем сообщение в статистику
    stats_db.add_message(
        user_id=str(message.author.id),
        user_name=message.author.name
    )
    
    # Пропускаем для обработки команд
    await bot.process_commands(message)

# ===================== КОМАНДЫ =====================

@bot.command(name="кто")
async def кто(ctx, *, вопрос=""):
    """Выбирает случайного участника"""
    # Получаем всех участников (не ботов)
    members = [m for m in ctx.guild.members if not m.bot]
    
    if not members:
        await ctx.send("👻 В чате нет людей!")
        return
    
    chosen = random.choice(members)
    
    if вопрос:
        responses = [
            f"🎲 Я думаю, {chosen.mention} {вопрос}!",
            f"✨ Мне кажется, {chosen.mention} {вопрос}.",
            f"👑 Определённо {chosen.mention} {вопрос}!",
            f"⭐ Без сомнений - {chosen.mention} {вопрос}.",
        ]
    else:
        responses = [
            f"🎲 Я выбираю {chosen.mention}!",
            f"✨ Мой выбор: {chosen.mention}!",
            f"👑 Внимание на {chosen.mention}!",
        ]
    
    await ctx.send(random.choice(responses))

@bot.command(name="укого")
async def укого(ctx, *, качество=""):
    """Найти у кого есть качество"""
    if not качество:
        await ctx.send("❌ Укажи качество: `аллах укого самый умный`")
        return
    
    members = [m for m in ctx.guild.members if not m.bot]
    
    if not members:
        await ctx.send("🤖 В чате только боты!")
        return
    
    chosen = random.choice(members)
    
    response = f"**У {chosen.name} {качество}**"
    emojis = ["👔", "✨", "⭐", "🎯", "💫", "👑", "🌟", "🔥"]
    response += f" {random.choice(emojis)}"
    
    await ctx.send(response)

@bot.command(name="инфо")
async def инфо(ctx, member: discord.Member = None):
    """Информация об участнике"""
    if not member:
        member = ctx.author
    
    user_stats = stats_db.get_user_stats(str(member.id))
    
    embed = discord.Embed(
        title=f"📋 Информация о {member.name}",
        color=discord.Color.blue()
    )
    
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    embed.add_field(name="📛 Имя", value=member.name, inline=True)
    embed.add_field(name="👤 Ник", value=member.display_name, inline=True)
    embed.add_field(name="🆔 ID", value=member.id, inline=True)
    
    if user_stats:
        embed.add_field(
            name="📊 Сообщений",
            value=user_stats['messages'],
            inline=True
        )
        
        first_seen = datetime.fromisoformat(user_stats['first_seen']).strftime("%d.%m.%Y %H:%M")
        last_seen = datetime.fromisoformat(user_stats['last_seen']).strftime("%d.%m.%Y %H:%M")
        
        embed.add_field(name="📅 Первый раз", value=first_seen, inline=True)
        embed.add_field(name="📅 Последний раз", value=last_seen, inline=True)
    
    embed.set_footer(text=f"Запросил: {ctx.author.name}")
    
    await ctx.send(embed=embed)

@bot.command(name="умер")
async def умер(ctx):
    """Простое приветствие"""
    await ctx.send(f'только ты, {ctx.author.mention}!')

@bot.command(name="ты")
async def ты(ctx, *, вопрос=""):
    """Ответ да/нет на утверждение про тебя"""
    if not вопрос.strip():
        responses = ["🤔 Я что?", "❓ Что 'ты'?", "👂 Не расслышал, повтори"]
        await ctx.send(random.choice(responses))
        return
    
    if random.choice([True, False]):
        ответ = "**✅ ДА**"
    else:
        ответ = "**❌ НЕТ**"
    
    await ctx.send(ответ)

@bot.command(name=",")
async def запятая(ctx):
    """Ответ да/нет"""
    if random.choice([True, False]):
        await ctx.send("✅ ДА")
    else:
        await ctx.send("❌ НЕТ")

@bot.command(name="скинь")
async def скинь(ctx):
    """Отправить гифку"""
    chosen_gif = random.choice(GIFS)
    await ctx.send(f"держи гифку\n{chosen_gif}")

@bot.command(name="шиперим")
async def шиперим(ctx):
    """Случайные два человека"""
    members = [m for m in ctx.guild.members if not m.bot]
    
    if len(members) < 2:
        await ctx.send("😔 Нужно минимум 2 человека в чате!")
        return
    
    # Выбираем двух РАЗНЫХ людей
    person1 = random.choice(members)
    available = [p for p in members if p.id != person1.id]
    person2 = random.choice(available)
    
    phrases = [
        f"{person1.mention} и {person2.mention} - сладкая парочка! 💕",
        f"Смотрите! {person1.mention} + {person2.mention} = любовь! ❤️",
        f"Новая парочка: {person1.mention} & {person2.mention} 🥰",
        f"Шипперим {person1.mention} с {person2.mention}! 💑",
    ]
    
    await ctx.send(random.choice(phrases))

@bot.command(name="ктопобедит")
async def ктопобедит(ctx, *, текст=""):
    """Кто победит"""
    if " или " not in текст.lower():
        await ctx.send("❌ Формат: `аллах ктопобедит [имя] ИЛИ [имя]`")
        return
    
    parts = текст.lower().split(" или ")
    if len(parts) < 2:
        await ctx.send("❌ Формат: `аллах ктопобедит [имя] ИЛИ [имя]`")
        return
    
    winner_text = random.choice([parts[0].strip(), parts[1].strip()])
    
    responses = [
        f"🏆 Победит {winner_text}!",
        f"🎯 Мой выбор: {winner_text} победит!",
        f"⭐ Определённо {winner_text} выиграет!",
    ]
    
    await ctx.send(random.choice(responses))

@bot.command(name="топ")
async def топ(ctx):
    """Топ 10 активных пользователей"""
    top_users = stats_db.get_top_users(limit=10)
    
    if not top_users:
        await ctx.send("📊 Статистика ещё не собрана!")
        return
    
    text = "🏆 **ТОП 10 САМЫХ АКТИВНЫХ:**\n\n"
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for i, (user_id, user_data) in enumerate(top_users):
        medal = medals[i] if i < len(medals) else f"{i+1}."
        text += f"{medal} **{user_data['name']}** - {user_data['messages']} сообщений\n"
    
    await ctx.send(text)

@bot.command(name="кормить")
async def кормить(ctx):
    """Покормить свою свинью"""
    user = ctx.author
    
    # Проверяем можно ли кормить
    can_feed, remaining_time = pig_system.can_feed(str(user.id))
    
    if not can_feed and remaining_time:
        hours = remaining_time.seconds // 3600
        minutes = (remaining_time.seconds % 3600) // 60
        
        time_str = ""
        if hours > 0:
            time_str += f"{hours} ч "
        if minutes > 0:
            time_str += f"{minutes} мин"
        
        await ctx.send(f"⏰ КД ещё не прошло!\nСледующее кормление через: {time_str}")
        return
    
    # Кормим свинью
    pig_data, level_up = pig_system.feed_pig(str(user.id), user.name)
    
    # Определяем статус
    weight = pig_data['weight']
    if weight < 10:
        status = "🐷 Маленький поросёнок"
    elif weight < 50:
        status = "🐽 Подросток-хряк"
    elif weight < 100:
        status = "🐗 Взрослый кабан"
    elif weight < 200:
        status = "🐖 ГИГАНТСКИЙ ХРЯК"
    else:
        status = "👑 БОГ СВИНЕЙ"
    
    text = (
        f"{status}\n"
        f"Вы покормили свою свинью!\n\n"
        f"📊 Вес: **{pig_data['weight']} кг** (+5 кг)\n"
        f"🍽️ Кормлений: **{pig_data['feed_count']}**\n"
        f"⭐ Уровень: **{pig_data['level']}**"
    )
    
    rank = pig_system.get_user_rank(str(user.id))
    if rank:
        text += f"\n🏆 Место в топе: **#{rank}**"
    
    if level_up:
        text += f"\n🎉 **УРОВЕНЬ ПОВЫШЕН!** Теперь уровень {pig_data['level']}!"
    
    await ctx.send(text)

@bot.command(name="свинья")
async def свинья(ctx, member: discord.Member = None):
    """Показать информацию о свинье"""
    if not member:
        member = ctx.author
    
    pig_data = pig_system.get_pig(str(member.id))
    
    if not pig_data:
        await ctx.send(f"У {member.mention} ещё нет свиньи! Напиши `аллах кормить`")
        return
    
    weight = pig_data['weight']
    if weight < 10:
        title = "🐷 Маленький поросёнок"
    elif weight < 50:
        title = "🐽 Подросток-хряк"
    elif weight < 100:
        title = "🐗 Взрослый кабан"
    elif weight < 200:
        title = "🐖 ГИГАНТСКИЙ ХРЯК"
    else:
        title = "👑 БОГ СВИНЕЙ"
    
    text = (
        f"{title} - {member.name}\n\n"
        f"📊 Вес: **{pig_data['weight']} кг**\n"
        f"🍽️ Кормлений: **{pig_data['feed_count']}**\n"
        f"⭐ Уровень: **{pig_data['level']}**\n"
    )
    
    rank = pig_system.get_user_rank(str(member.id))
    if rank:
        text += f"🏆 Место в топе: **#{rank}**\n"
    
    created = datetime.fromisoformat(pig_data['created']).strftime("%d.%m.%Y")
    last_feed = datetime.fromisoformat(pig_data['last_feed']).strftime("%d.%m.%Y %H:%M") if pig_data['last_feed'] else "Никогда"
    
    text += f"📅 Свинья с: **{created}**\n"
    text += f"📅 Последнее кормление: **{last_feed}**"
    
    await ctx.send(text)

@bot.command(name="топсвиней")
async def топсвиней(ctx):
    """Топ 10 самых тяжёлых свиней"""
    top_pigs = pig_system.get_top_pigs(limit=10)
    
    if not top_pigs:
        await ctx.send("🐷 Пока никто не завёл свиней! Напиши `аллах кормить`")
        return
    
    text = "🏆 **ТОП 10 САМЫХ ТЯЖЁЛЫХ СВИНЕЙ:**\n\n"
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for i, (user_id, pig_data) in enumerate(top_pigs):
        medal = medals[i] if i < len(medals) else f"{i+1}."
        
        weight = pig_data['weight']
        if weight < 50:
            emoji = "🐷"
        elif weight < 100:
            emoji = "🐽"
        elif weight < 200:
            emoji = "🐗"
        else:
            emoji = "👑"
        
        text += f"{medal} {emoji} **{pig_data['name']}** - {pig_data['weight']} кг (ур. {pig_data['level']})\n"
    
    await ctx.send(text)

@bot.command(name="диагностика")
async def диагностика(ctx):
    """Диагностика бота"""
    embed = discord.Embed(
        title="🔍 Диагностика бота",
        color=discord.Color.green()
    )
    
    embed.add_field(name="🤖 Имя бота", value=bot.user.name, inline=True)
    embed.add_field(name="🆔 ID бота", value=bot.user.id, inline=True)
    embed.add_field(name="👥 Серверов", value=len(bot.guilds), inline=True)
    
    embed.add_field(name="🎮 Префикс", value=f"`{PREFIX}`", inline=True)
    embed.add_field(name="📅 Время", value=datetime.now().strftime("%H:%M:%S"), inline=True)
    embed.add_field(name="✅ Статус", value="Работает", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="помощь")
async def помощь(ctx):
    """Показать все команды"""
    embed = discord.Embed(
        title="📋 Помощь по командам Аллах-бота",
        description=f"**Префикс:** `{PREFIX}`",
        color=discord.Color.gold()
    )
    
    embed.add_field(
        name="🎲 Основные команды",
        value=(
            "`кто [вопрос]` - Случайный участник\n"
            "`укого [качество]` - Кто обладает качеством\n"
            "`ты [утверждение]` - Да/нет про тебя\n"
            "`,` - Да/нет про участника\n"
            "`скинь` - Случайная гифка\n"
            "`шиперим` - Случайная пара\n"
            "`ктопобедит X ИЛИ Y` - Кто победит"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🐷 Система свиней",
        value=(
            "`кормить` - Покормить свою свинью\n"
            "`свинья [@участник]` - Инфо о свинье\n"
            "`топсвиней` - Топ тяжёлых свиней\n"
            "`топ` - Топ активных пользователей"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔧 Утилиты",
        value=(
            "`инфо [@участник]` - Информация\n"
            "`умер` - Простое приветствие\n"
            "`диагностика` - Проверка бота\n"
            "`помощь` - Эта справка"
        ),
        inline=False
    )
    
    embed.set_footer(text="Бот работает на Railway")
    
    await ctx.send(embed=embed)

# ===================== ЗАПУСК =====================

if __name__ == "__main__":
    print("🚀 Запускаю Discord бота...")
    bot.run(TOKEN)