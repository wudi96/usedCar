from tkinter import *
from scrapy.crawler import CrawlerProcess
from usedCarData.spiders.usedCar_spider import *
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import pandas as pd

spider = UsedCarSpider()
settings = get_project_settings()
process = CrawlerProcess(settings=settings)


def startSpider():
    # 获取文本框内容
    brandChoose = var.get()
    args = [spider, brandChoose]
    process.crawl(*args)
    process.start()


def endSpider():
    pass


def export_csv():
    client = MongoClient('localhost', 27017)
    db = client.car_data_test01
    collection = db.UsedCarDataItem
    data = collection.find()
    time_filter = filter(lambda car: car['time'] != '未上牌', data)
    runway_filter = filter(lambda car: car['runway'] != "百公里内", time_filter)
    data = list(runway_filter)
    with open("car_data.csv", "w", newline='') as csvfileWriter:
        writer = csv.writer(csvfileWriter)
        fieldList = [
            "name",
            "runway",
            "time",
            "city",
            "money",
            "brand"
        ]
        writer.writerow(fieldList)

        for car in data:
            recordValueLst = []
            recordValueLst.append(car['name'])
            recordValueLst.append(car['runway'].replace('万公里', ''))
            recordValueLst.append(car['time'].replace('年', ''))
            recordValueLst.append(car['city'])
            recordValueLst.append(car['money'].replace('万', ''))
            recordValueLst.append(car['brand'])
            writer.writerow(recordValueLst)
    client.close()


def price_image():
    data = pd.read_csv('car_data.csv')
    plt.rc('font', family='Microsoft YaHei')
    data['money'].plot(kind='hist', title='价格分布直方图')
    plt.savefig("price.png")
    plt.close('all')


def runway_image():
    data = pd.read_csv('car_data.csv')
    plt.rc('font', family='Microsoft YaHei')
    data['runway'].plot(kind='hist', title='里程分布直方图')
    plt.savefig("runway.png")
    plt.close('all')


def time_image():
    data = pd.read_csv('car_data.csv')
    plt.rc('font', family='Microsoft YaHei')
    data['time'].value_counts()[::-1].plot(kind='barh', title='时间分布柱状图')
    plt.savefig("time.png")
    plt.close('all')


root = Tk()
root.title("usedCar")

brand_list = ['江铃', '北汽威旺', '北汽制造', '东南', '特斯拉', '凯迪拉克', 'WEY', '巴博斯', '东风小康', '金杯', '哈弗', '名爵', '吉利', 'Jeep', '金旅',
              '萨博', '斯柯达', '海马', '中兴', '迈凯伦', '永源', 'OX', '福特', 'MINI', '一汽', '奥迪', '腾势', '黄海', '东风风神', '玛莎拉蒂', '五菱',
              '长安欧尚', '迈巴赫', '理念', '华颂', '别克', '法拉利', '北京', '丰田', '菲亚特', '瑞麒', '陆风', '东风风度''阿尔法·罗密欧', '克莱斯勒', '驭胜',
              '本田', '卡尔森', '华凯', '领克', '欧朗', '九龙', '长安', '摩根', '恒天', '金龙', '汉腾', '布加迪', '云度', '福田', '华泰', '红旗', '宾利',
              '阿斯顿·马丁', '哈飞', '北汽昌河', '凯翼', '五十铃', '劳斯莱斯', '广汽新能源', '标致', '长安跨越', '雷诺', '广汽吉奥', '日产', '雷克萨斯', '华普',
              '长城', '庆铃', '现代', '路虎', '北汽幻速', '铃木', '林肯', 'GMC', '野马', '福汽启腾', '大众', '宝骏', '讴歌', '山姆', '启辰', '卡威', '猎豹',
              '众泰', '捷豹', '荣威', '上汽大通', '广汽传祺', '悍马', '兰博基尼', '中华', '马自达', 'SWM斯威', '力帆', '双星驰', '东风风光', '汇众']
brand_str = ""
for str in brand_list:
    brand_str = brand_str + ' ' + str
    if brand_list.index(str) % 5 == 0 and brand_list.index(str) > 0:
        brand_str = brand_str + '\n'

# Label
Label(root, text='输入汽车品牌：').grid(column=1, row=1, columnspan=1)
# 关键字输入框
var = StringVar()
e = Entry(root, textvariable=var).grid(column=2, row=1, columnspan=1)
# 确认按钮
Button(root, text="开始查询", command=startSpider).grid(column=1, row=2, columnspan=2)
# 文本框
Label(root, text=brand_str, width=40, height=22).grid(column=1, row=3, columnspan=2)
# 图片按钮
Button(root, text="导出csv文件", command=export_csv).grid(column=1, row=4, columnspan=2)
Button(root, text="价格分布直方图", command=price_image).grid(column=1, row=5, columnspan=2)
Button(root, text="里程分布直方图", command=runway_image).grid(column=1, row=6, columnspan=2)
Button(root, text="车龄分布直方图", command=time_image).grid(column=1, row=7, columnspan=2)
# 进入消息循环
root.mainloop()
