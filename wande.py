import datetime
import math
import time

import certifi
import pyautogui
import pymongo
from cnocr import CnOcr
import mss
import mss.tools
import pyperclip
import os

from pymongo.server_api import ServerApi

# ret = w.start()
# print(ret)
#
# ret = w.isconnected()
# print(ret)
#
# # test WSD function
# ret = w.wsd("000001.SZ", "sec_name", "2022-05-08", "2022-06-08", "")
# print(ret)


# capture selected portion of the screen
def autogui(num, title):
    # im = pyautogui.screenshot(region=(282, 800, 1252, 604))
    # im.save("demo.png")
    with mss.mss() as sct:
        # The screen part to capture
        region = {'top': 290, 'left': 280, 'width': 1252, 'height': 604}
        # Grab the data
        img = sct.grab(region)
        # Save to the picture file
        mss.tools.to_png(img.rgb, img.size,
                         output=f'wande_images\curr_{num}.png')


# ocr
def ocr(path):
    curr_ocr = CnOcr()
    title_total = []

    time1 = time.time()
    res = curr_ocr.ocr(path)
    flag = 0
    curr_total = []
    for each in res:
        if flag == 0 and \
                (len(each['text']) == 5 or len(each['text']) == 10) and \
                (each['text'][2] == '-' or
                 each['text'][2] == ':' or
                 each['text'][4] == '-'):
            flag = 1
            if each['text'][2] == ':':
                curr_time = datetime.datetime.now()
                parse_time = datetime.datetime.strptime(
                    f"{curr_time.year}-{curr_time.month}-{curr_time.day}T00:00:00.000Z",
                    "%Y-%m-%dT%H:%M:%S.000Z")
                curr_total.append(parse_time)
            elif each['text'][2] == '-':
                curr_month, curr_day = each['text'].split("-")[0], \
                    each['text'].split("-")[1]
                try:
                    parse_time = datetime.datetime.strptime(
                        f"{datetime.datetime.now().year}-{curr_month}-{curr_day}T00:00:00.000Z",
                        "%Y-%m-%dT%H:%M:%S.000Z")
                    curr_total.append(parse_time)
                except:
                    print("ocr issue")
                    curr_total.append("error")
            else:
                curr_year, curr_month, curr_day = each['text'].split("-")[0], \
                    each['text'].split("-")[1], \
                    each['text'].split("-")[2]
                try:
                    parse_time = datetime.datetime.strptime(
                        f"{curr_year}-{curr_month}-{curr_day}T00:00:00.000Z",
                        "%Y-%m-%dT%H:%M:%S.000Z")
                    curr_total.append(parse_time)
                except:
                    print("ocr issue")
                    curr_total.append("error")
        if flag == 1 and len(each['text']) > 10:
            flag = 0
            # print(each['text'])
            curr_total.append(each['text'])
        if len(curr_total) == 2:
            print(curr_total)
            title_total.append(curr_total)
            curr_total = []
    time2 = time.time()
    print('本次图片识别总共耗时%s s' % (time2 - time1))

    return title_total


def run(titles):
    # search = ["长江证券情绪周报", "兴业证券期权水晶球预测日报", "中信建投市场情绪跟踪",
    #           "申万宏源证券量化择时周报", "光大证券金融工程市场跟踪", "海通证券周报",
    #           "中泰证券期权周报", "广发证券A股量化择时", "天风证券宏观点评"]


    # print("目前搜索词条如下:")
    # for i in range(len(titles)):
    #     print(f"{i + 1}. {titles[i]}")
    #
    # ask = input("\n是否添加新搜索词条(y/n)：")
    # if ask == "y":
    #     bool = True
    #     while bool:
    #         add = input("\n添加搜索词条：")
    #         confirm = input(f"确认添加该词条：{add}(y/n)")
    #         if confirm == "y":
    #             titles.append(add)
    #             print("添加成功")
    #         con = input("是否继续添加(y/n)")
    #         if con == "n":
    #             bool = False
    #
    #     print("目前搜索词条如下:")
    #     for i in range(len(titles)):
    #         print(f"{i + 1}. {titles[i]}")

    # create new dir for storing images
    dir = "wande_images"
    if not os.path.exists(dir):
        os.makedirs(dir)


    password = "huaxin12345"
    uri = f"mongodb+srv://stevenwyl:{password}@cluster0.ihlnkdr.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    db = client.db2
    paper = db.paper
    total_data = []

    for title in titles:
        print(title)

        # automation
        pyautogui.PAUSE = 1

        # move to search bar and search
        pyperclip.copy(title)
        pyautogui.moveTo(750, 150, duration=1)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(1)

        # identify curr number of pages
        with mss.mss() as sct:
            # The screen part to capture
            region = {'top': 900, 'left': 1705, 'width': 30, 'height': 18}
            img = sct.grab(region)
            mss.tools.to_png(img.rgb, img.size,
                             output=f'wande_images\curr_page.png')

        with mss.mss() as sct:
            # The screen part to capture
            region = {'top': 260, 'left': 390, 'width': 50, 'height': 20}
            img = sct.grab(region)
            mss.tools.to_png(img.rgb, img.size,
                             output=f'wande_images\curr_page2.png')

        # ocr to find number of pages
        curr_ocr = CnOcr()
        res1 = curr_ocr.ocr('wande_images\curr_page.png')
        res2 = curr_ocr.ocr('wande_images\curr_page2.png')
        try:
            number = res1[0]['text']
            result1 = int(number)
        except:
            result1 = 1

        try:
            number = res2[0]['text']
            pages = int(number)
            print(f"there are {pages} results")
            result2 = int(math.ceil(pages / 20))

        except:
            result2 = 1

        result = max(result1, result2)
        print(f"there are {result} pages")

        # start looping through pages
        pyautogui.moveTo(1755, 905, duration=1)

        for i in range(1, result + 1):
            autogui(i, title)
            pyautogui.click()
            time.sleep(1.5)

        # loop through all the screenshot
        for i in range(1, result + 1):
            print(f"image {i}")
            path = os.path.join(dir, f"curr_{i}.png")
            total_data.extend(ocr(path))

        for item in total_data:
            if item[0] != "error":
                curr = {
                    'time': item[0],
                    'title': item[1],
                }
                paper.insert_one(curr)


if __name__ == '__main__':
    title = []
    run(title)