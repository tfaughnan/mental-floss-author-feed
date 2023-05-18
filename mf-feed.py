#!/usr/bin/env python3

import datetime
import json
import logging
import sys

import bs4
import feedgen.feed
import requests

def main() -> int:
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    if len(sys.argv) != 2:
        logging.error(f'Usage: {sys.argv[0]} IMDB_RATINGS_URL')
        return 1
    author_slug = sys.argv[1]
    author_url = f'https://www.mentalfloss.com/authors/{author_slug}'
    try:
        r = requests.get(author_url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return 1

    soup = bs4.BeautifulSoup(r.text, 'lxml')
    author = soup.find('title').text.strip()

    fg = feedgen.feed.FeedGenerator()
    fg.id(author_url)
    fg.title(f'{author} - Mental Floss')
    fg.author(name=author)
    fg.link(href=author_url, rel='alternate')
    fg.language('en')

    react_data_shit_tag = soup.find('script', {'type': 'application/ld+json'})
    react_data_shit = json.loads(react_data_shit_tag.text)
    for article in react_data_shit['itemListElement']:
        try:
            article_date = datetime.datetime.fromisoformat(article['datePublished'])
        except ValueError as e:
            logging.error(e)
            return 1

        fe = fg.add_entry()
        fe.id(article['url'])
        fe.title(article['headline'])
        fe.author(name=author)
        fe.published(article_date)
        fe.updated(article_date)
        fe.link(href=article['url'], rel='alternate')
        fe.content(f'<img src="{article["image"]}">')

    atomfeed = fg.atom_str(pretty=True)
    print(atomfeed.decode())
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
