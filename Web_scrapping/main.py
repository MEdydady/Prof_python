import json
import requests
import pprint
from fake_headers import Headers
from bs4 import BeautifulSoup

HOST = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"


def get_headers():
    return Headers(browser="firefox", os="windows").generate()


def get_html():
    html = requests.get(HOST, headers=get_headers()).text
    return html


my_json_list = []


def parse_vacancy():
    bs = BeautifulSoup(get_html(), "lxml")
    article_list = bs.find_all(class_="vacancy-serp-item__layout")
    for i in article_list:
        vacancies = i.find("a", class_="serp-item__title")
        link = vacancies["href"]
        response_links = requests.get(
            link,
            headers=get_headers(),
        ).text
        bs2 = BeautifulSoup(response_links, "lxml")
        work_text = bs2.find(
            "div",
            {"data-qa": "vacancy-description"},
        )
        for i2 in work_text:
            if ("Flask" or "Django") in i2.text:
                company_name = i.find("a", class_="bloko-link bloko-link_kind-tertiary")
                city = i.find(
                    "div",
                    attrs={
                        "data-qa": "vacancy-serp__vacancy-address",
                        "class": "bloko-text",
                    },
                )
                salary = i.find(
                    "span",
                    attrs={
                        "data-qa": "vacancy-serp__vacancy-compensation",
                        "class": "bloko-header-section-3",
                    },
                )
                if salary:
                    salary = salary.text
                else:
                    salary = "Зарплата не указана"
                my_json_list.append(
                    {
                        "Название компании": company_name.text.split(".")[0],
                        "Название вакансии": vacancies.text,
                        "Ссылка на вакансию": link,
                        "Город": city.text,
                        "Вилка заработной платы": salary,
                    }
                )
    return my_json_list
    # print(my_json_list)


def write_json(json_list):
    with open("Web_scrapping/vacancy.json", "w", encoding="utf-8") as f:
        json.dump(json_list, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    run = parse_vacancy()
    write_json(run)
