import datetime
import random

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import tasks, commands

# client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix="/", intents=intents)
tz = datetime.timezone(datetime.timedelta(hours=8))
everyday_time = datetime.time(hour=12, minute=00, tzinfo=tz)
URL = "https://play-lh.googleusercontent.com/FNShJS-ArMjI28I4-CHlgWaA9HqKnj4DrW8-lXF2B_FH3U0KxP_djBnMuyK7Hxymxrq8"  # 動畫瘋


def animate(x):
    info = ""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.45 Safari/537.36',
    }
    r = requests.get('https://ani.gamer.com.tw/', headers=headers)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        check = {
            1: soup.select('.programlist-block > .today-list'),
            2: soup.select('.programlist-block > .day-list')
        }
        today_list = check[x]

        for item in today_list:
            day = item.select_one('h3.day-title').text
            anime_infos = item.select('.text-anime-info')
            for anime_info in anime_infos:
                time = anime_info.select_one('span.text-anime-time').text
                name = anime_info.select_one('p.text-anime-name').text
                number = anime_info.select_one('p.text-anime-number').text
                info += "Day:{}\nTime:{}\nAnime Name:{}\nEpisode Number:{}\n------\n".format(day, time, name, number)
        return info
    else:
        print(f'請求失敗：{r.status_code}')


# 調用 event 函式庫
@client.event
# 當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)
    everyday.start()


@client.tree.command(name="today", description="看每日更新")
async def today(interaction: discord.Interaction):
    embed = discord.Embed(title="今日更新", url="https://ani.gamer.com.tw/", description=animate(1), color=0x808080)
    embed.set_author(name="狗蟻寫的今日新番查詢")
    embed.set_thumbnail(url=URL)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="week", description="看本週更新")
async def week(interaction: discord.Interaction):
    embed = discord.Embed(title="本週更新", url="https://ani.gamer.com.tw/", description=animate(2), color=0x00ff00)
    embed.set_author(name="狗蟻寫的本週新番查詢")
    embed.set_thumbnail(url=URL)
    await interaction.response.send_message(embed=embed)


def random_url():
    x = random.randrange(0, 1)
    check = {
        0: str("http://scp-zh-tr.wikidot.com/random:random-scp"),
        1: str("http://scp-zh-tr.wikidot.com/random:random-tale")
    }
    return check[x]


@tasks.loop(time=everyday_time)
async def everyday():
    try:
        channel_id = 1212953165188698173
        channel = client.get_channel(channel_id)
        # 設定發送訊息的頻道ID
        embed = discord.Embed(title="隨機作品", url=random_url(), description="隨機作品", color=0x00ff00)
        embed.set_author(name="隨機作品")
        embed.set_thumbnail(
            url="https://lh3.googleusercontent.com/a/ACg8ocLA-LdiwIeFif-mL4WueXFLPpyP2J8nrENoXPFuriOdvhM=s288-c-no")
        await channel.send(embed=embed)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    client.run('機器人金鑰')
