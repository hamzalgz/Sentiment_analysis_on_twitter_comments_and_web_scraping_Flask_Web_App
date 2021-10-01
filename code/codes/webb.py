import csv
import pandas as pd
from getpass import getpass
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from ast import literal_eval
from time import sleep
from builtins import str
import json
from bson import json_util

def scraping_tweet(card):
    usernam=card.find_element_by_xpath('.//span').text
    try:
        date=card.find_element_by_xpath('.//time').get_attribute('datetime')
        retweet_cnt = card.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[4]/div/div[1]/div/a/div/span').text
        quote_cnt = card.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[4]/div/div[2]/div/a').text
        like_cnt = card.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[4]/div/div[3]/div/a').text
        text =card.find_element_by_xpath('.//div[2]/div[2]/div[2]/div[1]').text
    except NoSuchElementException:
        return 0
    try:
        text =card.find_element_by_xpath('.//div[2]/div[2]/div[2]/div[1]').text
    except NoSuchElementException:
        return 'NaN'

    tweet=(usernam, date,like_cnt,retweet_cnt,quote_cnt,text  )
    return tweet

def web_scraping(url):
    driver=Chrome(r'D:\project twee\chromedriver_win32\chromedriver.exe')
    driver.get(url)
    comments = []
    tweet_ids = set()

    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True

    while scrolling:
        page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
        #nb = page_cards[0].find_element_by_xpath('.//div[@data-testid="retweet"]').text
        for card in page_cards:
            tweet = scraping_tweet(card)
            if tweet:
                tweet_id=''.join(tweet)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    comments.append(tweet)


        scroll_attempt = 0
        while True:
            # check scroll position
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(2)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                # end of scroll region
                if scroll_attempt >= 3:
                    scrolling = False
                    break
                else:
                    sleep(2) # attempt another scroll
            else:
                last_position = curr_position
                break

    return comments