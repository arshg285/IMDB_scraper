import scrapy

class ImdbSpider(scrapy.Spider):

    name = 'imdb_spider'    
    start_urls = ['https://www.imdb.com/title/tt0460649/']

    def parse(self, response):

        """        
        This function navigates to the Cast and Crew section by starting on the IMDB page for the TV show.

        Parameters:
            self: This is referring to the class object itself that is being called when running this class method.

            response: This refers to the output/response received when we are making request to a URL. It will be used since we will be accessing elements of the webpage yielded by the URL.

        Does not return any data but calls the parse_full_credits function.
        """

        # Creating the URL to get to the Cast and Crews section
        cast_url = str('https://www.imdb.com/title/tt0460649/') + str("fullcredits")

        # Calling the parse_full_credits method
        yield scrapy.Request(url = cast_url, callback = self.parse_full_credits)

    def parse_full_credits(self, response):

        """        
        This function yields a request to go to the IMDB page of each actor and actress for the TV show that we're working with from the Cast and Crew section that it starts from.

        Parameters:
            self: This is referring to the class object itself that is being called when running this class method.

            response: This refers to the output/response received when we are making request to a URL. It will be used since we will be accessing elements of the webpage yielded by the URL.

        Does not return any data but calls the parse_actor_page function.
        """

        # Getting URLs for every actor/actress in the TV show
        actor_pages = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        # Calling the parse_actor_page method for every actor/actress
        for i in range(len(actor_pages)):
            actor_page = 'https://www.imdb.com' + str(actor_pages[i])
            yield scrapy.Request(url = actor_page, callback = self.parse_actor_page)

    def parse_actor_page(self, response):

        """        
        This function is called for each actor and actress in the TV show and fetches us the information we are interested in about them, primarily their name and the TV shows/movies that they've worked in.

        Parameters:
            self: This is referring to the class object itself that is being called when running this class method.

            response: This refers to the output/response received when we are making request to a URL. It will be used since we will be accessing elements of the webpage yielded by the URL.

        It yields a dictionary containing the name of the actor/actress and the title for the movie/TV show they've worked in for every movie/TV show they have starred in.
        """

        # Fetching the name of the actor/actress from their webpage using the appropriate CSS elements
        actor_name = response.css("h1.header").css("span.itemprop::text").get()
        
        # Getting the name of the movies/TV shows that they're worked in
        show = response.css("div.article")
        name = show.css("div.filmo-row")
        prof = name.css("::attr(id)").get()

        # Determining whether the person is an actor (male) or an actress (female)
        if prof[:4] == 'acto':
            no = show.css("div#filmo-head-actor.head::text").getall()
        if prof[:4] == 'actr':
            no = show.css("div#filmo-head-actress.head::text").getall()
        num = no[-1][2:4]

        # Yielding the dictionary for every movie/TV show that the actor/actress has starred in
        for i in range(int(num)):
            movie_or_TV_name = name[i].css("a::text").get()
            yield {"Actor" : actor_name, "Movie/TV Name" : movie_or_TV_name}