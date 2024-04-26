import discord
from discord.ext import commands
from discord.ext.commands import Context
from sqlalchemy import text


class Challenges(commands.Cog, name="challenges"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="createchall", description="Create a new challenge.")
    async def createchall(
        self, context: Context, ask: str, response: str, points: int
    ) -> None:
        if "PedroManager" in [r.name for r in context.author.roles]:
            sql = text(
                f"INSERT INTO `Pedro`.`Challenge` (`ChallengeAsk`, `ChallengeResponse`, `ChallengePoint`) VALUES ('{ask}', '{response}', '{points}');"
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
        name="getchall",
        description="Get specific challenge set name to all if you want all challenges",
    )
    async def getchall(self, context: Context, name: str, page: int = 1) -> None:
        name = "%" if name == "all" else name
        sql = text(f"SELECT * FROM PedroBot.Chall where ChallName like '{name}';")
        try:
            with self.bot.database.connect() as conn:
                result = conn.execute(sql).mappings().all()
        except Exception as e:
            embed = discord.Embed(description="Problem with Database", color=0xE02B2B)
            embed.add_field(name="Error", value=f"```{e}```")

            await context.send(embed=embed)
            return

        if "PedroManager" not in [r.name for r in context.author.roles]:
            result = [d for d in result if d["ChallAvailable"] == 1]

        embed = discord.Embed(description="item successfully challenge", color=0xBEBEFE)
        page -= 1
        size = 5
        content = [result[i : i + size] for i in range(0, len(result), size)]
        page = max(0, min(len(content) - 1, page))
        for c in content[page]:
            if "PedroManager" in [r.name for r in context.author.roles]:
                embed.add_field(
                    name=c["ChallName"],
                    value=f"{c['ChallAsk']}\nPoints: {c['ChallPoints']}\nAnswer: {c['ChallAnswer']} Available: {c['ChallAvailable']}",
                    inline=False,
                )
            else:
                embed.add_field(
                    name=c["ChallName"],
                    value=f"{c['ChallAsk']}\nPoints: {c['ChallPoints']}",
                    inline=False,
                )
        embed.set_footer(text=f"page {page +1 }/{len(content)}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="updatechall",
        description="Update a specific challengechallenge available.",
    )
    async def updatechall(
        self,
        context: Context,
        name: str,
        ask: str = "",
        answer: str = "",
        points: str = "",
        available: str = "",
    ) -> None:

        if "PedroManager" in [r.name for r in context.author.roles]:

            sqlSelect = text(
                f"SELECT ChallName , ChallAsk , ChallAnswer , ChallPoints , ChallAvailable FROM PedroBot.Chall where ChallAvailable = 1 and ChallName like '{name}';"
            )
            try:
                with self.bot.database.connect() as conn:
                    init = conn.execute(sqlSelect).mappings().one()

                    json = {
                        "ChallAsk": init["ChallAsk"] if ask == "" else ask,
                        "ChallAnswer": init["ChallAnswer"] if answer == "" else answer,
                        "ChallPoints": init["ChallPoints"] if points == "" else points,
                        "ChallAvailable": (
                            init["ChallAvailable"] if available == "" else available
                        ),
                    }
                    sqlUpdate = text(
                        f"UPDATE `PedroBot`.`Chall` SET `ChallAsk` = '{json['ChallAsk']}', `ChallAnswer` = '{json['ChallAnswer']}', `ChallPoints` = '{json['ChallPoints']}', `ChallAvailable` = '{json['ChallAvailable']}' WHERE (`ChallName` = '{name}');"
                    )
                    conn.execute(sqlUpdate)
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
        name="delchall", description="Delete a specific challengechallenge available."
    )
    async def delchall(self, context: Context, name: str) -> None:
        if "PedroManager" in [r.name for r in context.author.roles]:
            sql = text(
                f"DELETE FROM `PedroBot`.`Chall` WHERE (`ChallName` = '{name}');"
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

    @commands.hybrid_command(name="answerchall", description="answer to a challenge")
    async def answerchall(self, context: Context, name: str, answer: str) -> None:
        sqlSelectC = text(
            f"SELECT ChallName , ChallAsk , ChallAnswer , ChallPoints , ChallAvailable FROM PedroBot.Chall where ChallAvailable = 1 and ChallName like '{name}';"
        )
        try:
            with self.bot.database.connect() as conn:
                CurentChall = conn.execute(sqlSelectC).mappings().one()
        except Exception as e:
            embed = discord.Embed(description="Problem with Database", color=0xE02B2B)
            embed.add_field(name="Error", value=f"```{e}```")

            await context.send(embed=embed)
            return

        if CurentChall["ChallAnswer"] == answer:
            embed = discord.Embed(description="Good Answer", color=0xBEBEFE)
            embed.add_field(
                name="reward",
                value=f"This success give you {CurentChall['ChallPoints']} points",
            )

            sqlSelectP = text(
                f"SELECT * FROM PedroBot.Points WHERE (`DiscordUser` = '{context.author.id}') and (`GuildId` = '{context.guild.id}');"
            )

            sqlInsertP = text(
                f"INSERT INTO `PedroBot`.`Points` (`DiscordUser`, `GuildId`, `PointsAmount`) VALUES ('{context.author.id}', '{context.guild.id}','{CurentChall['ChallPoints']}');"
            )
            try:
                with self.bot.database.connect() as conn:
                    selectResult = conn.execute(sqlSelectP).mappings().all()
                    if len(selectResult) > 0:
                        amount = (
                            selectResult[0]["PointsAmount"] + CurentChall["ChallPoints"]
                        )
                        sqlUpdateP = text(
                            f"UPDATE `PedroBot`.`Points` SET `PointsAmount` = '{amount}' WHERE (`DiscordUser` = '{context.author.id}') and (`GuildId` = '{context.guild.id}');"
                        )
                        conn.execute(sqlUpdateP)
                        conn.commit()
                    else:
                        conn.execute(sqlInsertP)
                        conn.commit()

            except Exception as e:
                embed = discord.Embed(
                    description="Problem with Database", color=0xE02B2B
                )
                embed.add_field(name="Error", value=f"```{e}```")

                await context.send(embed=embed)
                return

            # get actula points
            # update
            # or insert if not have points

        else:
            embed = discord.Embed(description="Problem with Database", color=0xE02B2B)

        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Challenges(bot))
