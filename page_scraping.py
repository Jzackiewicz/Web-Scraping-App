import requests
from bs4 import BeautifulSoup


class Ogloszenie():
    def __init__(self, numer, organizator, nazwa, termin, adres, link):
        self.numer = numer
        self.organizator = organizator
        self.nazwa = nazwa
        self.termin = termin
        self.adres = adres
        self.link = link

    def __repr__(self):
        return f'Przetarg: {self.numer}, {self.organizator}, {self.nazwa}, {self.termin}, {self.adres}, {self.link}\n'

    def __iter__(self):
        self.__iterkeys = iter(vars(self).keys())
        return self

    def __next__(self):
        key = next(self.__iterkeys)
        return getattr(self, key)


def scrape_page(url):
    przetargi = []

    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    przetargi_raw = soup.find_all("table", class_="body-wrap")[2]
    przetargi_raw = przetargi_raw.find("tr")
    przetargi_raw = przetargi_raw.find("td")

    cells = przetargi_raw.find_all("tr")
    for cell in cells:
        lines = cell.find_all("td")

        if len(lines) >= 5 and lines[0].text.strip() != "Numer ogłoszenia" and lines[0].text.strip() is not None:
            nr = lines[0].text.strip()
            org = lines[1].text.strip()
            dan = lines[2].text.strip().replace("\n", "")
            ter = lines[3].text.strip()
            lok = lines[4].text.strip().replace("\n", "").strip()
            url = cell.find("a")['href']

            ogl = Ogloszenie(nr, org, dan, ter, lok, url)
            przetargi.append(ogl)

    return przetargi


if __name__ == '__main__':
    offers = scrape_page(
        'https://www.oferty-biznesowe.pl/powiadomienia/pokaz/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnQiOjI1ODU4OCwibm90aWZpY2F0aW9uIjozNzk1MjIsImtleSI6IjIwMjQtMDEtMzEtMS0xNy0xMCIsImV4cCI6MTcwOTMxMTYzMX0.CWarsdb5b-P8Fm4OHIlTUQw4pbIcwW7M2ZUuI8WWZk8')
    print(offers)
