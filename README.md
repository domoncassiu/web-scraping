# Crawler Tool
This is the english version of the project introduction [English](https://github.com/domoncassiu/web-scraping/blob/main/README.md)

通过以下链接查看中文说明 [Chinese](https://github.com/domoncassiu/web-scraping/blob/main/README_CN.md)

## Project Introduction

This project is a crawler tool based on multiple open source automation testing tools. Its goal is to collect data on stock market trends from various social media platforms, quantify and summarize various indicators to predict short-term trends.

This project is mainly divided into three modules:

- Using the [selenium](https://github.com/SeleniumHQ/selenium) web automation tool to collect the daily video views and comments of well-known financial bloggers on Today's Headline, and use the trained [snownlp](https://github.com/isnowfy/snownlp) language model to calculate the emotional index of the day based on emotion indicators.
- Using [pyautogui](https://github.com/asweigart/pyautogui) and [cnocr](https://yiyan.baidu.com/) to batch collect and summarize research reports from wind database. It uses the pyautogui module to automatically search and the cnocr image recognition library to collect text content.
- Using the [appium](https://github.com/appium/appium) Android automation tool to click and collect article content from WeChat official account.

All collected data is stored in the MongoDB database for further processing and aggregation. The MongoDB chart function is used to process the data and combine it with stock market data for further comparison. The [python-eel](https://github.com/python-eel/Eel) front-end graphics interface library was used to integrate the above modules, allowing users to operate them through button clicks in the interface.

## Environment Configuration

You can directly run the executable file [automation_tool.exe](https://github.com/domoncassiu/web-scraping/releases/tag/v0.1.0-alpha) on Windows to view the tool's operation effect.

> [!NOTE]
> The executable file relies on the Chrome browser and appium environment for data capture, which needs further configuration.

If you need to configure the project environment locally, please refer to the following steps:

1. Install Google Chrome: [Download link](https://www.google.com/chrome/)

2. Install dependencies: `pip install -r requirements.txt`

3. Configure appium Android automation environment: Due to the complexity of the appium environment and its inability to be packaged, you can refer to [this article](https://blog.csdn.net/u010454117/article/details/122531278?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522169329147616800192279737%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=169329147616800192279737&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-122531278-null-null.142^v93^chatgptT3_2&utm_term=windows%20appium&spm=1018.2226.3001.4187) for configuration.

   - JDK 1.8
   - Android-SDK 34
   - Node.js: node-v18.16.0
   - Appium 2.0.0

4. Connect your Android device to the computer and turn on developer debugging mode: [How to enable developer mode](https://developer.android.com/studio/debug/dev-options)

After successful configuration, you should see the following results:

```bash
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

## Module Usage

This project is mainly divided into three modules: Toutiao Crawler, Wind Database Crawler, and WeChat Official Account Crawler. Below we will explain each module.

### Toutiao Module

Using the selenium automation tool, we crawl data on the Toutiao website from well-known financial bloggers. We crawl the video views, total likes, and all user comments and their likes for the updated articles on the same day. The integrated data is stored in a MongoDB database and presented in a chart.

![](https://github.com/domoncassiu/web-scraping/blob/main/examples/1.gif)

### Wind Database Module

Using automatic screenshot and pyautogui tools, we crawl research report data in the wind database, and use cnocr to automatically recognize the crawled data. We record all research report names and their publication dates. The integrated data is stored in a MongoDB database and presented in a chart.

![](https://github.com/domoncassiu/web-scraping/blob/main/examples/2.gif)

### WeChat Official Account Module

Using appium automation tools, we crawl WeChat public account articles on an Android phone. We crawl the updated articles and their links on the same day. The integrated data is stored in a MongoDB database and presented in a chart. [View Demo](https://github.com/domoncassiu/web-scraping/blob/main/examples/demo.mov)

### Front-end Interface

Using python-eel, we integrated the above tools into a GUI software that can be run by directly running gui.py.

![](https://github.com/domoncassiu/web-scraping/blob/main/examples/3.gif)

## Packaging Project

You can use pyinstaller to re-package the project. Execute the following code in the project directory:

```bash
python -m eel gui.py web -p toutiao.py -p wande.py -p weixin.py --onefile --collect-all snownlp --collect-all cnocr
```

The packaged executable file will be saved in the **dist** directory.

## Problem Handling

- If you encounter a Chrome driver version mismatch error, similar to the following error message:

  ```
  'unknown error: cannot connect to chrome at 127.0.0.1:98765 from session not created: This version of ChromeDriver only supports Chrome version 114 Current browser version is 116.0.5845.111"
  ```

  You need to update selenium to the latest version:

  ```bash
  pip install selenium —upgrade
  ```

- If you encounter a MongoDB timeout error, similar to the following error message:

  ```
  Timed out after 30000 ms while waiting for a server that matches com.mongodb.client.internal.MongoClientDelegate$1@b586e86. Client view of cluster state is {type=REPLICA_SET, servers={, type=UNKNOWN, state=CONNECTING}, {address=, type=UNKNOWN, state=CONNECTING}, {address=](), type=UNKNOWN, state=CONNECTING}]
  ```

  You need to check your network connection and turn off VPN.
