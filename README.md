# Extractdede
Extractdede es una herramienta de extracción de links de las distintas series de Megadede.

## Configuración

Abrimos el archivo de configuración "configuration.conf" y modificamos cada dato de la siguiente manera:

    [SERIE]
    URL = HOME.SERIE.URL.VALUE (Sin comillas)
    [SESSION]
    COOKIE_CFDUID = 'cfduid.VALUE' (Con comillas)
    COOKIE_CAKEPHP_SESSION = 'cakephp_session.VALUE' (Con comillas) 
    COOKIE_CF_USE_OB = 'cf_use_ob.VALUE' (Con comillas)
    COOKIE_MEGADEDE-SESS = 'megadede-sess.VALUE' (Con comillas)
    COOKIE_PHPSESSID = 'PHPSESSID.VALUE' (Con comillas)
    COOKIE_POPSHOWN2 = 'popshown2.VALUE' (Con comillas)
    COOKIE_XSRF-TOKEN = 'xsrf-token.VALUE' (Con comillas)

Si no tenemos instalado splash: 
    
    pip install scrapy-splash

O también:

    docker pull scrapinghub/splash

## Iniciando

Primero arrancamos scrapy-splash con docker por ejemplo

    docker run -p 8050:8050 scrapinghub/splash
    
Y por último, estando en el directorio raíz del proyecto, nos movemos hasta el directorio extractdede/extractdede/spiders de la siguiente manera:
    
    cd extractdede/extractdede/spiders

 ejecutamos:

    scrapy runspider main.py -o  enlaces.csv -t csv --nolog

Al finalizar el proceso se nos creará un archivo llamado 'enlaces.csv' que es el que contendrá los enlaces a cada capítulo. Podemos abrirlo con cualquier editor de texto en caso de no poder manejar un archivo csv.

## Extras

    Cabe destacar que en ningún momento se suprime el proceso de registro en Megadede ya que cada usuario debe usar sus Cookies para poder realizar la operación.

    Este programa está pensado para ayuda a la comunidad. No me hago responsable del mal uso de este programa.
