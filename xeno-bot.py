import discord
import os
import json
import asyncio
import random
import aiohttp
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timedelta
from quiz import fetch_quiz_data

load_dotenv()

# Chargement des tokens
guild_token = int(os.getenv('GUILD_ID'))
bot_token = os.getenv('BOT_TOKEN')

reaction_options = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']

# Configuration des intentions
intents = discord.Intents.all()  # Permet au bot d'écouter tous les événements possibles

# Initialisation du bot avec un préfixe et les intentions
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

    # Charger les cogs ici
    await bot.load_extension('cogs.hello')
    await bot.load_extension('cogs.events')
    # daily_water_reminder.start()

    # Remplacez VOTRE_GUILD_ID par l'ID de votre serveur
    guild = bot.get_guild(guild_token)

    
    if guild is not None:
        print(f'Liste des membres de {guild.name}:')
        for member in guild.members:
            print(member.name, member.id)  # Affiche le nom du membre
        # for channel in guild.channels:
        #     print(channel.name, channel.id)  # Affiche le nom du membre
    else:
        print("Guild non trouvée")

@bot.command()
async def card(ctx):
    # Création de l'embed
    embed = discord.Embed(
        title="Alo salam",
        description="OHAHAHAHAH",
        color=discord.Color.purple()
    )
    
    embed.set_image(url="https://pbs.twimg.com/media/FtYIqhhXwAMA2vn.jpg")  # Remplacez par une URL d'image valide
    embed.set_footer(text="Bassem ton gros crane")
    
    await ctx.send(embed=embed)

@bot.command()
async def me(ctx):
    # Création de l'embed
    user = ctx.author
    embed = discord.Embed(
        title=user.name,
        color=discord.Color.purple()
    )
    
    embed.set_image(url=user.avatar.url)  # user.avatar.url pour l'URL de l'avatar
    await ctx.send(embed=embed)

@bot.command()
async def join(ctx):
    """Command to make the bot join the voice channel."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"C'est bon chui co à {channel}")
    else:
        await ctx.send("T'es meme pas en voc espèce de golmon")

@bot.command()
async def leave(ctx):
    """Command to make the bot leave the voice channel."""
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("C'est bon chui déco.")
    else:
        await ctx.send("Chui meme pas co mgl.")

@tasks.loop(hours=24)  # Répète toutes les 24 heures
async def daily_water_reminder():
    now = datetime.now()
    
    # Vérifie si l'heure actuelle est 12h
    print(f"Heure actuelle : {now.strftime('%H:%M:%S')}")
    if now.hour == 12 and now.minute == 40:
        channel = bot.get_channel(1062478775440392202)  # Remplacez par l'ID de votre canal
        if channel:  # Vérifiez si le canal existe
            await channel.send("N'oubliez pas de boire de l'eau ! 💧")
            print("Message envoyé avec succès.")
        else:
            print("Erreur : canal introuvable.")

    # Attendre jusqu'à la prochaine exécution (dans ce cas, 60 secondes)
    await asyncio.sleep(60)  # Vérifie toutes les minutes si l'heure est 12h


@daily_water_reminder.before_loop
async def before_daily_water_reminder():
    # Attendre jusqu'à demain à 12h10
    now = datetime.now()
    target_time = now.replace(hour=12, minute=40, second=0, microsecond=0)
    
    if target_time < now:
        target_time += timedelta(days=1)

    wait_time = (target_time - now).total_seconds()
    print(f"Attente de {wait_time} secondes avant la première exécution.")
    await asyncio.sleep(wait_time)

@bot.command(name='quiz')
async def quiz(ctx):
    quiz_data = await fetch_quiz_data()  # Récupère les questions depuis l'API

    question = random.choice(quiz_data)  # Sélectionne une question au hasard
    options = question['incorrect_answers'] + [question['correct_answer']]  # Combine réponses incorrectes et correcte
    random.shuffle(options)  # Mélange les options pour les rendre aléatoires

    # Formatage de la question et des options
    options_text = '\n'.join([f"{reaction_options[i]} {option}" for i, option in enumerate(options)])
    question_text = f"**{question['question']}**\n\n{options_text}\n\nRépondez en cliquant sur la réaction correspondante."

    # Envoi de la question
    quiz_message = await ctx.send(question_text)

    # Ajoute les réactions sous le message
    for i in range(len(options)):
        await quiz_message.add_reaction(reaction_options[i])

    def check_reaction(reaction, user):
        return user == ctx.author and str(reaction.emoji) in reaction_options and reaction.message.id == quiz_message.id

    try:
        # Attend que l'utilisateur réagisse
        reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check_reaction)
        answer_index = reaction_options.index(str(reaction.emoji))

        # Vérifie si la réponse est correcte
        if options[answer_index] == question['correct_answer']:
            await ctx.send(f"Correct ! 🎉 La réponse est bien **{question['correct_answer']}**.")
        else:
            await ctx.send(f"Faux ! ❌ La bonne réponse était **{question['correct_answer']}**.")
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé ! ⏰ Vous avez mis trop de temps à répondre.")

# Connectez le bot avec votre token
bot.run(bot_token)