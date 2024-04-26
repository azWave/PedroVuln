import platform

import discord
from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        # self.context_menu_user = app_commands.ContextMenu(
        #     name="Grab ID", callback=self.grab_id
        # )
        # self.bot.tree.add_command(self.context_menu_user)
        # self.context_menu_message = app_commands.ContextMenu(
        #     name="Remove spoilers", callback=self.remove_spoilers
        # )
        # self.bot.tree.add_command(self.context_menu_message)

    @commands.hybrid_command(
        name="help", description="List all commands the bot has loaded."
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="Help", description="List of available commands:", color=0xBEBEFE
        )
        for i in self.bot.cogs:
            if i == "owner" and not (await self.bot.is_owner(context.author)):
                continue
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context: Context) -> None:
        embed = discord.Embed(color=0xBEBEFE)
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="azWave#1649", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.config['prefix']} for normal commands",
            inline=False,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    
    @commands.hybrid_command(
        name="wave",
        description="Wave a member",  
    )
    async def wave(self,ctx, to: discord.User = commands.parameter(default=lambda ctx: ctx.author)):
        await ctx.send(f'Hello {to.mention} :wave:')

    


async def setup(bot) -> None:
    await bot.add_cog(General(bot))
