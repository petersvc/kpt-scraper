import scrapy

class KabumGpuSpider(scrapy.Spider):
    name = 'KabumGpuSpider'
    #pagination = 1
    #first_half_url = 'https://www.kabum.com.br/hardware/placa-de-video-vga?page_number='
    #second_half_url = '&page_size=100&facet_filters=&sort=most_searched'
    #start_urls = [first_half_url + str(pagination) + second_half_url]
    #stop_scrapping = False 
    #
    url='https://www.kabum.com.br/hardware/placa-de-video-vga?page_number={}&page_size=100&facet_filters=&sort=most_searched'
    
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'

    custom_settings = {
        'FEEDS': {
            'kabumGpus.json': {
                'format': 'json'
            }
        }
    }

    def start_requests(self):
        for i in range(1, 7):
            yield scrapy.Request(self.url.format(i))

    def parse(self, response):
        for products in response.css("div.productCard"):
            link = products.css("a::attr(href)").get().replace('/produto', 'kabum.com.br/produto')
            price = products.css("div span.priceCard::text").get().replace('R$\xa0', '')
            name = products.css("div span.nameCard::text").get().replace('\u00ed', 'i')
            #image = products.css("div a img.imageCard::attr(src)").get()

            name = name.replace('Placa de Video ', '')
            name = name.replace('Placa de V\u00ecdeo ', '')
            priceInt = price.replace('.', '') 
            
            if name.find(',') != -1:
                virgula_index = name.index(',')
                name = name[:virgula_index]              

            if priceInt.find(',') != -1:
                virgula_index = priceInt.index(',')
                priceInt = priceInt[:virgula_index] 
                priceInt = int(priceInt)

            if price == '---':
                self.stop_scrapping = True
                break
            
            matches_name = ['rtx', 'RTX', 'Rtx', 'rx', 'RX', 'Rx', 'gtx', 'GTX', 'Gtx']

            matches_brand = [
                'Afox', 'afox', 'Akasa', 'akasa', 'Asrock', 'asrock', 'Asus', 'asus',
                'ASUS', 'Axle', 'axle', 'Barrow', 'barrow', 'Colorful', 'colorful', 
                'Duex', 'duex', 'Evga', 'EVGA', 'evga', 'Gainward', 'gainward', 
                'Galax', 'GALAX', 'galax', 'Gigabyte', 'gigabyte', 'MSI', 'Msi', 'msi',
                'PALIT', 'Palit', 'palit', 'PCYES', 'PCYes', 'pcyes', 'Pcyes', 'Pny',
                'PNY', 'pny', 'Power Color', 'Powercolor', 'powercolor', 'power-color',
                'RedDragon', 'reddragon', 'Sapphire', 'sapphire', 'XFX', 'xfx', 'Zotac',
                'ZOTAC', 'zotac'
            ]

            brand = 'Outra'

            for x in matches_brand:
                if link.find(x) != -1:
                    brand=x

            if not brand.isupper():
                #print(matches_brand[8])
                if not brand[0].isupper():
                    a = list(brand)
                    a[0] = a[0].capitalize()
                    brand = ''.join(a)
                    #print(matches_brand[8])
            else:
                brand = brand.capitalize()

            models_nvidia = [
                '1050', '1650', '1660', '2060', '2070', '2080', '3050', '3060', '3070',
                '3080', '3090', '4050', '4060', '4070', '4080' '4090'
            ]

            models_amd = [
                '6400', '6500', '6550', '6600', '6650', '6700', '6750', '6800', '6850',
                '6900', '6950'
            ]

            model = 'outra'
            manufactor = 'outra'

            for x in models_nvidia:
                if name.find(x) != -1:
                    model= x
                    manufactor = 'Nvidia'
            
            if model == 'outra':
                manufactor = 'Amd'
                for x in models_amd:
                    if name.find(x) != -1:
                        model= x                        

            series_nvidia = ['16', '20', '30', '40']
            series_amd = ['6000']

            serie = 'outra'

            if manufactor == 'Nvidia':
                for x in series_nvidia:
                    if model.find(x) != -1:
                        serie= x
            
            if manufactor == 'Amd':
                if model != 'outra':
                    temp_model = int(model)
                    for x in series_amd:                        
                        if temp_model >= int(x) and temp_model < int(x) + 1000:
                            serie= x

            if any(x in name for x in matches_name):
                if brand != 'Barrow' and serie != 'outra':
                    yield {
                        #'id': link,
                        'manufactor': manufactor,
                        'serie': serie,
                        'model': model,
                        'brand': brand,
                        'name': name,
                        'link': link,
                        'price': price,
                        'priceInt': priceInt,
                        'store': 'Kabum'
                        #'image': image,
                    }

        #next_page = response.css('li.next a.nextLink::text').get()

        #if next_page == '>' and self.stop_scrapping == False:
        #    self.pagination += 1
        #    new_url = self.first_half_url + str(self.pagination) + self.second_half_url
        #    self.start_urls = new_url
        #    
        #    yield response.follow(new_url, callback=self.parse)