# Scrapy settings for dirbot project
BOT_NAME = 'ssbd'

SPIDER_MODULES = ['ssbd.spiders']
NEWSPIDER_MODULE = 'ssbd.spiders'

ITEM_PIPELINES = ['scrapy.pipelines.images.ImagesPipeline']
#ITEM_PIPELINES = {'dirbot.pipelines.MyImgPipeline': 1}
IMAGES_STORE = '/tmp'
