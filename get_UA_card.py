from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from sentry_sdk.metrics import timing
card_number = "JJK-1-001" #input()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
}
icon = {
    "ico_circle_yellow": ":yellow_circle:"

}
base_url = f'https://rugiacreation.com/ua/search?Find1={card_number}'
r = requests.get(base_url, headers=headers)
soup = BeautifulSoup(r.text,'html.parser')
effect = soup.find('span',{'class': 'timing'}).find_parent('div')
card_img = soup.find("span",{"class":"cards"}).find("img",{"class":"cards"}).get('data-src')
card_img_link = f"https://rugiacreation.com/ua/{card_img}"
effect_txt = ""
for node in effect.children:
    if node.name == 'img':
        img_src = urljoin(base_url, node['src'])
        # 你可以根據檔名判斷用什麼符號取代
        for i in icon.keys():
            if i in node['src']:
                effect_txt += icon["ico_circle_yellow"]  # 或用 :yellow_circle: 之類的表情碼
            else:
                effect_txt += "[圖]"
    elif hasattr(node, 'string') and node.string:
        effect_txt += node.string.strip() + " "
    elif isinstance(node, str):
        effect_txt += node.strip()
print(card_img_link)
print(effect_txt)

