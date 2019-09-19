import requests
from bs4 import BeautifulSoup
from ebooklib import epub
from tempfile import mkstemp, gettempdir
import urllib.request
import shutil
import time

site = 'https://ranobes.com'
lang = 'ru'


def get_html(url):
    '''
    Получение html кода страницы по url
    :param url: url страницы html-код которой надо получить
    :return: html-code's page
    '''
    r = requests.get(url)
    return r.text


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    filledLength = int(length * iteration // total)
    bar = '{}{}'.format(fill * filledLength, '-' * (length - filledLength))
    print('\r{} |{}| {} из {} {}'.format(prefix, bar, iteration, total, suffix), end='\r')
    if iteration == total:
        print()


def getRanobesInfo(html):
    info = {}
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find('div', id='dle-content')
    desc = content.find('div', {'class': 'text', 'itemprop': 'description'})
    title = content.find('h1', class_='title').next_element
    info['title'] = title
    poster_url = desc.find('a').get('href')
    info['poster_url'] = poster_url
    author = desc.find('div', {'class': 'b', 'itemprop': 'author'}).find('a').text
    info['author'] = author
    info['first_chapter'] = '{}{}'.format(site, desc.find('a', class_='btn').get('href'))
    for b in desc.find_all('div', class_='b'):
        if b.next_element == 'Год издания: ':
            info['year'] = b.find('a').text
        if b.next_element == 'Количество глав: ':
            info['chapters_org'] = b.find('a').text
    genre = list()
    for a in desc.find('div', class_='tag_list').find_all('a'):
        genre.append(a.text)
    info['genre'] = genre
    return info


def downloadCover(url):
    fd, tmpFile = mkstemp(prefix='ranobes_', dir=gettempdir())
    with urllib.request.urlopen(url) as response, open(tmpFile, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return tmpFile


def generateChapter(html, num, lng='ru', ):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1', {'class': 'title', 'itemprop': 'headline'}).next_element
    text = soup.find('div', {'class': 'text', 'id': 'arrticle'})
    [div.extract() for div in text.find_all('div')]
    [s.extract() for s in text('script')]
    next_chapter = soup.find('a', {'class': 'btn', 'id': 'next'})
    # print(text)
    chapter = epub.EpubHtml(title=title, file_name='{}.html'.format(num), lang=lng)
    chapter.set_content('<html><head></head><body>{}</body></html>'.format(text))
    if next_chapter:
        return chapter, next_chapter.get('href')
    else:
        return chapter, None

def main():
    link = 'https://ranobes.com/ranobe/39855-the-book-eating-magician.html'

    info = getRanobesInfo(get_html(link))
    start_link = info['first_chapter']
    book = epub.EpubBook()
    cover = downloadCover(info['poster_url'])
    book.set_cover("image.jpg", open(cover, 'rb').read())
    book.set_identifier('sample123456')
    book.set_title(info['title'])
    book.set_language(lang)
    book.add_author(info['author'])
    num_chapter = 1
    lstChapter = ['nav']
    navMap = list()
    while start_link:
        html = get_html(start_link)
        chapter, start_link = generateChapter(html, num_chapter, lng=lang)
        book.add_item(chapter)
        lstChapter.append(chapter)
        navMap.append(epub.Link('{}.html'.format(num_chapter), chapter.title, 'intro'))
        num_chapter += 1
        print('\rgenerate chapter {} is done!'.format(num_chapter), end='\r')

    print()
    book.toc = navMap
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = lstChapter
    epub.write_epub('/tmp/{}.epub'.format(info['title']), book, {})
    # items = list(range(0, 507))
    # l = len(items)
    # print('Обработано глав:')
    # for i, item in enumerate(items):
    #     time.sleep(0.1)
    #     printProgressBar(i + 1, l, prefix='', suffix='завершено', length=50)


if __name__ == '__main__':
    main()
