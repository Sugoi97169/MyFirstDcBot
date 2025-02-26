from bs4 import BeautifulSoup
import requests


def get_tier_dict(ua_num):
    response = requests.get("https://torecards.com/unionarenatier/")
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("figure", {'class': 'tier_list'})
    rows = table.find_all('tr')
    tier_str_title = []
    tier_str_img = []
    deck_list = []
    tier_str = ""
    tier_deck = \
        {
            0: None,  # T1
            1: None,  # T1.5
            2: None,  # T2
            3: None,  # T2.5
            4: None,  # T3
            5: None,  # T4
            6: None,  # T5
        }
    tier_deck_1 = \
        {
            0: [],  # T1
            1: [],  # T1.5
            2: [],  # T2
            3: [],  # T2.5
            4: [],  # T3
            5: [],  # T4
            6: [],  # T5
        }
    for row in rows:
        cols = row.find_all('td')
        if cols != []:
            deck_list.append(cols)
    for i in range(0, 7):
        tier_deck[i] = deck_list[i]
    for i in tier_deck:
        for img in tier_deck[i]:
            tier_deck[i] = img.find_all('img')
        for img in tier_deck[i]:
            tier_deck_1[i].append(img.get("alt"))
            tier_deck_1[i].append(img.get("src"))
    for i in range(0,len(tier_deck_1[ua_num])):
        if i==0:
            tier_str_title.append(tier_deck_1[ua_num][i])
        else:
            if i%2!=0:
                tier_str_img.append(tier_deck_1[ua_num][i])
            else:
                tier_str_title.append(tier_deck_1[ua_num][i])


    for i in range(0,len(tier_str_title)):
        tier_str+=f"{tier_str_title[i]}\n{tier_str_img[i]}\n------\n"
    return tier_str







