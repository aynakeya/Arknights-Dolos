# Arknights-Dolos

## 免责申明

### 本软件仅供个人学习测试使用，请在下载后24小时内删除，不得用于商业用途，否则后果自负。

### 使用本软件对自己以及相关公司造成的所有损失和法律责任一律与本人无关，一切后果自负。

### 禁止使用者对其进行以任何方式的发行，传播，宣传。上述行为对自己以及相关公司造成的所有损失和法律责任一律与本人无关，一切后果自负。

---


## 简介

Arknights-Dolos/明日方舟中间人攻击框架 

使用 mitmproxy来捕获明日方舟的数据，借此来修改指定数据。

灵感来源：

[GhostStar/Arknights-Armada](https://github.com/GhostStar/Arknights-Armada)

[Tao0Lu/Arknights-Cheater](https://github.com/Tao0Lu/Arknights-Cheater)

[破解未成年时间限制](https://www.bilibili.com/read/cv7795601)

## 原理

直接获取明日方舟的数据是获取不到的，因为明日方舟使用了本地服务器进行转发

利用mitmproxy可以转发

破解本地服务器转发的方法来自 [GhostStar/Arknights-Armada](https://github.com/GhostStar/Arknights-Armada)

## 使用说明

1. clone本repository

2. 安装mitmproxy, `pip3 install mitmproxy`

2. 手机/模拟器上设置代理服务器

3. 在手机、模拟器中信任mitmproxy证书

4. 启动main,要启动网页还是命令行可以自己改代码

5. 重新进入游戏，开始

ps: 对如何配置mitmproxy有疑问的建议参照 [Tao0Lu/Arknights-Cheater](https://github.com/Tao0Lu/Arknights-Cheater)

## 数据更新说明

从[ArknightsGameData/tree/master/zh_CN/gamedata/excel](https://github.com/Kengxxiao/ArknightsGameData)中

下载

[character_table.json](https://github.com/Kengxxiao/ArknightsGameData/blob/master/zh_CN/gamedata/excel/character_table.json)

[skin_table.json](https://github.com/Kengxxiao/ArknightsGameData/blob/master/zh_CN/gamedata/excel/skin_table.json)


放入 /data 文件夹内

运行 `python dataProcess.py`


