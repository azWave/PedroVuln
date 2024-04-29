import discord
from discord.ext import commands
from discord.ext.commands import Context
from sqlalchemy import text


class Points(commands.Cog, name="points"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="createuserpoints", description="Create user's points score."
    )
    async def createuserpoints(
        self,
        context: Context,
        to: discord.User = commands.parameter(default=lambda ctx: ctx.author),
    ) -> None:
        if "pedromanager" in [r.name for r in context.author.roles]:
            sql = text(
                f"INSERT INTO `PedroBase`.`Points` (`DiscordUser`, `GuildId`) VALUES ('{to.id}', '{context.guild.id}');"
            )
            try:
                with self.bot.database.connect() as conn:
                    conn.execute(sql)
                    conn.commit()
            except Exception as e:
                embed = discord.Embed(
                    description="Problem with Database", color=0xE02B2B
                )
                embed.add_field(name="Error", value=f"```{e}```")
                await context.send(embed=embed)
                return
            embed = discord.Embed(
                description="Command completed with success", color=0xBEBEFE
            )

            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                description="You are not allowed to use this command", color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="getpoints", description="get to a spesifc user's points score."
    )
    async def getpoints(
        self,
        context: Context,
        to: discord.User = commands.parameter(default=lambda ctx: ctx.author),
    ) -> None:
        sql = text(
            f"SELECT * FROM PedroBase.Points WHERE (`DiscordUser` = '{to.id}') and (`GuildId` = '{context.guild.id}');"
        )
        try:
            with self.bot.database.connect() as conn:
                resultSql = conn.execute(sql).mappings().one()

        except Exception as e:
            embed = discord.Embed(description="Problem with Database", color=0xE02B2B)
            embed.add_field(name="Error", value=f"```{e}```")
            await context.send(embed=embed)
            return

        embed = discord.Embed(color=0xBEBEFE)
        embed.set_author(
            name=context.author.display_name, icon_url=context.author.display_avatar
        )
        embed.add_field(
            name="Score",
            value=f"{context.author.display_name} has {resultSql['PointsAmount']} points.",
        )

        await context.send(embed=embed)

    @commands.hybrid_command(name="setpoint", description="set points of a user.")
    async def setpoint(
        self,
        context: Context,
        amount: int,
        to: discord.User = commands.parameter(default=lambda ctx: ctx.author),
    ) -> None:
        if "pedromanager" in [r.name for r in context.author.roles]:
            sql = text(
                f"UPDATE `PedroBase`.`Points` SET `PointsAmount` = '{amount}' WHERE (`DiscordUser` = '{to.id}') and (`GuildId` = '{context.guild.id}');"
            )
            try:
                with self.bot.database.connect() as conn:
                    conn.execute(sql)
                    conn.commit()
            except Exception as e:
                embed = discord.Embed(
                    description="Problem with Database", color=0xE02B2B
                )
                embed.add_field(name="Error", value=f"```{e}```")
                await context.send(embed=embed)
                return
            embed = discord.Embed(
                description="Command completed with success", color=0xBEBEFE
            )

            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                description="You are not allowed to use this command", color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.hybrid_command(name="deletepoints", description="set points of a user.")
    async def deletepoints(
        self,
        context: Context,
        to: discord.User = commands.parameter(default=lambda ctx: ctx.author),
    ) -> None:
        if "pedromanager" in [r.name for r in context.author.roles]:
            sql = text(
                f"DELETE FROM `PedroBase`.`Points` WHERE (`DiscordUser` = '{to.id}') and (`GuildId` = '{context.guild.id}');"
            )
            try:
                with self.bot.database.connect() as conn:
                    conn.execute(sql)
                    conn.commit()
            except Exception as e:
                embed = discord.Embed(
                    description="Problem with Database", color=0xE02B2B
                )
                embed.add_field(name="Error", value=f"```{e}```")
                await context.send(embed=embed)
                return
            embed = discord.Embed(
                description="Command completed with success", color=0xBEBEFE
            )

            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                description="You are not allowed to use this command", color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="gettop", description="get classement on top (max 20)"
    )
    async def gettop(self, context: Context, top: int = 3) -> None:
        top = max(min(20, top), 3)
        sql = text(
            f"SELECT * FROM PedroBase.Points WHERE (`GuildId` = '{context.guild.id}') order by PointsAmount desc;"
        )
        try:
            with self.bot.database.connect() as conn:
                users = conn.execute(sql).mappings().all()

        except Exception as e:
            embed = discord.Embed(description="Problem with Database", color=0xE02B2B)
            embed.add_field(name="Error", value=f"```{e}```")
            await context.send(embed=embed)
            return

        embed = discord.Embed(title=f"Top {top}:", color=0xBEBEFE)
        for u in users[:top]:
            currentUser = await self.bot.fetch_user(int(u["DiscordUser"]))
            embed.add_field(
                name=f"Top {users.index(u)+1}: {currentUser.display_name}",
                value=f"{currentUser} has {u['PointsAmount']} points.",
            )

        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Points(bot))
