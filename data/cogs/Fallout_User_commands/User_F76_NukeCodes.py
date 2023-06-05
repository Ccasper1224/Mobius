# import discord library
import json
import discord
import requests
import configparser

# Imports commands
from discord.ext import commands
from discord import app_commands
# Allows the code to retrieve data online
from datetime import datetime

from data.functions.logging import get_log
logger = get_log(__name__)


class User_F76_NukeCodes(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()  # Important for grouping Slash commands

    @app_commands.command(name="codes", description="Will output the current nuke codes for Fallout 76")
    async def codes(self, interaction: discord.Interaction) -> None:
        """ /codes """
        logger.info("A user requested nuke codes")
        config = configparser.ConfigParser()
        config.read("./config.ini")

        data = config["NukaCrypt"]["API_key"]
        header = config["NukaCrypt"]["Header"]
        r = requests.post(url=f'https://nukacrypt.com/api/codes', data=json.loads(data), headers=json.loads(header))
        if str(r.status_code) == "500":
            await interaction.response.send_message("NukaCrypt is currently experiencing issues.\n"
                                                    "Please report the issue to our community server if you can!")
        else:
            response = r.json()

            embed = discord.Embed(color=0xe7e9d3, title="Fallout 76 Nuclear Codes")
            embed.set_footer(text="Special thanks to https://nukacrypt.com/ for providing codes for all these years!")

            if response["ALPHA"] == "34959739":
                warning = "This is the notorious 8 day code week. Meaning the codes will last for 8 days and not 7. " \
                          "Once per year, there is an overlap in nuke codes. That happens to be this week, " \
                          "where there are 8 days instead of 7 days. When the codes reset. " \
                          "We recommend that you wait 1 day to avoid confusion & " \
                          "risk of potential loss of nuclear key cards."
                embed.add_field(name="⚠️WARNING⚠️", value=warning, inline=False)
            elif response["ALPHA"] == "45836295":
                warning = "First day of code reset?\n" \
                          "Please use the following codes instead.\n" \
                          "**Alpha**: 34959739\n" \
                          "**Bravo**: 33701503\n" \
                          "**Charlie**2: 98469385\n" \
                          "Why you might ask?\n" \
                          "Last week was the notorious 8 day code week. " \
                          "Meaning the codes will last for 8 days and not 7.\n" \
                          "Once per year, there is an overlap in nuke codes. That happens to be last week, " \
                          "where there are 8 days instead of 7 days."
                embed.add_field(name="⚠️WARNING⚠️", value=warning, inline=False)
            code_response = f'Nuke codes reset in <t:{response["since_epoch"]+604800}:R>\n' \
                            f'which is every <t:{response["since_epoch"]+604800}:F> \n' \
                            f'**Alpha**: {response["ALPHA"]}\n' \
                            f'**Bravo**: {response["BRAVO"]}\n' \
                            f'**Charlie**: {response["CHARLIE"]}'

            config = configparser.ConfigParser()
            config.read("./config.ini")
            embed.set_thumbnail(url=config["EDB.TOOLS"]["F76_NukeCodes"])

            embed.add_field(name="This week's nuclear codes",
                            value=code_response)

            # await interaction.response.send_message(code_response)
            await interaction.response.send_message(embed=embed)

    @commands.command(name="codes", aliases=["nukecodes", "nukecode", "nc", "code", "cc"])
    async def _codes(self, ctx):
        logger.info("A user requested nuke codes")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        await ctx.send(config["LEGACY"]["UseSlash"])

        data = config["NukaCrypt"]["API_key"]
        header = config["NukaCrypt"]["Header"]
        r = requests.post(url=f'https://nukacrypt.com/api/codes', data=json.loads(data), headers=json.loads(header))
        response = r.json()
        code_response = f'Nuke codes reset in <t:{response["since_epoch"]+604800}:R>\n' \
                        f'which is every <t:{response["since_epoch"]+604800}:F> \n' \
                        f'**Alpha**: {response["ALPHA"]}\n' \
                        f'**Bravo**: {response["BRAVO"]}\n' \
                        f'**Charlie**: {response["CHARLIE"]}'
        await ctx.send(code_response)


# ends the extension
async def setup(client: commands.Bot) -> None:
    await client.add_cog(User_F76_NukeCodes(client))