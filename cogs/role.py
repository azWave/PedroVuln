import discord
from discord.ext import commands
from discord.ext.commands import Context



class Role(commands.Cog, name="role"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="makemeadmin", description="Give to user the PedroMaster role"
    )
    @commands.has_permissions(manage_roles=True)
    async def makemeadmin(
        self,
        context: Context,
    ) -> None:
        role = discord.utils.get(context.guild.roles,id=1232261601080643674)
        print(role)
        await context.author.add_roles(role)

    @commands.hybrid_command(
        name="boulecristal", description="Somme bouledecristal.h "
    )
    async def boulecristal(
        self,
        context: Context,
        to: discord.User = commands.parameter(default=lambda ctx: ctx.author),
    ) -> None:
        print(to.roles)

async def setup(bot) -> None:
    await bot.add_cog(Role(bot))
