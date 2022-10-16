from urllib.request import urlopen
from lxml import html
import requests

GREATEST_BOOKS_URL = "https://thegreatestbooks.org/?page="
OPEN_LIBRARY_URL = "https://openlibrary.org/isbn/"
NO_PAGES = 1
BOOKS = []


def main():
    global BOOKS
    for i in range(NO_PAGES):
        page_html = get_page(i + 1)
        tree = html.fromstring(page_html)
        amazon_links = tree.xpath("//a[contains(@href,'amazon')]/@href")
      
        for al in amazon_links:
            isbn = al[-10:]
            print(isbn)
            ol_page = requests.get(f"{OPEN_LIBRARY_URL}{isbn}")
            ol_tree = html.fromstring(ol_page.content)
            number_of_pages = ol_tree.xpath('//span[@class="edition-pages"]/text()')
            no_pages = 0       
            if number_of_pages is not None:
                no_pages = number_of_pages[0]
            book_name = ol_tree.xpath('//h1[@class="work-title"]/text()')
            BOOKS.append({"name": book_name[0], "page": no_pages})
    
    sorted_books = sorted(BOOKS, key=lambda i: i['page'], reverse=True)
    with open(r'results.txt', 'w') as fp:
        for _, i in enumerate(sorted_books):
            fp.write("%s\n" % i)


def get_page(page):
    page = urlopen(f"{GREATEST_BOOKS_URL}{page}")
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return html


if __name__ == "__main__":
    main()