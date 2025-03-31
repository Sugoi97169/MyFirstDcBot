from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
}
icon = {
    "ico_circle_yellow": ":yellow_circle:",
    "ico_circle_red": "red_circle",
    "ico_circle_pruple": "pruple_circle",
    "ico_circle_green": "green_circle",
    "ico_circle_blue": "blue_circle"
}
def search_card(card_number):
    base_url = f'https://rugiacreation.com/ua/search?Find1={card_number}'
    r = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.find('span', {'class': 'timing'})!=None:
        effect = soup.find('span', {'class': 'timing'}).find_parent('div')
    elif soup.find('span', {'class': 'underline'})!=None:
        effect = soup.find('span', {'class': 'underline'}).find_parent('div')
    elif soup.find('span', {'class': 'times'})!=None:
        effect = soup.find('span', {'class': 'times'}).find_parent('div')
    elif soup.find('span', {'class': 'effectKeyword'})!=None:
        effect = soup.find('span', {'class': 'effectKeyword'}).find_parent('div')
    else:
        effect = "可能有問題"
    card_img = soup.find("span", {"class": "cards"}).find("img", {"class": "cards"}).get('data-src')
    card_img_link = f"https://rugiacreation.com/ua/{card_img}"
    effect_txt = ""
    if effect != "可能有問題":
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
    else:
        effect_txt = effect
    print(card_number)
    print(card_img_link)
    print(effect_txt)

for i in range(1,10):
    card_number = f"JJK-1-00{i}" #input()
    search_card(card_number)
for i in range(10,101):
    card_number = f"JJK-1-0{i}" #input()
    search_card(card_number)

