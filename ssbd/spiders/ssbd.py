from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.item import Item, Field
from selenium import webdriver

class ImItem(Item):
    image_url = Field()

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
        #comic_url = response.css('div#comic img::attr("src")')[0].extract()

        next_comic_url = driver.find_element_by_css_selector('td.comic_navi_right a.navi-next').get_attribute("href")
        last_comic_url = driver.find_element_by_css_selector('td.comic_navi_right a.navi-last').get_attribute("href")
        #next_comic_url = response.css('td.comic_navi_right a::attr("href")')[0].extract()
        #last_comic_url = response.css('td.comic_navi_right a::attr("href")')[1].extract()
        curr_comic_url = next_comic_url
        #items = []
        while (driver.current_url != last_comic_url):

            driver.get(curr_comic_url)
            comic_url = driver.find_element_by_css_selector('div#comic img').get_attribute("src")
            next_comic_url = driver.find_element_by_css_selector('td.comic_navi_right a.navi-next').get_attribute("href")
            #yield Request(comix_url, callback=self.parse_comic)
            item = ImItem()
            item['image_url'] = comic_url

            yield item
            #items.append(item)
            curr_comic_url = next_comic_url

        #return items
            

    #def parse_comic(self, response):
        #item = ImItem()
        #item['image_url'] = str(comic_url)
        #return [item]
