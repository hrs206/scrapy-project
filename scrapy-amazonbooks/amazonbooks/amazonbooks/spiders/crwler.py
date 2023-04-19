import scrapy

class Amazonbooks(scrapy.Spider):
    name="amazonbooks"
    start_urls=["https://www.amazon.in/s?k=books&crid=3FMK1XO4EHDXS&sprefix=books%2Caps%2C330&ref=nb_sb_noss_1"]

    def parse(self, response):
        for product in response.css("div.sg-col-20-of-24.s-result-item.s-asin.sg-col-0-of-12.sg-col-16-of-20.sg-col.s-widget-spacing-small.sg-col-12-of-16"):
            yield {
                "title": product.css("span.a-size-medium.a-color-base.a-text-normal::text").get(),
                "rating": product.css("span.a-icon-alt::text").get(),
                "price(INR)": product.css("span.a-price-whole::text").get()
            }
        
        next_page = response.css("a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator").attrib["href"]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)