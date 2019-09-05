import requests
from bs4 import BeautifulSoup
import time


def get_html(url):
    '''
    Получение html кода страницы по url
    :param url: url страницы html-код которой надо получить
    :return: html-code's page
    '''
    r = requests.get(url)
    return r.text


# Print iterations progress
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
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = '{}{}'.format(fill * filledLength, '-' * (length - filledLength))
    print('\r{} |{}| {} из {} {}'.format(prefix, bar, iteration, total, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def main():
    link = 'https://ranobes.com/ranobe/51243-main-character-hides-his-strength.html'
    # A List of Items
    items = list(range(0, 507))
    l = len(items)
    print('main')

    # Initial call to print 0% progress
    # printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
    print('Обработано глав:')
    for i, item in enumerate(items):
        # Do stuff...
        time.sleep(0.1)
        # Update Progress Bar
        printProgressBar(i + 1, l, prefix='', suffix='завершено', length=50)


if __name__ == '__main__':
    main()
