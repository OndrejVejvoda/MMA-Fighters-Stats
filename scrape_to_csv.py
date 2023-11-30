import pandas as pd
from bs4 import BeautifulSoup
import requests
import string
import os


def fetch_html(char):
    url = f"http://www.ufcstats.com/statistics/fighters?char={char}&page=all"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def parse_hyperlinks(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='b-statistics__table')
    rows = table.find_all('tr')[1:]
    return [row.find("a").get("href") for row in rows if row.find("a") is not None]


def get_hyperlinks(chars):
    hyperlinks = []
    for char in chars:
        html_content = fetch_html(char)
        if html_content:
            links = parse_hyperlinks(html_content)
            hyperlinks.extend(links)
    return hyperlinks


def fetch_fighter_page(url):
    response = requests.get(url)
    return response.text if response.status_code == 200 else None


def parse_basic_info(soup):
    try:
        title_highlight_text = soup.find(class_="b-content__title-highlight").get_text(strip=True).split()
        first_name = title_highlight_text[0] if len(title_highlight_text) > 0 else "-"
        last_name = title_highlight_text[1] if len(title_highlight_text) > 1 else "-"
        nickname = soup.find("p", class_="b-content__Nickname").get_text(strip=True)
        record_text = soup.find(class_="b-content__title-record").get_text(strip=True).split()[1]
        wins, losses, draws = record_text.split("-")
        return [first_name, last_name, nickname, wins, losses, draws]
    except AttributeError:
        return None


def parse_statistics(soup):
    try:
        return [i_tag.get_text(strip=True).split(":")[1] for i_tag in soup.find_all("li", class_="b-list__box-list-item") if ":" in i_tag.get_text()]
    except Exception:
        return None


def get_fighters_stats(url):
    html_content = fetch_fighter_page(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        basic_info = parse_basic_info(soup)
        statistics = parse_statistics(soup)
        if basic_info and statistics:
            return basic_info + statistics
        else:
            return None
    else:
        return None


def scrape_data():
    column_names = ["first_name", "last_name", "nickname", "wins", "loses", "draws", "height", "weight", "reach", "stance" ,"born", "slpm", "str_acc", "sapm","str_def","td_avg","td_acc","td_def","sub_avg"]
    chars = list(string.ascii_lowercase)
    urls = get_hyperlinks(chars)
    fighters = []  
    for url in urls:
        fighters.append(get_fighters_stats(url))
    df = pd.DataFrame(fighters,columns=column_names)
    return df
