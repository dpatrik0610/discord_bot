import discord
from discord import app_commands
from discord.ext import commands
from domain.dice_roller import DiceRoller
from infrastructure.api_client import DiceAPIClient
import config

class DiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.roller = DiceRoller()
        self.api_client = DiceAPIClient(config.API_BASE_URL)

    @app_commands.command(name="roll", description="Roll dice using D&D notation")
    async def roll(self, interaction: discord.Interaction, roll: str):
        try:
            result = self.roller.roll(roll)
            
            # Try to send the API call but don't let it break the command if it fails
            try:
                self.api_client.send_roll(interaction.user.name, roll, result)
            except Exception as api_error:
                print(f"API call failed: {api_error}")  # Log but continue
            
            # Build a clean string for each die
            details_list = []
            for die in result["details"]:
                # Include modifier only if non-zero
                mod_str = f"+{die.modifier}" if die.modifier > 0 else f"{die.modifier}" if die.modifier < 0 else ""
                details_list.append(f"🎲 `{die.count}d{die.sides}{mod_str}` → rolls {die.rolls} = **{die.subtotal}**")
            
            details_str = "\n".join(details_list)
            
            await interaction.response.send_message(
                f"**{interaction.user.display_name}** rolled `{roll}`:\n"
                f"{details_str}\n\n**Total = {result['total']}**"
            )
            
        except ValueError as e:
            # Ephemeral message so only the user sees it
            await interaction.response.send_message(f"❌ {e}", ephemeral=True)
        except Exception as e:
            # Catch any other errors
            print(f"Unexpected error in roll command: {e}")
            await interaction.response.send_message(f"❌ An unexpected error occurred.", ephemeral=True)
