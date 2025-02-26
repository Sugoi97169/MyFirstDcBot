import datetime
import random

import discord
import requests
from ua_scrpaer import get_tier_dict
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import tasks, commands
from discord.app_commands import Choice

# client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix="/", intents=intents)
tz = datetime.timezone(datetime.timedelta(hours=8))
everyday_time = datetime.time(hour=12, minute=00, tzinfo=tz)
URL = "https://play-lh.googleusercontent.com/FNShJS-ArMjI28I4-CHlgWaA9HqKnj4DrW8-lXF2B_FH3U0KxP_djBnMuyK7Hxymxrq8"  # 動畫瘋
ptcg_URL = "https://asia.pokemon-card.com/hk/archive/common/assets_c/2020/10/CH-TCG_logo-thumb-650xauto-15381.png" # 寶可夢牌組
ua_url="https://torecards.com/wp-content/uploads/2023/08/Tierアートボード-1-600x315.png"

def poke_deck_response(x):
    response = requests.get(f"https://pokecabook.com/archives/{x}")
    soup = BeautifulSoup(response.text, "html.parser")
    return soup
def poke_deck_name(x):
    pokemon = poke_deck_response(x).find("h1").text
    pokemon = pokemon.replace("環境デッキレシピまとめ", "")
    return pokemon

def poke_deck(x):
    soup = poke_deck_response(x)
    results = soup.find_all("img", {"width": "800", "height": "400"}, limit=30)
    titles = soup.find_all("figcaption", {"class": "wp-element-caption"}, limit=30)
    image_links = []
    text = []
    info = ""
    for result in results:
        src = result.get("src")
        if len(image_links) == 10:
            break
        if "http" in src:
            image_links.append(src)
    for title in titles:
        if len(text) == 10:
            break
        else:
            text.append(title.text)
    for i in range(0, 10):
        info += (f"{image_links[i]}\n{text[i]}\n-----\n")
    print(info)
    return info


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
    slash = await client.tree.sync()
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


@client.tree.command(name="ptcg", description="查詢上位牌組")
@app_commands.describe(pokemon_name="輸入寶可夢名稱")
@app_commands.choices(
    pokemon_name=[
        Choice(name="雄偉牙", value=2003),
        Choice(name="皮卡丘", value=155139),
        Choice(name="忍蛙", value=111205),
        Choice(name="草貓", value=40222),
        Choice(name="惡噴", value=5717),
        Choice(name="電蜘蛛", value=137410),
        Choice(name="密勒頓", value=2278),
        Choice(name="鐵荊棘", value=111240),
        Choice(name="多龍",value=122503)
    ])
async def ptcg(interaction: discord.Interaction, pokemon_name: Choice[int]):
    embed = discord.Embed(title=f"{poke_deck_name(pokemon_name.name)}", url="", description=poke_deck(pokemon_name.value), color=0x00ff00)
    embed.set_author(name="狗蟻寫的寶可夢牌組查詢")
    embed.set_thumbnail(url=ptcg_URL)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="ua", description="看UAt表")
@app_commands.describe(union_arena="T幾")
@app_commands.choices(
    union_arena=[
        Choice(name="T1", value=0),
        Choice(name="T1.5", value=1),
        Choice(name="T2", value=2),
        Choice(name="T2.5", value=3),
        Choice(name="T3", value=4),
        Choice(name="T4", value=5),
        Choice(name="T5", value=6)
    ])
async def ua(interaction: discord.Interaction, union_arena: Choice[int]):
    embed = discord.Embed(title=f"{union_arena.name}", url="https://torecards.com/unionarenatier/", description=get_tier_dict(union_arena.value), color=0x808080)
    embed.set_author(name="狗蟻寫的UAt表")
    embed.set_thumbnail(url=ua_url)
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
    client.run(os.getenv('token'))
