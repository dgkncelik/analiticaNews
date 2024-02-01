import requests
import xml.etree.ElementTree as ET
import sqlite3
import datetime
import elasticsearch

sql_connection = sqlite3.connect("scrape_database.db")
elastic_client = elasticsearch.Elasticsearch(
    "http://54.85.90.67:9200",  # Elasticsearch endpoint
)

rss_feed_list = [
    "https://www.trthaber.com/manset_articles.rss",
    "https://www.trthaber.com/sondakika_articles.rss",
    "https://www.haberturk.com/rss/spor.xml"
]


def create_table(db_connection_object):
    db_connection_object.execute('''CREATE TABLE HABERLER
             (ID             INTEGER PRIMARY KEY AUTOINCREMENT,
             TITLE           TEXT    NOT NULL,
             DATE            TEXT    NOT NULL,
             LINK            TEXT    NOT NULL,
             SUMMARY         TEXT,
             AUTHOR          TEXT);''')


def create_index(es_client_object):
    es_client_object.indices.create(index="haberler")


def insert_document(es_client_object, nd):
    es_client_object.index(
        index="haberler",
        document=nd
    )


def insert_row(db_connection_object, nd):
    insert_string = ("INSERT INTO HABERLER (TITLE,DATE,LINK,SUMMARY,AUTHOR) VALUES ('%s', '%s', '%s', '%s', '%s')" %
                     (nd["title"].replace("'", " "),
                      nd["date"],
                      nd["link"],
                      nd["summary"].replace("'", " "),
                      nd["author"]))
    db_connection_object.execute(insert_string)
    db_connection_object.commit()
    print("[+] Saved to database")


def rss_loop(rss_url_list):
    i = 0
    for rss_url in rss_url_list:
        print("[+] Scraping start for: %s %d" % (rss_url, i))
        response = requests.get(rss_url)
        if response.status_code == 200:
            content_short = response.content[:200]
            print("[+] Content %s" % content_short)
            parsed_content = parse_rss_content(response.content)
            for pc in parsed_content:
                insert_row(sql_connection, pc)
                insert_document(elastic_client, pc)
            # write_file_to_csv(parsed_content)
            print(parsed_content)
            print("[+] Scraping Completed")
        else:
            print("[!] Scraping error, status code %d" % response.status_code)
        i = i + 1


def parse_rss_content(rss_content_input):
    parsed_rss_content = ET.fromstring(rss_content_input)

    # create empty list for news items
    all_news = []

    # iterate news items
    for item in parsed_rss_content.findall('./channel/item'):
        news_object = {
            "title": "",
            "date": "",
            "summary": "",
            "link": "",
            "author": ""
        }
        if item.find("./title") is not None:
            news_object["title"] = item.find('./title').text

        if item.find('./pubDate') is not None:
            date_string = item.find('./pubDate').text
            if "GMT" in date_string:
                date_string = date_string.replace("GMT", "+0000")
            datetime_object = datetime.datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')
            iso8601_str = datetime_object.isoformat()
            news_object["date"] = iso8601_str

        if item.find('./description') is not None:
            news_object["summary"] = item.find('./description').text

        if item.find('./link') is not None:
            news_object["link"] = item.find('./link').text

        if item.find("./author") is not None:
            news_object["author"] = item.find("./author").text

        all_news.append(news_object)
        print("Parsing completed for RSS source")

    return all_news


def write_file_to_csv(news_item_object):
    myFile = open("haberler.txt", "a")
    for nio in news_item_object:
        myFile.write("%s \n" % nio)


# Start here!
if __name__ == '__main__':
    try:
        create_table(sql_connection)
    except sqlite3.OperationalError as e:
        if "already exists" in str(e):
            print("Table already exists, skipping creation")

    try:
        create_index(elastic_client)
    except elasticsearch.exceptions.BadRequestError as e2:
        if "already exists" in str(e2):
            print("Index already exists, skipping creation")

    rss_loop(rss_feed_list)
