import os
from dotenv import load_dotenv  # Aggiungi questa linea per caricare il file .env
import discord
from discord.ext import commands

# Carica il file .env
load_dotenv()

# Recupera il token dal file .env
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Verifica se il token è stato caricato correttamente
if not TOKEN:
    print("Errore: Il token non è stato caricato correttamente.")
else:
    print("Token caricato con successo.")

# Set intents
intents = discord.Intents.default()
intents.members = True  # Required to manage members
intents.message_content = True  # Required to read commands

bot = commands.Bot(command_prefix="!", intents=intents)

# Game settings
GAMER_ROLE_NAME = "Gamer"
LOG_CHANNEL_ID = 1344238527033905206  # Log channel ID
banned_users = []  # List to track banned users in order

# Prizes for the last 10 players
PRIZES = {
    1: "1000 sparks",
    2: "900 sparks",
    3: "800 sparks",
    4: "700 sparks",
    5: "600 sparks",
    6: "500 sparks",
    7: "400 sparks",
    8: "300 sparks",
    9: "200 sparks",
    10: "100 sparks"
}

@bot.event
async def on_ready():
    print(f'✅ Bot online! Logged in as {bot.user}')

# 1️⃣ Test command
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# 2️⃣ BAN command for users with @Gamer
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member):
    author_roles = {role.name for role in ctx.author.roles}
    member_roles = {role.name for role in member.roles}
    
    if GAMER_ROLE_NAME in author_roles and GAMER_ROLE_NAME in member_roles:
        try:
            await member.ban(reason=f'Banned by {ctx.author}')
            banned_users.append(member.name)  # Register banned user

            await ctx.send(f'🚨 {member.mention} has been banned!')

            # Log in the specific channel
            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(f'⚔️ **{member.name}** has been banned by **{ctx.author.name}**!')

            # 3️⃣ Check how many players are left
            guild = ctx.guild
            gamers_left = [m for m in guild.members if discord.utils.get(m.roles, name=GAMER_ROLE_NAME)]

            if len(gamers_left) == 1:
                winner = gamers_left[0]  # The last remaining player is the ultimate winner
                banned_users.append(winner.name)  # Add to the winner list

                await ctx.send(f"🏆 **THE GAME IS OVER!** 🏆\n**{winner.mention} is the ultimate winner!** 🎉🎊")

                # Generate the final leaderboard
                leaderboard = []
                for i, player in enumerate(reversed(banned_users[-10:]), start=1):  # Get the last 10
                    prize = PRIZES.get(i, "No prize")
                    leaderboard.append(f"**{i}º** {player} - 🎁 {prize}")

                # Announce the winners
                leaderboard_text = "\n".join(leaderboard)
                await ctx.send(f"🏅 **Final Leaderboard:**\n{leaderboard_text}")

                if log_channel:
                    await log_channel.send(f"📜 **Final Leaderboard:**\n{leaderboard_text}")

        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to ban this user.")
    else:
        await ctx.send(f"⚠️ You can only ban users with the **{GAMER_ROLE_NAME}** role!")

# Run the bot with the loaded token
bot.run(TOKEN)
