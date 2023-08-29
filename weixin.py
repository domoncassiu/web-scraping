import datetime
import time

import certifi
from appium import webdriver
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WeiXin:
    def __init__(self):
        self.caps = {"platformName": "Android",
                     "platformVersion": "13",
                     "deviceName": "RedmiK50G",
                     "unicodeKeyboard": True,
                     "resetKeyboard": True,
                     "automationName": "uiautomator2"
                     }
        # "appPackage": "com.tencent.mm",
        # "appActivity": "com.tencent.mm.ui.LauncherUI"
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub",
                                       self.caps)
        self.wait = WebDriverWait(self.driver, 300)
        self.size = self.driver.get_window_size()
        self.uri = f"mongodb+srv://stevenwyl:huaxin12345@cluster0.ihlnkdr.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(self.uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
        self.collection = self.client.db3.articles

    # grab all the articles with given titles
    # have to make sure the account given is already following
    def articles(self, search_title, time_period):
        for item in search_title:
            # search button
            button = self.wait.until(EC.presence_of_element_located(
                (By.ID, 'com.tencent.mm:id/f15')))
            button.click()

            # enter text and search
            search = self.wait.until(EC.presence_of_element_located(
                (By.ID, 'com.tencent.mm:id/cd7')))
            search.send_keys(item)
            self.driver.press_keycode(66)

            # enter detail page
            name = self.wait.until(EC.presence_of_element_located(
                (By.ID, 'com.tencent.mm:id/kpm')))
            name.click()

            # enter the article page
            icon = self.wait.until(
                EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/eo')))
            icon.click()

            first = True
            period = True
            while True:
                # scroll the block to the top of the page
                # location of the date
                el1 = self.wait.until(EC.presence_of_element_located(
                    (By.ID, 'com.tencent.mm:id/ijh')))
                if first:
                    # location of the top
                    el2 = self.wait.until(EC.presence_of_element_located(
                        (By.ID, 'com.tencent.mm:id/njv')))
                    first = False
                    self.driver.scroll(el1, el2)
                else:
                    # location of the date
                    el2 = self.wait.until(EC.presence_of_element_located(
                        (By.ID, 'com.tencent.mm:id/iks')))
                    location = el2.location['y']
                    # scroll the date to the top of the page
                    self.driver.swipe(200, location, 200, 320, duration=1500)

                time.sleep(1)
                # find the date and parse the date
                date = self.driver.find_element(By.ID,
                                                "com.tencent.mm:id/iks").text
                parse = self.parse_date(date)
                print(parse)

                # if datetime.datetime.now() - datetime.timedelta(days=time_period) < parse:
                #     period = False

                block = self.driver.find_element(By.ID, "com.tencent.mm:id/ikt")

                # check if there is more article button
                try:
                    self.driver.find_element(By.ID,
                                             "com.tencent.mm:id/lyt").click()
                except:
                    print("no more articles")

                # enter the article page and store the article context
                time.sleep(0.5)
                count = len(block.find_elements(By.ID, "com.tencent.mm:id/cs"))
                for i in range(count):
                    block = self.driver.find_element(By.ID,
                                                     "com.tencent.mm:id/ikt")
                    curr = block.find_elements(By.ID, "com.tencent.mm:id/cs")[i]
                    text = curr.text
                    curr.click()
                    self.store_articles(text, parse)
                    self.driver.press_keycode(4)

                # after reading the curr block, swipe down and move to the next
                # block to continue reading
                self.driver.swipe(self.size['width'] * 0.5,
                                  self.size['height'] * 0.7,
                                  self.size['width'] * 0.5,
                                  self.size['height'] * 0.5,
                                  duration=500
                                  )
            # time.sleep(5)
            # for i in range(3):
            #     self.driver.press_keycode(4)

    # store the article link and text into database
    def store_articles(self, text, date):
        # WeChat article is using webview which prevents appium from finding the
        # sharing and copy link button, so coordinate of the button is used here
        time.sleep(1)

        # click on the three dot icon
        self.driver.tap([(1008, 154)])
        # button = self.wait.until(
        #     EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/eo')))
        # button.click()

        # click on the copy link button
        time.sleep(1)
        self.driver.tap([(460, 1970)])
        # button = self.wait.until(
        #     EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/f15')))
        # button.click()

        # get article link
        curr_link = self.driver.get_clipboard_text()
        print(f"{text} {curr_link}")
        article = {
            'title': text,
            'link': curr_link,
            'date': date
        }
        self.collection.insert_one(article)

    # change the date into datetime format
    def parse_date(self, date):
        result = 0
        print(date)
        week_list = {"星期一": 1, "星期二": 2, "星期三": 3, "星期四": 4,
                     "星期五": 5, "星期六": 6, "星期日": 7}
        curr_time = datetime.datetime.now()
        curr_day = curr_time.isoweekday()
        # today and yesterday
        if date == "今天":
            result = curr_time
        elif date == "昨天":
            result = curr_time - datetime.timedelta(days=1)
        elif date in week_list:
            date = week_list[date]
            if date > curr_day:
                delta = curr_day + 7 - date
            elif date < curr_day:
                delta = curr_day - date
            else:
                delta = 7
            result = curr_time - datetime.timedelta(days=delta)
        else:
            month, day = date.split("月")[0], date.split("月")[1][:-1]
            parse_time = datetime.datetime.strptime(
                f"{curr_time.year}-{month}-{day}T00:00:00.000Z",
                "%Y-%m-%dT%H:%M:%S.000Z")
            return parse_time

        parse_time = result.strptime(
            f"{result.year}-{result.month}-{result.day}T00:00:00.000Z",
            "%Y-%m-%dT%H:%M:%S.000Z")
        return parse_time


if __name__ == "__main__":
    title = ["华鑫研究", "广发证券研究", "留富兵法", "中金量化及ESG"]
    weixin = WeiXin()
    weixin.articles(title, time_period=30)
