## 整合式网络爬虫自动化工具

### 项目介绍

该项目是一个基于多个开源自动化测试工具的整合式爬虫工具，目标是收集用户在各类社交媒体上有关股市行情的数据，对各项指标进行量化汇总以预测短期的走势。
本项目主要分为三个模块：

- 利用了[selenium](https://github.com/SeleniumHQ/selenium)网络自动化工具收集今日头条知名财经博主每日的视频播放数量以及评论内容， 并通过训练过后的[snownlp](https://github.com/isnowfy/snownlp)语言模型进行情绪指标的判断并计算出当日的情绪指标。
- 利用了[pyautogui](https://github.com/asweigart/pyautogui)以及[cnocr]()对万得数据库研究报告进行了批量采集汇总， 通过驱动光标的方式进行自动搜索并使用cnocr图像识别来采集文字内容。
- 利用了[appium](https://github.com/appium/appium)安卓自动化工具对微信公众号得文章内容进行点击和采集。

以上采集到的所有数据都存入mongodb数据库进行进一步处理和汇总，通过mongodb的图表功能对数据进行处理并和股票大盘数据进行结合，来起到进一步对比的效果。
使用了[python-eel](https://github.com/python-eel/Eel)制作了前端图形界面，并对以上几个模块进行了整合，可以通过图形界面的按钮来进行操作。

### 环境配置

可在windows环境下直接运行可执行文件[automation_tool.exe](https://github.com/domoncassiu/web-scraping/releases/tag/v0.1.0-alpha)来查看工具运行效果
> [!NOTE]
> 可执行文件依赖chrome浏览器以及appium环境进行数据抓取，需要进一步配置。


