from bs4 import BeautifulSoup
import requests
import math
import pandas as pd
import re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
           "Connection": "close", "Upgrade-Insecure-Requests": "1"}
site_reviews = "https://www.amazon.com/Apple-iPhone-Fully-Unlocked-256GB/product-reviews/B07754X4XV/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

def get_number_of_reviews(soup):
    # Example: 47,216 global ratings | 2,541 global reviews

    header_reviews_div = soup.find('div', {'data-hook': 'cr-filter-info-review-rating-count'})
    header_reviews_text = header_reviews_div.span.text.strip()
    header_list = header_reviews_text.split(" ")
    print(int(header_list[4].replace(",", "")))
    return int(header_list[4].replace(",", ""))


def get_number_of_total_pages(total_reviews, reviews_per_page):
    return math.ceil(total_reviews / reviews_per_page)


def get_soup(url, headers):
    r = requests.get(url, headers=headers)
    content = r.content
    if r.status_code == 200:
        soup = BeautifulSoup(content, "html.parser")
    else:
        soup = get_soup(url, headers)
    return soup




def get_product_reviews(base_url, headers, reviews_per_page):
    soup = get_soup(base_url, headers)
    reviewNumber = get_number_of_reviews(soup)
    pagesNumber = get_number_of_total_pages(reviewNumber, reviews_per_page)

    formattedReviews = []
    for i in range(pagesNumber):
        page_url = base_url + "&pageNumber=" + str(i + 1)
        soup = get_soup(page_url, headers)
        reviews = soup.findAll('div', {'data-hook': "review"})
        for item in reviews:
            formattedReview = {
                "review Text": item.find('span', {'data-hook': "review-body"}).find('span').text.strip(),
                "review Grade": int(float(item.find('i', {'data-hook': re.compile(r"review-star-rating|cmps-review-star-rating")}).text.split(" ")[0]))
            }
            print(formattedReview)
            formattedReviews.append(formattedReview)
    return formattedReviews



def export_reviews_to_csv(formattedReviews, file_name):
    df = pd.DataFrame(formattedReviews)
    df.to_csv(file_name)


if __name__ == "__main__":
    product_reviews = get_product_reviews(site_reviews, headers, 10)
    export_reviews_to_csv(product_reviews, "amazon_reviews.csv")


