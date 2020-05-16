from __future__ import print_function, unicode_literals
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_2
import webbrowser

data = {"techcrunch": {"posts": []}, "coronavirus": {"posts": []}}


def get_news_type(answers):
    switcher = {"Tech": ["Techcrunch", "Wired", "Suprise Me!"]}
    return switcher.get(answers["news_type"])


def getSoupData(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def buildTechcrunchJSON():
    site_data = {
        "site_name": "techcrunch",
        "URL": "https://techcrunch.com/",
        "posts_container": "river",
        "post_blocks": "post-block",
        "title": "post-block__title__link",
        "href": "post-block__title__link",
        "description": "post-block__content",
    }
    soup = getSoupData(site_data["URL"])
    container = soup.find(class_=site_data["posts_container"])
    post_blocks = container.find_all(class_=site_data["post_blocks"])

    for post_block in post_blocks:
        title = post_block.find(class_=site_data["title"]).text.strip()
        href = post_block.find("a", class_=site_data["href"])["href"]
        description = post_block.find(class_=site_data["description"]).text.strip()
        # blob = {"name": title}
        blob = {"name": title, "href": href, "description": description}
        data[site_data["site_name"]]["posts"].append(blob)


questions = [
    {
        "type": "list",
        "name": "news_type",
        "message": "What type of news would you like to view?",
        "choices": ["Tech", "World", "Local"],
    },
    {
        "type": "list",
        "name": "news_site",
        "message": "Which site would you like?",
        "choices": get_news_type,
    },
]

answers = prompt(questions, style=custom_style_2)
fetchData = {"Techcrunch": buildTechcrunchJSON()}
fetchData.get(answers["news_site"])

sites = [
    {
        "type": "checkbox",
        "qmark": "😃",
        "name": "selected_sites",
        "message": "Select articles",
        "choices": data["techcrunch"]["posts"],
    },
]

open_sites = prompt(sites, style=custom_style_2)
print(open_sites)

for post in data["techcrunch"]["posts"]:
    should_open = post["name"] in open_sites["selected_sites"]
    if should_open:
        webbrowser.open_new_tab(post["href"])

# print(data["techcrunch"]["posts"])
# json_data = json.dumps(open_sites, indent=4,)
# print(json_data)

# currentDate = datetime.today().strftime('%Y_%m_%d')

# data = {currentDate: {}}
# data[currentDate] = {"techcrunch" : { "posts": []}, "coronavirus": { "posts": []}}

# def getSoupData(URL):
#     page = requests.get(URL)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     return soup

# def buildTechcrunchJSON():
#     site_data = {"site_name": "techcrunch", "URL": "https://techcrunch.com/", "posts_container": "river", "post_blocks": "post-block", "title": "post-block__title__link", "href": "post-block__title__link", "description": "post-block__content"}
#     soup = getSoupData(site_data["URL"])
#     container = soup.find(class_=site_data["posts_container"])
#     post_blocks = container.find_all(class_=site_data["post_blocks"])
#     # postDate = datetime.today().strftime("%B %d, %Y")
#     for post_block in post_blocks:
#         # postedDate = post_block.find_all('time')[0].text.strip()
#         # if (postDate in postedDate):
#             title = post_block.find(class_=site_data["title"]).text.strip()
#             href = post_block.find('a', class_=site_data["href"])['href']
#             description = post_block.find(class_=site_data["description"]).text.strip()
#             blob = {"title": title, "href": href, "description": description}
#             data[currentDate][site_data["site_name"]]["posts"].append(blob)
#         # else:
#         #     break

# buildTechcrunchJSON()

# def coronavirusJSON():
#     site_data = {"site_name": "coronavirus", "URL": "https://www.foxnews.com/category/health/infectious-disease/coronavirus", "posts_container": "collection-article-list", "post_blocks": "article", "title": "title", "href": "", "description": "dek"}
#     URL = site_data["URL"]
#     page = requests.get(URL)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     container = soup.find(class_=site_data["posts_container"])
#     post_blocks = container.find_all(class_=site_data["post_blocks"])

#     for post_block in post_blocks:
#             title = post_block.find('h4', class_=site_data["title"])
#             href = post_block.find(class_=site_data["title"]).select('a')[0]['href']
#             description_el = post_block.find(class_=site_data["description"])
#             description =post_block.find(class_=site_data["description"]).select('a')[0].text.strip()
#             blob = {"title": title, "href": href, "description": description}
#             data[currentDate][site_data["site_name"]]["posts"].append(blob)

# coronavirusJSON()

#     # for post_block in post_blocks:
#     #     title = post_block.find(class_='post-block__title__link').text.strip()
#     #     href = post_block.find('a', class_='post-block__title__link')['href']
#     #     description = post_block.find(class_='post-block__content').text.strip()
#     #     blob = {"title": title, "href": href, "description": description}
#     #     data[currentDate]["techcrunch"]["posts"].append(blob)
#         # print(title)
#         # print(href)
#         # print(content)

# json_data = json.dumps(data, indent=4,)
# print(json_data)
