import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore les messages envoyés par le bot lui-même
        if message.author == self.bot.user:
            return

        # Vérifie si le message est exactement "quoi" ou termine par "quoi"
        if message.content.lower() == 'quoi' or message.content.lower().endswith('quoi'):
            await message.channel.send('feur')

        if message.content.lower() == 'suce' or message.content.lower() == 'suces':
            await message.channel.send('Bonsoir, Non.')

        # Si vous voulez que d'autres commandes continuent de fonctionner
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.bot.user:
            return
        channel = after.channel
        await channel.send(f"Pourquoi tu modifies ton message {before.author.mention}. Le message de base c'était : {before.content}")

async def setup(bot):
    await bot.add_cog(Events(bot))