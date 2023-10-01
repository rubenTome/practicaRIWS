from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class wikidexCSP(CrawlSpider):
    name = "wikidexx"
    allowed_domains = ["wikidex.net"]
    start_urls = ["https://www.wikidex.net/wiki/WikiDex"]
    rules = (Rule(LinkExtractor(allow = "/wiki/Lista_de_Pok%C3%A9mon"),  #generaci%C3%B3n
                  callback = "parse_item", 
                  follow = False),)

    custom_settings = {
        'COOKIES_ENABLE': False,
        'DOWNLOAD_DELAY': 2.5,
    }

    def parse_item(self, response):
        pokemons = response.css("table.tabpokemon td a::attr(href)").re(r"^(?!\/wiki\/Tipo)(?!#cite).*$")

        for pokemon in pokemons:
            urldestino = "https://www.wikidex.net" + pokemon
            print(urldestino)
            yield Request(urldestino, callback=self.parse_pokemon)


    def parse_pokemon(self, response):

        # REVISAR SI LOS STRINGS SON NONE, PORQUE HAY VARIOS QUE DA ERROR POR EL HABITAT
        # SOLO HA PILLADO 338 DE 1017 POKEMONS, LOS CUALES SON DE PRIMERA, SEGUNDA O TERCERA GEN. 
        # MIRAR PORQUE NO PILLA EL RESTO.
        # COMENTAR AL PROFE EL VIERNES SI HAY ALGUNA FORMA DE ACELERAR EL CRAWLING EVITANDO QUE BANEEN EL SPIDER. 

        nombre = response.css("div.titulo::text").get()

        generacion = response.css("table.datos.resalto td a::attr(title)").re_first(r"(.*generación.*)")
        generacion = generacion.replace(' generación', '')

        tipo = response.css("table.datos.resalto td a::attr(title)").re(r"(.*Tipo.*)")

        peso = response.css("table.datos.resalto td::text").re(r"(.*kg.*)")[0]

        altura = response.css("table.datos.resalto td::text").re(r"(.*\d m.*)")[0]

        habitat = response.css("table.datos.resalto td img::attr(alt)").re_first(r"(.*Hábitat.*)")
        habitat = habitat.replace('.gif', '') #removes file format from the string
        habitat = habitat.replace('Hábitat ', '')



        yield {
            'Nombre': nombre,
            'Generación': generacion,
            'Tipo': tipo,
            'Peso': peso,
            'Altura': altura,
            'Hábitat': habitat
        }

