Redirect to the english version [Readme.md](![](https://github.com/domoncassiu/web-scraping/blob/main/README_eng.md))

## 项目介绍

该项目是一个基于多个开源自动化测试工具的整合式爬虫工具，目标是收集用户在各类社交媒体上有关股市行情的数据，对各项指标进行量化汇总以预测短期的走势。
本项目主要分为三个模块：

- 利用了[selenium](https://github.com/SeleniumHQ/selenium)网络自动化工具收集今日头条知名财经博主每日的视频播放数量以及评论内容， 并通过训练过后的[snownlp](https://github.com/isnowfy/snownlp)语言模型进行情绪指标的判断并计算出当日的情绪指标。
- 利用了[pyautogui](https://github.com/asweigart/pyautogui)以及[cnocr]()对万得数据库研究报告进行了批量采集汇总， 通过驱动光标的方式进行自动搜索并使用cnocr图像识别来采集文字内容。
- 利用了[appium](https://github.com/appium/appium)安卓自动化工具对微信公众号得文章内容进行点击和采集。

以上采集到的所有数据都存入mongodb数据库进行进一步处理和汇总，通过mongodb的图表功能对数据进行处理并和股票大盘数据进行结合，来起到进一步对比的效果。
使用了[python-eel](https://github.com/python-eel/Eel)制作了前端图形界面，并对以上几个模块进行了整合，可以通过图形界面的按钮来进行操作。

## 环境配置

可在windows环境下直接运行可执行文件[automation_tool.exe](https://github.com/domoncassiu/web-scraping/releases/tag/v0.1.0-alpha)来查看工具运行效果
> [!NOTE]
> 可执行文件依赖chrome浏览器以及appium环境进行数据抓取，需要进一步配置。

如需在本地配置项目环境可参考如下步骤：

1. 安装谷歌浏览器: [下载链接](https://www.google.com/chrome/)
2. 安装依赖: ```pip install -r requirements.txt```
3. 配置appium安卓自动化环境: 由于appium环境较为复杂且无法进行打包，可参考[此文章](https://blog.csdn.net/u010454117/article/details/122531278?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522169329147616800192279737%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=169329147616800192279737&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-122531278-null-null.142^v93^chatgptT3_2&utm_term=windows%20appium&spm=1018.2226.3001.4187)进行配置。
   - JDK 1.8
   - Android-SDK 34
   - Node.js：node-v18.16.0
   - Appium 2.0.0
4. 将安卓手机连接电脑并打开开发者调试功能:[如何打开开发者模式](https://developer.android.com/studio/debug/dev-options)
     
配置成功后结果如下：
```
$ java -version
java version "14.0.2" 2020-07-14
Java(TM) SE Runtime Environment (build 14.0.2+12-46)
Java HotSpot(TM) 64-Bit Server VM (build 14.0.2+12-46, mixed mode, sharing)

$ adb version
Android Debug Bridge version 1.0.41
Version 34.0.3-10161052
Installed as /Users/domoncassiu/Library/Android/sdk/platform-tools/adb
Running on Darwin 22.3.0 (x86_64)

$ node -v
v18.16.0

$ npm -v
9.5.1

$ appium -v
2.0.0

$ adb devices
List of devices attached
3214c552	device
```

## 模块使用
该项目主要分为今日头条爬虫，万得数据库爬虫和微信公众号爬虫三个模块，以下会对各个模块进行说明。

### 今日头条模块
运用selenium自动化工具在今日头条网站上对知名财经博主进行数据抓取，每日抓取当日更新的文章的播放量，点赞总数，以及文章下的所有用户评论及其点赞数量。将整合后的数据存入mongodb数据库并以图表的方式进行呈现。

![](https://github.com/domoncassiu/web-scraping/blob/main/examples/1.gif)

### 万得数据库模块
运用自动截图和pyautogui工具在万得数据库中对研报数据进行抓取，并通过cnocr对抓取数据进行自动识别，记录所有研报的名称以及其发布日期。将整合后的数据存入mongodb数据库并以图表的方式进行呈现。

![](https://github.com/domoncassiu/web-scraping/blob/main/examples/2.gif)

### 微信公众号模块
运用appium自动化工具在安卓手机上对微信公共号文章进行抓取，每日抓取当日更新的文章以及文章链接。将整合后的数据存入mongodb数据库并以图表的方式进行呈现。[查看演示](https://github.com/domoncassiu/web-scraping/blob/main/examples/demo.mov)

### 前端界面
运用python-eel将以上工具整合成了gui软件，可以直接运行gui.py来运行程序。

![](https://github.com/domoncassiu/web-scraping/blob/main/examples/3.gif)



## 打包项目

可以使用pyinstaller对项目重新进行打包，在项目目录下执行以下代码

```bash
python -m eel gui.py web -p toutiao.py -p wande.py -p weixin.py --onefile --collect-all snownlp --collect-all cnocr
```

打包完成后可执行文件会保存在**dist**目录下




## 问题处理

- 如遇到chrome driver版本不匹配问题，类似代码报错

  ```
  'unknown error: cannot connect to chrome at 127.0.0.1:98765 from session not created: This version of ChromeDriver only supports Chrome version 114 Current browser version is 116.0.5845.111"
  ```

  需要更新selenium至最新版本

  ```bash
  pip install selenium —upgrade
  ```

- 如遇到mongodb超时问题，类似代码报错

  `````
  Timed out after 30000 ms while waiting for a server that matches com.mongodb.client.internal.MongoClientDelegate$1@b586e86. Client view of cluster state is {type=REPLICA_SET, servers={, type=UNKNOWN, state=CONNECTING}, {address=, type=UNKNOWN, state=CONNECTING}, {address=](), type=UNKNOWN, state=CONNECTING}]
  `````

  需要检查网络连接，关闭vpn连接
