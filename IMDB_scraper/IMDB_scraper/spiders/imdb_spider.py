import scrapy

class ImdbSpider(scrapy.Spider):

    name = 'imdb_spider'    
    start_urls = ['https://www.imdb.com/title/tt0460649/']

    def parse(self, response):

        cast_url = str('https://www.imdb.com/title/tt0460649/') + str("fullcredits")
        yield scrapy.Request(url = cast_url, callback = self.parse_full_credits)

    def parse_full_credits(self, response):

        actor_pages = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        for i in range(len(actor_pages)):
            actor_page = 'https://www.imdb.com' + str(actor_pages[i])
            yield scrapy.Request(url = actor_page, callback = self.parse_actor_page)

    def parse_actor_page(self, response):

        actor_name = response.css("h1.header").css("span.itemprop::text").get()
        show = response.css("div.article")
        name = show.css("div.filmo-row")
        prof = name.css("::attr(id)").get()
        if prof[:4] == 'acto':
            no = show.css("div#filmo-head-actor.head::text").getall()
        if prof[:4] == 'actr':
            no = show.css("div#filmo-head-actress.head::text").getall()
        num = no[-1][2:4]
        for i in range(int(num)):
            movie_or_TV_name = name[i].css("a::text").get()
            yield {"Actor" : actor_name, "Movie/TV Name" : movie_or_TV_name}