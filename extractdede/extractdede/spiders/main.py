#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Cristian Romero Povea

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy
from scrapy_splash import SplashRequest
import requests
import configparser

#class bcolors:
RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

class MegaadedeItem(Item):
    capitulo = Field()
    url = Field()

class MegadedeSpider(CrawlSpider):
    name = "MegadedeCrawlSpider"

    #Archivo configuración:
    configuration = configparser.ConfigParser()
    configuration.read('configuration.conf')

    url_serie = configuration['SERIE']['URL']
    url_nombre = {}
    cookies_conf = configuration['SESSION']
    
    cookies={
        '__cfduid':cookies_conf['COOKIE_CFDUID'] ,
        'cakephp_session':cookies_conf['COOKIE_CAKEPHP_SESSION'],
        'cf_use_ob':cookies_conf['COOKIE_CF_USE_OB'],
        'megadede-sess':cookies_conf['COOKIE_MEGADEDE-SESS'],
        'PHPSESSID':cookies_conf['COOKIE_PHPSESSID'],
        'popshown2':cookies_conf['COOKIE_POPSHOWN2'],
        'XSRF-TOKEN':cookies_conf['COOKIE_XSRF-TOKEN']
    }

    rules = (
        Rule(LinkExtractor(allow=r'aportes'),callback='parse'),
    )

    '''
        Con esta función empezamos a hacer las peticiones a la web asignada
        Debemos pasarle las cookies necesarias para que acceda a la web.
        Por último, llamamos a la función de callback parse.
    '''
    def start_requests(self):
        self.logo()
        print 'Serie a analizar => [',self.url_serie,']'
        url_final = str(self.url_serie).strip() 
        yield SplashRequest(url_final,cookies=self.cookies, callback=self.parse)

    '''
        Esta función busca el link de aportes, lo general y se lo pasa al Splash.
        Por último llama a la función de callback parse_items_1
    '''
    def parse(self, response):
        for q in response.css(".show-close-footer::attr(data-href)"):
            url_aux = "https://www.megadede.com"+ q.extract()
            print 'Analizando url => [',url_aux,']'
            yield SplashRequest(url_aux,cookies=self.cookies, callback=self.parse_items_1)
    
    '''
        Esta función entra al link de aportes de cada uno de los capítulos y buscando el lenguaje y el servidor,
        si coincide con español y openload respectivamente, sigue adelante. 
        por último, llama a la función de callback parse_items_2
    '''
    def parse_items_1(self,response):
        ya_spanish = 0
        for q in response.xpath('//div[@id="online"]'):
            for i in q.css(".aporte"):
                aux_st_language = ''.join(str(x) for x in i.css(".language").extract())
                aux_st_server = ''.join(str(x) for x in i.css(".host img::attr(src)").extract())
                if ya_spanish < 1:
                    if "spanish" in aux_st_language and (not "sub" in aux_st_language or not "SUB" in aux_st_language) and "openload" in aux_st_server:   
                        url_ap = ''.join(str(x) for x in i.css("a::attr(href)").extract()).strip()
                        r = r = requests.get(response.url, cookies=self.cookies)
                        if r.status_code == 200:
                            ya_spanish = ya_spanish + 1 
                            yield SplashRequest(url_ap,cookies=self.cookies, callback=self.parse_items_2)
                        return
                else:
                    return
                        
        return

    '''
        Esta función monta la url pre-final para acceder al servidor que sea para obtener la url final.
        Pasamos el splash y llamamos a la función parse_items_3
    '''
    def parse_items_2(self,response):
        titulo = response.selector.xpath('//title/text()').extract()
        for q in response.css(".content"):
            lista = q.css(".visit-buttons a::attr(href)").extract()
            st_aux = ''.join(str(x) for x in lista)
            url_final = "https://www.megadede.com" + st_aux.strip()
            self.url_nombre[url_final] = [titulo]
            yield SplashRequest(url_final,cookies=self.cookies, callback=self.parse_items_3)
            

    '''
        Esta función obtiene la URL final del servidor y con la variable global de nombre del capitulo introduce el capitulo.
        Por último, guardamos en el archivo
    '''
    def parse_items_3(self,response):
        r = requests.get(response.url, cookies=self.cookies)
        url_openload = r.url
        print "###############################################################"
        ch_name_aux = str(self.format_chapter_name(''.join(str(x) for x in self.url_nombre[response.url]))).replace(',','')
        ch_name_aux_1 = ch_name_aux.replace("'","")
        ch_name_aux_2 = ch_name_aux_1.replace('(', '[ ')
        ch_name_aux_3 = ch_name_aux_2.replace(')', ' ]')
        ch_name = ch_name_aux_3.replace(',', '   -   ')
        print "Chapter Name => ",ch_name
        print "Chapter URL => ",url_openload
        print "###############################################################"
        yield {
            'capitulo': ch_name,
            'url': url_openload,
            }
        

    def format_chapter_name(self,chapter_name):
        season = self.obtain_season(chapter_name)
        chapter = self.obtain_chapter(chapter_name)
        return "Season ",season," - Chapter ",chapter

    def obtain_season(self,chapter_name):
        season = chapter_name.split("x")[0]
        return season[-2:]

    def obtain_chapter(self,chapter_name):
        chapter = chapter_name.split("x")[1]
        return chapter[0:2]

    def logo(self):

        print GREEN+'#####################################################################################################'
        print '#                                                                                                   #'
        print '#                                                                                                   #'
        print '#    '+RED+'******  *   *  *******  ******  ******  ******  *******  ******    ******  ******    ******    '+GREEN+'#'
        print '#    '+RED+'*        * *      *     *    *  *    *  *          *     *     *   *       *     *   *         '+GREEN+'#'
        print '#    '+RED+'***       *       *     ******  ******  *          *     *      *  ***     *      *  ***       '+GREEN+'#'
        print '#    '+RED+'*        * *      *     * *     *    *  *          *     *     *   *       *     *   *         '+GREEN+'#'
        print '#    '+RED+'******  *   *     *     *  *    *    *  ******     *     ******    ******  ******    ******    '+GREEN+'#'
        print '#                                                                                         '+RED+'v1.0      '+GREEN+'#'
        print '#                                                                                                   #'
        print '#                                                                   '+RED+'By: Cristian Romero Povea       '+GREEN+'#'
        print '#####################################################################################################'+RESET




