import scrapy


class PopulationSpider(scrapy.Spider):
    name = "population"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"]

    def parse(self, response):
        rows = response.xpath("//tbody/tr")
        print(rows)
        for row in rows[2:]:
            yield {
                "location": row.xpath(".//td[1]//a/text()").get(),
                "population_2022": int(row.xpath(".//td[2]/text()").get().replace(',', '')),
                "population_2023": int(row.xpath(".//td[3]/text()").get().replace(',', '')),
                "change": round(float(row.xpath(".//td[4]/span[2]/text()").get().replace('+', '').replace('−', '-').replace('%', ''))/100, 4),
                "continent": row.xpath(".//td[5]/a/text()").get(),
                "subregion": row.xpath(".//td[6]/a/text()").get()
            }
                
