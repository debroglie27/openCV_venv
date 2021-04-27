from bs4 import BeautifulSoup
from selenium import webdriver
import csv

# driver = webdriver.Firefox(executable_path=r'C:\Users\M K DE\AppData\Local\salabs_\WebDriverManager\gecko\v0.29.0\geckodriver-v0.29.0-win64\geckodriver.exe')
# driver = webdriver.Chrome(executable_path=r'C:\Users\M K DE\AppData\Local\salabs_\WebDriverManager\chrome\88.0.4324.96\chromedriver_win32\chromedriver.exe')

driver = webdriver.Firefox()

url_structure = 'https://www.amazon.com/s?k={}&page={}&ref=sr_pg_{}'
records = []
search_key = 'ultrawide monitor'
filename = search_key.replace(' ', '_') + '_results.csv'


def get_url(search_item, page_num):
    search_item = search_item.replace(' ', '+')
    return url_structure.format(search_item, page_num, page_num)


for page in range(1, 21):
    url = get_url(search_key, page)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    results = soup.find_all('div', class_="a-section a-spacing-medium")

    for result in results:
        product_name = result.find('h2', class_="a-size-mini a-spacing-none a-color-base s-line-clamp-2").span.text
        product_url = "https://www.amazon.com" + result.find('h2', class_="a-size-mini a-spacing-none a-color-base s-line-clamp-2").a['href']
        try:
            price = result.find('span', class_="a-offscreen").text
        except Exception:
            price = "Not Available"
        try:
            rating = result.find('span', class_="a-icon-alt").text
        except Exception:
            rating = "Not Available"
        try:
            review_count = result.find('span', class_="a-size-base").text
        except Exception:
            review_count = "Not Available"

        print(f"\nProduct Name: {product_name}")
        print(f"Product URL: {product_url}")
        print(f"Price: {price}")
        print(f"Rating: {rating}")
        print(f"Review Count: {review_count}")

        record = (product_name, price, rating, review_count, product_url)
        records.append(record)

driver.close()

with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Product Name', 'Price', 'Rating', 'Review Count', 'Url'])
    writer.writerows(records)
