import requests
from bs4 import BeautifulSoup

def get_listings(query: str):
    if query == "":
        return
    # Fügt die Query in den Ebay-Kleinanzeigen URL ein. / Inserts the query into the Ebay-Kleinanzeigen URL.
    # URL = "https://www.ebay-kleinanzeigen.de/stadt/stuttgart/" + query + "/k0l9280"
    URL = "https://www.ebay-kleinanzeigen.de/s-zu-verschenken/stuttgart/" + \
        query + "/k0c192l9280"

    # Setzt die Headers der Anfrage (Den User-Agent), damit Ebay-Kleinanzeigen die Anfrage nicht blockt. / Sets the headers of the request (the User-Agent) so that Ebay-Kleinanzeigen does not block the request.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
    }

    # Gibt den HTML text der Website in eine Variable wieder. / Puts the HTML text of the website into a variable again.
    response = requests.get(url=URL, headers=headers)

    # Setzt den Content der Website in eine Variable. / Sets the content of the website into a variable.
    page = response.content

    # Erstellt eine BeautifulSoup-Instanz mit dem Website-Content und einem passendem Parser. / Creates a BeautifulSoup instance with the website content and a suitable parser.
    soup = BeautifulSoup(page, "html.parser")
    # Setzt die Search-Results-Content in eine Variable. / Sets the search results content into a variable.
    srchRsltsContent = soup.find("div", id="srchrslt-content")

    # Setzt die Einträge inheralb der Seach-Results und dem Table dortdrinn in eine Variable / Array. / Sets the entries within the search results and the table therein into a variable/array.
    srchRslts = soup.find_all("li")

    # Setzt einen Counter. / Sets a counter.
    counter = 0

    # Setzt einen zweiten Counter. / Sets a second counter for 'VB' listings.
    vbCounter = 0
    ePreise = []

    count = 0
    url_list = []
    baseURL = 'https://www.ebay-kleinanzeigen.de'
    result = soup.find_all('ul', {'id': 'srchrslt-adtable'})
    for ul in result:
        li_elements = ul.find_all('li', {'class': 'ad-listitem lazyload-item'})
        # print(li_elements)
        for li in li_elements:
            link = li.find('a')
            if link:
                href = link.get('href')

                if href and '/s-anzeige/' in href:
                    url_list.append(baseURL + href)
                    # print(href)
                    count = count + 1
    return url_list