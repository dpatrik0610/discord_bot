import discord
from discord import app_commands
from discord.ext import commands

class TestCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("TestCog initialized!")

    @app_commands.command(name="test", description="Test command")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test command works!")