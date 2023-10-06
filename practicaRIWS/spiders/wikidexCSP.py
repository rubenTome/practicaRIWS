from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class wikidexCSP(CrawlSpider):
    name = "wikidexx"
    allowed_domains = ["wikidex.net"]
    start_urls = ["https://www.wikidex.net/wiki/WikiDex"]
    rules = (Rule(LinkExtractor(allow = "/wiki/Lista_de_Pok%C3%A9mon"),  #/wiki/Lista_de_Pok%C3%A9mon
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

        nombre = response.css("div.titulo::text").get()

        generacion = response.css("table.datos.resalto td a::attr(title)").re_first(r"(.*generación.*)")
        generacion = generacion.replace(' generación', '')

        tipo = response.css("table.datos.resalto td a::attr(title)").re(r"(.*Tipo.*)")

        peso = response.css("table.datos.resalto td::text").re(r"(.*kg.*)")[0]

        altura = response.css("table.datos.resalto td::text").re(r"(.*\d m.*)")[0]

        sexos = response.css("table.datos.resalto td::text").re(r"(.*\%.*)")

        if(len(sexos) == 0):
            sexomacho = '0%'
            sexohembra = '0%'

        else:
            sexomacho = sexos[0]
            sexohembra = sexos[1]

        imagenpokemon = 'https://www.wikidex.net' + response.css("a::attr(href)").re_first(r"/wiki/Archivo:.+")

        yield {
            'Nombre': nombre,
            'Generación': generacion,
            'Tipo': tipo,
            'Peso': peso,
            'Altura': altura,
            'ProbMacho': sexomacho,
            'ProbHembra': sexohembra,
            'Imagen': imagenpokemon
        }