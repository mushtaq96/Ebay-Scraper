import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
from emailing.sender import send_email
from db.db import get_db_conn, get_links, insert_links, link_exists, create_links_table
import schedule
import time
import threading
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


query = ""

@app.on_event("startup")
async def startup():
    async with get_db_conn() as conn:
        await create_links_table(conn)


@app.get("/query")
async def get_query(q: str, conn=Depends(get_db_conn)):
    # code for checking ebay kleinanzeigen listings and sending email
    global query
    query = q
    listings = get_listings()
    for listing in listings:
        async with get_db_conn() as conn:
            if not await link_exists(conn, listing):
                await insert_links(conn, listing)
                print(f'New listing found: {listing}')
            else:
                #remove listing from list
                listings.remove(listing)
    if len(listings) > 0:
        sender = os.environ.get('SENDER_MAIL')
        password = os.environ.get('SENDER_PASSWORD')
        receiver = os.environ.get('RECEIVER_MAIL')
        subject = query + ' New Ebay Listing ACTION NEEDED!'
        body = 'New listing found. Please check the link or links below: \n' + \
            '\n'.join(listings)
        send_email(sender, password, receiver, subject, body)
    return {"message": f"Query received: {query}"}


def get_listings():
    global query
    if query == "":
        return
    # Fügt die Query in den Ebay-Kleinanzeigen URL ein. / Inserts the query into the Ebay-Kleinanzeigen URL.
    # URL = "https://www.ebay-kleinanzeigen.de/stadt/stuttgart/" + query + "/k0l9280"
    URL = "https://www.kleinanzeigen.de/s-stuttgart/" + \
        query + "/k0l9280"

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
        li_elements = ul.find_all('li', {'class': 'ad-listitem'})
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


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


# create a schedule to run every 2 minutes
schedule.every(2).minutes.do(get_listings)

# start the schedule in a separate thread
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()
