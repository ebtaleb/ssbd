from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.settings import Settings
from twisted.internet import reactor

from scrapy.spiders import Spider
from scrapy.item import Item, Field
from selenium import webdriver

class ImItem(Item):
    image_urls = Field()
    images = Field()

class SSBDSpider(Spider):
    name = "scrapesixbilliondemons"
    allowed_domains = ["killsixbilliondemons.com"]
    start_urls = [
        "http://killsixbilliondemons.com/comic/kill-six-billion-demons-chapter-1/"
    ]

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://killsixbilliondemons.com/
        @scrapes name
        """

        driver = self.driver
        driver.get(response.url)
         
        comic_url = driver.find_element_by_css_selector('div#comic img').get_attribute("src")

        next_comic_url = driver.find_element_by_css_selector('td.comic_navi_right a.navi-next').get_attribute("href")
        last_comic_url = driver.find_element_by_css_selector('td.comic_navi_right a.navi-last').get_attribute("href")

        curr_comic_url = next_comic_url
        #items = []
        while (driver.current_url != last_comic_url):

            driver.get(curr_comic_url)
            comic_url = driver.find_element_by_css_selector('div#comic img').get_attribute("src")
            next_comic_url = driver.find_element_by_css_selector('td.comic_navi_right a.navi-next').get_attribute("href")

            item = ImItem()
            item['image_urls'] = [comic_url]

            yield item
            #items.append(item)
            curr_comic_url = next_comic_url
            #break
        #return items

# callback fired when the spider is closed
def callback(spider, reason):
    stats = spider.crawler.stats.get_stats()  # collect/log stats?

    # stop the reactor
    reactor.stop()


# instantiate settings and provide a custom configuration
settings = Settings()

#pipelines = { 'scrapy.pipelines.images.ImagesPipeline': 1 }
pipelines = { 'pipelines.MyImagesPipeline': 1 }

settings.set('ITEM_PIPELINES', pipelines, priority='cmdline')
settings.set('IMAGES_STORE', '/tmp', priority='cmdline')

# instantiate a spider
spider = SSBDSpider()

# instantiate a crawler passing in settings
crawler = Crawler(spider, settings)

# configure signals
crawler.signals.connect(callback, signal=signals.spider_closed)
crawler.crawl()

# start the reactor (blocks execution)
reactor.run()