![wordanki](./logo.png)

# wordanki

构建自己的生词本，并转换成 anki 卡片!

## setup

```shell
pip3 install tinydb genanki
cd db
touch words.json # 新建生词本数据库
python3 main.py -h
```

输出如下信息代表依赖安装成功，数据库创建成功

```
Usage: python3 main.py [opt] <arg>
	Options:
		-h print this help
		-a <word> required, add a word to list
		-g generate word deck using current list
		-r <filepath> required, read text file and write them to listdb
```

字典默认为： CET4，CET6，考研，专业 8 级， 约 20000 词

你也可以生成自己的字典：

字典资源来自 [kajweb/dict](https://github.com/kajweb/dict)，将 <code>db.py</code> 中的 <code>filenames</code> 改成对应的 json 文件即可

然后

```shell
python3 db.py
```

> 注：生成时间极长


## usage

```shell
python3 main.py -a wicked # 将单词 wicked 加入生词本
```

```shell
python3 main.py -r words.txt # 将 words.txt 文件中的所有单词加入生词本，txt 文件格式为 一行一个单词
```

```shell
python3 main.py -g # 使用生词本中的单词生成 anki deck
```

## shout out

字典资源来自 [kajweb/dict](https://github.com/kajweb/dict)
