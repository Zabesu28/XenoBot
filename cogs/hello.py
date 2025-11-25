import discord
from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        if ctx.author.id == 591618906519633930:
            await ctx.send(f'Mais dit donc ca ne serait pas cette poufiasse de {ctx.author.name} ?')
            
        elif ctx.author.id == 430749094135201792:
            await ctx.send(f'Comment va mon roux préféré ?')

        elif ctx.author.id == 717101929271918692:
            await ctx.send(f'Wsh {ctx.author.name} ca bz ou bien ?')

        elif ctx.author.id == 335739159467655168:
            await ctx.send(f'Bonjour créateur')
        else:
            await ctx.send(f'Ouais {ctx.author.name}, sdq ?')

        

async def setup(bot):
    await bot.add_cog(Hello(bot))