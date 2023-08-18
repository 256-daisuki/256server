import discord
import random
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()#スラッシュコマンドを同期

@tree.command(name="test",description="テストコマンドです。")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("しらすじゅーす！",ephemeral=False)

@tree.command(name="ping", description="BOTにpingを打ちます")
async def ping_command(interaction: discord.Interaction):
    # Ping値を秒単位で取得
    raw_ping = client.latency

    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000)

    # 送信する
    embed = discord.Embed(title="Pong!🏓", description=f"BotのPing値は{ping}msです。")
    await interaction.response.send_message(embed=embed)

@tree.command(name="omikuji", description="おみくじ　そのまま")
async def ping_command(interaction: discord.Interaction):
    omikuji = ["凶", "大凶"]
    await interaction.response.send_message(f"今日のお前の運勢 {random.choice(omikuji)}")

# メッセージを受信した時に呼ばれる
@client.event
async def on_message(message):
    # 自分のメッセージを無効
    if message.author == client.user:
        return

# トークン
client.run('ここに貴方のトークンを配置')