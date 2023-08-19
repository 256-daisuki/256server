import discord
from discord.ext import commands
import numpy as np
import matplotlib
matplotlib.use('agg')  # バックエンドを切り替える
import matplotlib.pyplot as plt

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.command(name="polygon", description="n角形の図形を描画します")
async def polygon_command(ctx, n: int):
    angle = 360 / n

    vertices = []
    for i in range(n):
        theta = np.radians(i * angle)
        x = np.cos(theta)
        y = np.sin(theta)
        vertices.append((x, y))

    fig, ax = plt.subplots()

    for i in range(n):
        ax.plot([vertices[i][0], vertices[(i + 1) % n][0]],
                [vertices[i][1], vertices[(i + 1) % n][1]], color='b')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.set_facecolor((0, 0, 0, 0))
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.grid(False)

    plt.savefig("transparent_polygon_no_labels.png", transparent=True, bbox_inches='tight', pad_inches=0)

    with open("transparent_polygon_no_labels.png", "rb") as file:
        picture = discord.File(file)
        await ctx.send(file=picture)

bot.run('MTE0MTg4NjQxNzYxODg4MjYyMA.G7IRxa.ZADUXXpEh-9uD5yBUAMJwNllLCZ01TfK5LL-vk')
