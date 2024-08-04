import scrapy
from ..items import UnsplashImageItem

        
class UnsplashSpider(scrapy.Spider):
    name = 'unsplash'
    allowed_domains = ['unsplash.com']
    start_urls = ['https://unsplash.com/']

    def parse(self, response):
        for category in response.xpath('//*[@class="wuIW2 R6ToQ"]/@href').extract():
            yield scrapy.Request(response.urljoin(category), callback=self.parse_category)
        


    def parse_category(self, response):
        category = response.url.split('/')[-1]
        urls = response.xpath('//*[@class="wdUrX"]/img[2]/@src').extract()
        names = []
        i = 1
        for name in response.xpath('//*[@class="wdUrX"]/img[2]'):
            if name.xpath('.//@alt'):
                names.append(name.xpath('.//@alt').extract_first())
            else:
                names.append(f'No Name {i}')
                i += 1
        for i in range(len(response.xpath('//*[@class="wdUrX"]/img[2]').extract())):
            yield UnsplashImageItem(category=category, name=names[i], url=urls[i])
            yield scrapy.Request(urls[i], callback=self.write_file, meta={'name': names[i]})

    def write_file(self, response):
        name = response.meta['name']
        with open('images/' + name + '.jpg', 'wb') as f:
            f.write(response.body)