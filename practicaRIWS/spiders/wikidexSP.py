from pathlib import Path

import scrapy


class wikidexSP(scrapy.Spider):
    name = "pokemons"

    def start_requests(self):
        urls = [
            "https://www.wikidex.net/wiki/Lista_de_Pok%C3%A9mon"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"pokemons-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")