import discord
from discord.ext import commands
import config

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Add cogs
        from cogs.dice_cog import DiceCog
        await self.add_cog(DiceCog(self))
        from cogs.test_cog import TestCog
        await self.add_cog(TestCog(self))
        
        # Sync commands
        if hasattr(config, 'TEST_GUILD_ID') and config.TEST_GUILD_ID:
            guild = discord.Object(id=config.TEST_GUILD_ID)
            self.tree.clear_commands(guild=guild)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands to guild")
        else:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands globally")

    async def on_ready(self):
        print(f"Bot ready! Logged in as {self.user}")

if __name__ == "__main__":
    bot = MyBot()
    bot.run(config.DISCORD_TOKEN)