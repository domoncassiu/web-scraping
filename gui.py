import os
import sys
import signal
import threading
import time
import eel
from wande import run
from toutiao import touTiao
from weixin import WeiXin

# python -m eel gui.py web -p toutiao.py -p wande.py -p weixin.py --onefile --collect-all snownlp --collect-all cnocr


print("now starting..")
# 资源文件目录访问
def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 修改当前工作目录，使得资源文件可以被正确访问
cd = source_path('')
os.chdir(cd)

dirname = os.path.dirname(__file__)
eel.init(os.path.join(dirname, "web"))


def helper():
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


@eel.expose
def toutiao():
    tt = threading.Thread(target=helper)
    tt.start()


@eel.expose
def wande(title):
    wd = threading.Thread(target=run, args=(title,))
    wd.start()


@eel.expose
def weixin(title):
    weixin = WeiXin()
    weixin.articles(title, time_period=30)


@eel.expose
def pause():
    # force quit chrome
    # os.system("killall -9 'Google Chrome'")
    os.system('taskkill /im chromedriver.exe /F')
    os.system('taskkill /im chrome.exe /F')
    os.kill(os.getpid(), signal.SIGINT)


eel.start('index.html', size=(1000, 750))  # 启动页面
