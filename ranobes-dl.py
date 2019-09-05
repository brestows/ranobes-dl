import requests
from bs4 import BeautifulSoup
import time

site = 'https://ranobes.com'

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
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', id='dle-content')
    desc = content.find('div', {'class': 'text', 'itemprop': 'description'})
    title = content.find('h1', class_='title').next_element
    info['title'] = title
    poster_url = desc.find('a').get('href')
    info['poster_url'] = poster_url
    autor = desc.find('div', {'class': 'b', 'itemprop': 'author'}).find('a').text
    info['autor'] = autor
    info['first_chapter'] = '{}{}'.format(site,desc.find('a', class_='btn').get('href'))
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


def main():
    link = 'https://ranobes.com/ranobe/51243-main-character-hides-his-strength.html'
    info = getRanobesInfo(get_html(link))
    start_link = info['first_chapter']
    # while start_link:

    # items = list(range(0, 507))
    # l = len(items)
    # print('Обработано глав:')
    # for i, item in enumerate(items):
    #     time.sleep(0.1)
    #     printProgressBar(i + 1, l, prefix='', suffix='завершено', length=50)


if __name__ == '__main__':
    main()
