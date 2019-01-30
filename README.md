# Extractdede
Extractdede es una herramienta de extracción de links de las distintas series de Megadede.

## Configuración

Abrimos el archivo de configuración "configuration.conf" y modificamos cada dato de la siguiente manera:

    [SERIE]
    URL = HOME.SERIE.URL.VALUE 
    [SESSION]
    COOKIE_CFDUID = cfduid.VALUE 
    COOKIE_CAKEPHP_SESSION = cakephp_session.VALUE 
    COOKIE_CF_USE_OB = cf_use_ob.VALUE 
    COOKIE_MEGADEDE-SESS = megadede-sess.VALUE 
    COOKIE_PHPSESSID = PHPSESSID.VALUE 
    COOKIE_POPSHOWN2 = popshown2.VALUE 
    COOKIE_XSRF-TOKEN = xsrf-token.VALUE 

Ejemplo del archivo configuration.conf:

    [SERIE]
    URL = https://www.megadede.com/serie-1 
    [SESSION]
    COOKIE_CFDUID = jfdoefmof5412fkspef
    COOKIE_CAKEPHP_SESSION = eeefefxgdthbcghnchbn 
    COOKIE_CF_USE_OB = 0 
    COOKIE_MEGADEDE-SESS = mbvmgnyfjfhrsjjf5hrd3sfgsghrdhb 
    COOKIE_PHPSESSID = vxdvbrxhbtdbrdbdr
    COOKIE_POPSHOWN2 = 1
    COOKIE_XSRF-TOKEN = segsevbg4hrsnrdhrghdrhrdhbr

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
