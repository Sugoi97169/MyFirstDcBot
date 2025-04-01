import discord
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
}
icon = {
    "ico_circle_yellow": ":yellow_circle:",
    "ico_circle_red": ":red_circle:",
    "ico_circle_pruple": ":pruple_circle:",
    "ico_circle_green": ":green_circle:",
    "ico_circle_blue": ":blue_circle:"
}
def search_card(card_number):
    base_url = f'https://rugiacreation.com/ua/search?Find1={card_number}'
    r = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    effect = soup.find("div",{"class": "infoBox"}).find_next_sibling('div')
    card_img = soup.find("span", {"class": "cards"}).find("img", {"class": "cards"}).get('data-src')
    card_img_link = f"https://rugiacreation.com/ua/{card_img}"
    effect_txt = ""
    if effect != "":
        for node in effect.children:
            if node.name == 'img':
                img_src = urljoin(base_url, node['src'])
                # 你可以根據檔名判斷用什麼符號取代
                for i in icon.keys():
                    if i in node['src']:
                        effect_txt += icon[i]  # 或用 :yellow_circle: 之類的表情碼
                    else:
                        effect_txt += ""
            elif hasattr(node, 'string') and node.string:
                effect_txt += node.string.strip() + " "

            elif isinstance(node, str):
                effect_txt += node.strip()
    elif effect == "":
        effect_txt="無效果"
    if soup.find("span", {"class": "raidBorder"})!=None:
        effect_txt += "突襲"+soup.find("span", {"class": "raidBorder"}).text

    embed = discord.Embed(title="UA查詢",description=effect_txt,color=0x00ff00)
    embed.set_image(url=card_img_link)
    return embed



