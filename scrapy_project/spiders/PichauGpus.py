import scrapy

class PichauGpuSpider(scrapy.Spider):
    name = 'PichauGpuSpider'
    pagination = 1
    # https://www.kabum.com.br/hardware/placa-de-video-vga?page_number='
    #first_half_url = 'https://www.pichau.com.br/hardware/placa-de-video?page='
    #second_half_url = '&page_size=100&facet_filters=&sort=most_searched'
    #start_urls = ['https://www.pichau.com.br/hardware/placa-de-video']  # + second_half_url]
    #stop_scrapping = False

    url='https://www.pichau.com.br/hardware/placa-de-video?sort=price-asc&page={}'
    
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'

    custom_settings = {
        'FEEDS': {
            'pichauGpus.json': {
                'format': 'json'
            }
        }
    }

    def start_requests(self):
        for i in range(1, 5):
            yield scrapy.Request(self.url.format(i))

    def parse(self, response):
        for products in response.css("a[data-cy='list-product']"):            
            link = products.css("::attr(href)").get()
            price = products.xpath("div/div[2]/div/div[3]/div/div[1]/text()").get().replace('R$\xa0', '')
            name = products.css("div div h2::text").get().replace('Placa de Video ', '')
            #name = products.css("div div h2::text").get().replace('Placa De Video ', '')
            #image1 = products.xpath("div/div[1]/div/div")
            #image = products.css('div.lazyload-wrapper div img::attr(src)').get()

            priceInt = price.replace(',', '')

            if name.find(',') != -1:
                virgula_index = name.index(',')
                name = name[:virgula_index] 

            if priceInt.find('.') != -1:
                ponto_index = priceInt.index('.')
                priceInt = priceInt[:ponto_index] 
                priceInt = int(priceInt)
                priceInt =  int((priceInt * 88) / 100)

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
                '3080', '3090'
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

            series_nvidia = ['16', '20', '30']
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

            if self.pagination == 4:
                self.stop_scrapping = True
                break

            if any(x in name for x in matches_name):
                if brand != 'barrow' and serie != 'outra':
                    yield {
                        'manufactor': manufactor,
                        'serie': serie,
                        'model': model,
                        'brand': brand,
                        'name': name,
                        'link': 'pichau.com.br' + link,
                        'price': price,
                        'priceInt': priceInt,
                        'store': 'Pichau'
                        #'image': 'https://images.kabum.com.br/produtos/fotos/sync_mirakl/339820/Placa-De-V-deo-Evga-Geforce-Rtx-3070-Ti-Lhr-FTW3-Ultra-Gaming-RGB-8GB-Gddr6x_1662389926_m.jpg',
                    }
