from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from datetime import datetime

from configuration import connect_todb


def scrapping():
    url = "https://pythonprogramming.net/parsememcparseface"
    response = requests.get(url=url, verify=False)
    # reading the web page
    content = BeautifulSoup(response.content, "html.parser")
    # parse the HTML
    introduction = content.find_all("p", {"class": "introduction"})[0].text
    nav = content.nav
    links = list()
    for link in nav.find_all('a'):
        links.append(link.get("href"))

    table = content.table
    list_records = list()
    # creating the data set
    for tr in table.find_all('tr'):
        td = tr.find_all('td')
        if len(td):
            row = {"Program Name": td[0].text, "Internet Points": td[1].text, "Kittens?": td[2].text}
            list_records.append(row)

    df = pd.DataFrame(list_records, columns=["Program Name", "Internet Points", "Kittens?"])
    # saving the data set to a csv file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.join(current_dir, "languages.csv")
    df.to_csv(file_name, index=False, encoding='utf-8')
    # reconstruction the data from a csv file
    data = pd.read_csv(file_name, encoding='utf-8')
    # save scrapping result to DB
    model = connect_todb()
    created_on = datetime.utcnow()
    new_data = dict(introduction=introduction, links=links, languages=list_records, date=created_on)
    model.insert_one(new_data)


if __name__ == "__main__":
    scrapping()
