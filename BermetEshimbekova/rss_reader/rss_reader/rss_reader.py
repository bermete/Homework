import argparse
import requests
from bs4 import BeautifulSoup
import os
import sys
import warnings
import functools
import logging
import json
import urllib.request
import cloudscraper

__version__ = 1.0

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


def create_logger(level=10):
    """
    Creates a logging object and returns it
    """

    root = logging.getLogger()
    root.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root

    # logger = logging.getLogger("example_logger")
    # logger.setLevel(logging.INFO)
    # # create the logging file handler
    # fh = logging.FileHandler("test.log")
    # fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # formatter = logging.Formatter(fmt)
    # fh.setFormatter(formatter)
    # # add handler to logger object
    # logger.addHandler(fh)
    # return logger


def exception(function):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        # logger = create_logger()
        try:
            return function(*args, **kwargs)
        except AttributeError:
            pass
        except UnboundLocalError:
            pass
        except:
            # log the exception
            # err = "There was an exception in  "
            # err +=
            logger.exception(function.__name__)
            # re-raise the exception
            pass

    return wrapper



@exception
def get_content(url):
    """A function returns content by url"""

    cookies = dict(cookies_are='working')
    response = requests.get(url, cookies=cookies)
    if response.status_code == 403:
        ses = requests.Session()
        scraper = cloudscraper.create_scraper(browser='chrome')
        response = scraper.get(url)
    content = BeautifulSoup(response.content, 'lxml-xml')
    return content


@exception
def get_entries(content, limit=None):
    """Find items or entries in content"""

    entry_types = ['item', 'entry']
    entries = 0
    for entry in entry_types:
        entries = content.find_all(entry, limit=limit)
        if len(entries):
            break
    if len(entries) == 0:
        raise
    return entries


@exception
def get_item_text(tag, item):
    """Return value of tag"""

    text = item.find(tag).text
    if text:
        text = BeautifulSoup(text, 'html.parser').get_text().replace('\n', ' ').strip()
    return text


@exception
def get_item_attr_value(tag, attr, item):
    """Return value of attributes in tag"""

    text = ''
    all_text = item.find(tag)
    if all_text and (attr in all_text.attrs):
        text = all_text.attrs[attr]
    return text


@exception
def search_description(item):
    """Try to find description"""

    text = ''
    tags = ['description', 'media:description', 'summary', 'content']
    for tag in tags:
        text = get_item_text(tag, item)
        if text:
            break
    if text in [None, '']:
        soup = BeautifulSoup(requests.get(search_link(item)).content, 'html.parser')
        metas = soup.find_all('meta')
        for meta in metas:
            if 'name' in meta.attrs and meta.attrs['name'] == 'description':
                text = meta.attrs['content']
    return text


@exception
def search_pubdate(item):
    """Try to find pubdate"""

    tags = ['pubDate', 'published', 'updated']
    for tag in tags:
        text = get_item_text(tag, item)
        if text:
            return text


@exception
def search_link(item):
    """Try to find link"""

    tags = ['link', 'enclosure']
    attrs = ['href', 'url']
    for tag in tags:
        text = get_item_text(tag, item)
        if text:
            return text
        else:
            for attr in attrs:
                text = get_item_attr_value(tag, attr, item)
                if text:
                    return text


@exception
def search_image(item):
    """Try to find image"""

    text = ''
    tags = ['thumbnail', 'media:thumbnail', 'media:content', 'image', 'enclosure', 'fullimage']
    attrs = ['src', 'url', 'href', 'img']
    for tag in tags:
        text = get_item_text(tag, item)
        if text and "http" in text:
            return text
        else:
            for attr in attrs:
                text = get_item_attr_value(tag, attr, item)
                if text:
                    return text

    if text is None:
        for tag in item.find_all():
            # print(tag.text)
            # text = item.find(tag.name).text
            text1 = BeautifulSoup(tag.text, 'html.parser')
                # .text.replace('\n', ' ').strip()
            # print(text1)
            try:
                return text1.find('img')['src']
            except:
                continue

    if text in [None, '']:
        soup = BeautifulSoup(requests.get(search_link(item)).content, 'html.parser')
        links = soup.find_all('link')
        for link in links:
            # print(str(meta))
            if "image" in str(link):
                try:
                    if 'http' in link.attrs['href']:
                        text = link.attrs['href']
                        return text
                except:
                    if 'http' in link.attrs['content']:
                        text = link.attrs['content']
                        return text
                else:
                    continue

    if text in [None, '']:
        imgs = soup.body.find_all('img')
        for img in imgs:
            try:
                if 'http' in img.attrs['src']:
                    text = img.attrs['src']
                    return text
            except:
                continue


def search_tags_and_attrs(item):
    """Find all tags and attributes"""

    for tag in item.find_all():
        print(tag.name, '-', tag.text)
        for attr in tag.attrs:
            print('attr - ', attr, '-', tag.attrs[attr])
            # print([tag.name for tag in item.find_all()])


@exception
def get_rssfeed(url, limit=None, *args, **kwargs):
    """Search 'title', 'pubDate', 'description', 'link', 'image' in rss feed"""

    tags = ['title', 'pubDate', 'description', 'link', 'image']
    content = get_content(url)
    entries = get_entries(content, limit=limit)
    result = {}
    result['feed'] = ''
    try:
        result['feed'] = content.channel.title.text
    except:
        result['feed'] = content.feed.title.text
    item_number = 1
    for item in entries:
        result_item = {}
        for tag in tags:
            text = 'not found'
            if tag == 'pubDate':
                text = search_pubdate(item)
                if text == None:
                    # text = content.channel.lastBuildDate.text
                    text = get_item_text('lastBuildDate', content.channel)
            elif tag == 'description':
                text = search_description(item)
                # text = ' '.join(char for char in text if char.isalnum())
            elif tag == 'link':
                text = search_link(item)
            elif tag == 'image':
                text = search_image(item)
            else:
                text = get_item_text(tag, item)
            result_item[tag] = text
        result['item'+str(item_number)] = result_item
        item_number += 1
    return result


def print_result(result, format='text'):
    """Print result in json or text"""

    if type(result) is dict:
        if format == 'text':
            for k, v in result.items():
                if type(v) is dict:
                    for vv in v:
                        print(f'{vv}: {v[vv]}')
                else:
                    print(v)
        elif format == 'json':
            sys.stdout.encoding
            json_object = json.dumps(result, ensure_ascii=False, indent=4)
            print(json_object)


def all_urls():
    """Read all urls in the urls.txt"""

    with open('urls.txt', 'r') as f:
        urls = f.readlines()
    for url in urls:
        url = url.replace('\n', '')
        get_rssfeed(url, limit=1)

def rss_reader():
    """RSS reader"""

    parser = argparse.ArgumentParser(
        description='Python command-line RSS reader.')
    parser.add_argument(
        'source',
        help='RSS URL')
    parser.add_argument(
        '--version',
        action='version',
        version='Version {version}'.format(version=__version__),
        help='Print version info')
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Outputs verbose status messages'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Print result as JSON in stdout'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit news topics if this parameter provided')
    args = parser.parse_args()

    if args.verbose:
        # logging.basicConfig(level=logging.DEBUG)
        logger = create_logger(10)
    else:
        logger = create_logger(50)

    if args.json:
        format = 'json'
    else:
        format = 'text'

    print_result(get_rssfeed(url=args.source, limit=args.limit), format)



if __name__ == '__main__':
    try:
        rss_reader()
    except:
        exit(0)
