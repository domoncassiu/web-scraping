import threading
import time
import re
import urllib.parse

import certifi
import datetime
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from snownlp import SnowNLP


class touTiao:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.password = urllib.parse.quote_plus('huaxin12345')
        self.uri = f"mongodb+srv://stevenwyl:{self.password}@cluster0.ihlnkdr.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(self.uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
        # self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client.db
        self.videos = self.db.videos
        self.comments = self.db.comments
        self.api_key = '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'
        self.curr_time = datetime.datetime.now()
        self.parse_time = datetime.datetime.strptime(
            f"{self.curr_time.year}-{self.curr_time.month}-{self.curr_time.day}T00:00:00.000Z",
            "%Y-%m-%dT%H:%M:%S.000Z")

    def launchBrowser(self):
        count = 0
        log = []

        self.browser.get(
            'https://www.toutiao.com/article/7222603053587792421/?channel'
            '=&source=search_tab')
        time.sleep(5)

        # append all the bloggers into the list with their homepage url
        element = self.browser.find_elements(By.XPATH, "//strong/a")
        for item in element:
            # print(item.text)
            # print(item.get_attribute("href"))
            log.append([item.text, item.get_attribute("href")])

        element2 = self.browser.find_elements(By.XPATH, "//li/a")
        for item in element2:
            if "粉" and "万" and "赞" in item.text:
                # print(item.text)
                # print(item.get_attribute("href"))
                log.append([item.text, item.get_attribute("href")])

        # filter the number out of all the bloggers
        for people in log:
            count += 1
            number = re.findall(r'\d+\.\d+万|\d+万', people[0])
            # number2 = re.findall(r'\d+万', people[0])
            # selected = number1 if number1 else number2
            likes = number[:2]
            # calculate the weight
            people.append(likes[0][:-1])
            # print(people)
            # print(f"获赞：{likes[0]} 粉丝: {likes[1]}")

        # sort the list according to the weight
        rank = sorted(log, key=lambda x: float(x[2]), reverse=True)
        for item in rank:
            print(item)
        return rank

    def homePage(self, link):
        self.browser.get(link)
        time.sleep(3)
        total = 0
        videoList = []
        curr_time = self.browser.find_elements(By.CLASS_NAME,
                                               "feed-card-footer-time-cmp")
        for item in curr_time:
            # filter the video uploaded today
            if item.text[-3:] == "小时前" or item.text[-3:] == "分钟前":
                try:
                    p = item.find_element(By.XPATH, "../../../../a")
                    videoList.append(p.get_attribute("href"))
                    total += 1
                    print(p.get_attribute("href"))
                    print(p.text)
                except NoSuchElementException:
                    pass

                try:
                    p = item.find_element(By.XPATH, "../../../a")
                    videoList.append(p.get_attribute("href"))
                    total += 1
                    print(p.get_attribute("href"))
                    print(p.text)
                except NoSuchElementException:
                    pass

        return total, videoList

    def videoList(self, video):
        all = []
        browser = webdriver.Chrome()
        browser.get(video)

        # wait until page loads
        WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "like-count"))
        )
        likes_count = browser.find_element(By.CLASS_NAME, "like-count").text
        comments_count = browser.find_element(By.CLASS_NAME,
                                              "comment-count").text
        favours_count = browser.find_element(By.CLASS_NAME, "favour-count").text
        # print(f"likes:{likes_count.text}  comments:{comments_count.text}  favourites:{favours_count.text}")

        # find the titile of the video
        title = browser.find_element(By.XPATH,
                                     '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/h1').text[
                3:]

        # insert the basic information in to the table
        info = {
            'title': title,
            'likes_count': int(likes_count),
            'comments_count': int(comments_count),
            'favours_count': int(favours_count),
            'date': self.parse_time
        }
        self.videos.insert_one(info)

        # click on the comment button to reach comment page
        button = browser.find_element(By.CSS_SELECTOR,
                                      ".video-action-button.comment")
        button.click()

        # wait until comments loaded
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, f'/html/body/div[3]/div/div['
                           f'2]/div[1]/ul/li['
                           f'1]/div/div/div[1]/div['
                           f'2]/div/div/span'))
        )

        time.sleep(2)

        # click on the load more button
        button = browser.find_element(By.CLASS_NAME, "load-more-btn")
        button.click()
        time.sleep(2)

        # select all the comments
        comments = browser.find_elements(By.CLASS_NAME, "comment-info")
        for i in range(1, len(comments) + 1):
            try:
                up = browser.find_element(By.XPATH,
                                          f'/html/body/div[3]/div/div[2]/div[1]/ul/li[{i}]/div/div/div[1]/div[2]/div/div/span').text
                text = browser.find_element(By.XPATH,
                                            f'/html/body/div[3]/div/div[2]/div[1]/ul/li[{i}]/div/div/div[2]/p').text

                # filter out the case when comment is empty or no likes
                if text != "" and up != "赞":
                    all.append([text, up])
                    # insert the data in db
                    curr = {
                        'title': title,
                        'comment': text,
                        'likes': int(up),
                        'date': self.parse_time,
                        'rating': SnowNLP(text).sentiments * 100
                    }
                    self.comments.insert_one(curr)
                print(f"likes: {up} \ncomment: {text}")
            except NoSuchElementException:
                pass


if __name__ == '__main__':
    tt = touTiao()
    rank = tt.launchBrowser()
    videoCount = 0
    # tt.homePage(rank[0][1])
    for people in rank:
        # if people[0] == "来自股市的猩猩1403.7万获赞69.3万粉丝":
        print("\n⬇️" + people[0] + "⬇️\n")
        currCount, video = tt.homePage(people[1])
        videoCount += currCount

        # perform video list operation
        # utilize multiple threading
        thread_list = []
        for curr in video:
            if "video" in curr:
                appium_server = threading.Thread(target=tt.videoList,
                                                 args=(curr,))
                thread_list.append(appium_server)
        for j in thread_list:
            j.start()
        time.sleep(15)

    print(f"\nThe total number of video updated today is {videoCount}")
