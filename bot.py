import discord
from discord.ext import commands
import config
import logging
import atexit
from datetime import datetime

# Set up logging (Railway-friendly - no file logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Only console output
    ]
)
logger = logging.getLogger(__name__)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        
        # Log startup
        logger.info("Bot starting up...")

    async def setup_hook(self):
        # Add cogs
        from cogs.dice_cog import DiceCog
        await self.add_cog(DiceCog(self))
        logger.info("DiceCog loaded successfully")
        
        # Sync commands
        if hasattr(config, 'TEST_GUILD_ID') and config.TEST_GUILD_ID:
            guild = discord.Object(id=config.TEST_GUILD_ID)
            self.tree.clear_commands(guild=guild)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            logger.info(f"Synced {len(synced)} commands to guild {config.TEST_GUILD_ID}")
        else:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} commands globally")

    async def on_ready(self):
        logger.info(f"Bot ready! Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"Connected to {len(self.guilds)} guilds")

    async def on_app_command_completion(self, interaction: discord.Interaction, command):
        """Log when slash commands are used"""
        user = interaction.user
        guild = interaction.guild.name if interaction.guild else "DM"
        logger.info(f"Command used: /{command.name} by {user.name}#{user.discriminator} in {guild}")

    async def on_app_command_error(self, interaction: discord.Interaction, error):
        """Log slash command errors"""
        user = interaction.user
        guild = interaction.guild.name if interaction.guild else "DM"
        logger.error(f"Command error: /{interaction.command.name if interaction.command else 'unknown'} by {user.name}#{user.discriminator} in {guild} - {error}")

def on_shutdown():
    """Called when the bot shuts down"""
    logger.info("Bot shutting down...")

if __name__ == "__main__":
    # Register shutdown handler
    atexit.register(on_shutdown)
    
    try:
        bot = MyBot()
        bot.run(config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
    finally:
        logger.info("Bot process ended")