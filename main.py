import requests
import xml.etree.ElementTree as ET

rss_feed_list = [
    "https://www.trthaber.com/manset_articles.rss",
    "https://www.trthaber.com/sondakika_articles.rss",
    "https://www.haberturk.com/rss/spor.xml"
]


def rss_loop(rss_url_list):
    i = 0
    for rss_url in rss_url_list:
        print("[+] Scraping start for: %s %d" % (rss_url, i))
        response = requests.get(rss_url)
        if response.status_code == 200:
            content_short = response.content[:200]
            print("[+] Content %s" % content_short)
            parsed_content = parse_rss_content(response.content)
            write_file_to_csv(parsed_content)
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
        news_object = {}
        if item.find("./title") is not None:
            news_object["title"] = item.find('./title').text

        if item.find('./pubDate') is not None:
            news_object["date"] = item.find('./pubDate').text

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
    myFile = open("haberler.csv", "a")
    for nio in news_item_object:
        myFile.write("%s \n" % nio)

# Start here!
if __name__ == '__main__':
    rss_loop(rss_feed_list)
