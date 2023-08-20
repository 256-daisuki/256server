import discord
import random
import requests
import subprocess
import re
import os
import pexpect
import platform
import psutil
import sys
import distro
from datetime import datetime, timezone, timedelta
from discord import app_commands
from discord.ext import commands
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

initial_directory = os.getcwd()

@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()#スラッシュコマンドを同期

# メッセージを受信した時に呼ばれる
@client.event
async def on_message(message):
    # 自分のメッセージを無効
    if message.author == client.user:
        return

    # shellコマンドです
    if message.content.startswith('$'):
        if message.author.id == 891521181990129675:
            cmd = message.content[1:]  # 先頭の$を取り除く
            current_directory = os.getcwd()
            command_with_prompt = f'discord@256server:{current_directory}${cmd}\n'

            # カレントディレクトリを変更する前にコマンドを実行
            result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=current_directory)
            stdout, stderr = result.communicate()
            output = stdout.decode() + stderr.decode()
            
            # カレントディレクトリを変更してから追加のコマンドを実行
            # cdはいろいろとめんどい
            if cmd.startswith("cd "):  # コマンドが「cd 」で始まる場合
                new_directory = cmd[3:].strip()
                os.chdir(new_directory)
                current_directory = os.getcwd()
            
            response = f'```{command_with_prompt}{output}```'
            await message.channel.send(response)
        else:
            await message.channel.send('256大好き!しか実行できません')

@tree.command(name="test",description="テストコマンドです。")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("しらすじゅーす！",ephemeral=False)

@tree.command(name="server_usage",description="サーバーの情報を今すぐ取得")
async def server_info(interaction: discord.Interaction):
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    cpu_bar_blocks = max(int(cpu_usage / 10), 1)
    ram_bar_blocks = max(int(ram_usage / 10), 1)

    cpu_bar = "█" * cpu_bar_blocks + " " * (10 - cpu_bar_blocks)
    ram_bar = "█" * ram_bar_blocks + " " * (10 - ram_bar_blocks)

    embed = discord.Embed(
        title="サーバー使用率",
        color=0x00ff00,
    )

    embed.add_field(name="CPU使用率", value=f"```{cpu_bar}\n{cpu_usage:.2f}%```")
    embed.add_field(name="RAM使用率", value=f"```{ram_bar}\n{ram_usage:.2f}%```")

    await interaction.response.send_message(embed=embed)

@tree.command(name="ping", description="BOTにpingを打ちます")
async def ping_command(interaction: discord.Interaction):
    # Ping値を秒単位で取得
    raw_ping = client.latency

    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000)

    # 送信する
    embed = discord.Embed(
        title="Pong!🏓", 
        color=0x00ff00,
        description=f"BotのPing値は{ping}msです。")
    await interaction.response.send_message(embed=embed)

@tree.command(name="omikuji", description="おみくじ　そのまま")
async def ping_command(interaction: discord.Interaction):
    omikuji = ["大凶","中凶","小凶","末吉凶","吉凶","凶"]
    await interaction.response.send_message(f"今日のお前の運勢 {random.choice(omikuji)}")

@tree.command(name="echo", description="あんなことやそんなことまで言います")
async def echo_command(interaction: discord.Interaction, *, text: str):
    await interaction.response.send_message(text, ephemeral=False)

@tree.command(name="google", description="Googleで検索結果を表示します")
async def google_command(interaction: discord.Interaction, *, search_word: str):
    pages_num = 10 + 1  # 上位から何件までのサイトを抽出するか指定
    result_embed = discord.Embed(title=f"Google検索結果: {search_word}", color=0xfabb05)

    url = f'https://www.google.co.jp/search?hl=ja&num={pages_num}&q={search_word}'
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    search_site_list = soup.select('div.kCrYT > a')

    for site in search_site_list:
        try:
            site_title = site.select('h3.zBAuLc')[0].text
        except IndexError:
            site_title = site.select('img')[0]['alt']
        site_url = site['href'].replace('/url?q=', '').split('&')[0]  # 余計な部分を取り除く
        result_embed.add_field(name=site_title, value=f'({site_url})', inline=False)

    await interaction.response.send_message(embed=result_embed, ephemeral=False)

@tree.command(name="yahoo", description="yahooニュースの記事を出力します")
async def yahoo_news_command(interaction: discord.Interaction):
    URL = "https://www.yahoo.co.jp/"
    rest = requests.get(URL)
    soup = BeautifulSoup(rest.text, "html.parser")

    data_list = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))

    result_embed = discord.Embed(title="Yahooニューストップ見出し", color=0xff0839)
    for data in data_list:
        title = data.span.string
        url = data.attrs["href"]

        # リンクとなるテキストを作成
        link_text = f"{title}"
        result_embed.add_field(name=link_text, value=f'({url})', inline=False)

    await interaction.response.send_message(embed=result_embed, ephemeral=False)

# トークン
client.run('')