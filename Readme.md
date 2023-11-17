# Instrucciones de ejecución

Estando en el directorio raíz del proyecto, ejecutar:

### scrapy crawl wikidexx -O archivodesalida.json

## Sobre la fase de indexación en ElasticSearch

Una vez obtenida la salida en formato JSON, para incluir los datos en el cluster de ElasticSearch debemos:

    - Lanzar una petición de creación del índice, el cual debe llamarse pokemon.
    - Lanzar una petición para el mapeado de las properties. En el fichero mapeado_properties.txt se incluye el contenido necesario.
    - Realizar la inserción de los elementos. Esto se incluye en el fichero peticion_json.txt

Se asume que se tiene en ejecución un clúster de ElasticSearch con una versión 8.9 o superior.