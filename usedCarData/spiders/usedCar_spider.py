import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from usedCarData.items import *


class UsedCarSpider(scrapy.Spider):
    name = "usedCar"

    host = "http://www.taoche.com"

    def __init__(self, brandChoose=None, *args, **kwargs):
        super(UsedCarSpider, self).__init__(*args, **kwargs)
        self.brandChoose = brandChoose

    def start_requests(self):
        url_brand = "http://www.taoche.com/all/"
        yield Request(url=url_brand, callback=self.parse_brand)  # 车牌

    def parse_brand(self, response):
        self.log('A response from %s just arrived!' % response.url)
        brands = {}
        sel = Selector(response)
        brand_first_words = sel.css('.ul_C')
        for brand_first_word in brand_first_words:
            brand_same_words = brand_first_word.css('li')
            for brand_same_word in brand_same_words:
                brand = brand_same_word.css('a::text').extract()[0]
                brand_url = brand_same_word.xpath('a').xpath('@href').extract()[0]
                brands[brand] = brand_url
        # brands = {"阿斯顿·马丁": "/astonmartin/"}
        # for key, value in brands.items():
        key = self.brandChoose
        value = brands[key]
        url_cars_pages = "http://www.taoche.com" + value
        yield Request(url=url_cars_pages, meta={"brand": key, "brand_url": value}, callback=self.parse_pages)  # 车牌

    def parse_pages(self, response):
        self.log('A response from %s just arrived!' % response.url)
        brand = response.meta["brand"]
        brand_url = response.meta["brand_url"]
        sel = Selector(response)
        if 'the-pages' in response.body.decode('utf-8'):
            last_page = sel.css('.the-pages a:nth-last-of-type(2)::text').extract()[0]
        else:
            last_page = 1
        for i in range(1, int(last_page) + 1):
            url_cars_same_brand = "http://www.taoche.com" + brand_url + "?page=%d#pagetag" % i
            yield Request(url=url_cars_same_brand, meta={"brand": brand}, callback=self.parse_cars)

    def parse_cars(self, response):
        self.log('A response from %s just arrived!' % response.url)
        brand = response.meta["brand"]
        items = []
        sel = Selector(response)
        cars = sel.css('.gongge_main')
        for car in cars:
            item = UsedCarDataItem()
            name = car.css('a span::text').extract()[0]
            time = car.css('p i:nth-child(1)::text').extract()[0]
            runway = car.css('p i:nth-child(2)::text').extract()[0]
            city = car.css('.city_i a::text').extract()[0]
            price = car.css('.price i:nth-child(1)::text').extract()[0]
            item['name'] = name
            item['runway'] = runway
            item['time'] = time
            item['city'] = city
            item['money'] = price
            item['brand'] = brand
            items.append(item)
        return items
