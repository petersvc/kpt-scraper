import scrapy

class TerabyteGpuSpider(scrapy.Spider):
    name = 'TerabyteGpuSpider'
    start_urls = ['https://webcache.googleusercontent.com/search?q=cache%3Ahttps%3A%2F%2Fwww.terabyteshop.com.br%2Fhardware%2Fplacas-de-video%2Famd-radeon&oq=cache%3Ahttps%3A%2F%2Fwww.terabyteshop.com.br%2Fhardware%2Fplacas-de-video%2Famd-radeon&aqs=chrome..69i57j69i58.4003j0j4&sourceid=chrome&ie=UTF-8'] 
    
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'

    custom_settings = {
        'FEEDS': {
            'terabyteGpus.json': {
                'format': 'json'
            }
        }
    }

    def parse(self, response):
        for products in response.css("div.commerce_columns_item_inner"):            
            link = products.css('a.prod-name::attr(href)').get().replace('https://www.', '')
            price = products.css("div.prod-new-price span::text").get().replace('R$ ', '')
            name = products.css("a.prod-name h2::text").get().replace('Placa de Vídeo ', '')
            #image = products.css("div.text-center img::attr(src)").get()

            priceInt = price.replace('.', '')

            if name.find(',') != -1:
                virgula_index = name.index(',')
                name = name[:virgula_index] 

            if priceInt.find(',') != -1:
                ponto_index = priceInt.index(',')
                priceInt = priceInt[:ponto_index] 
                priceInt = int(priceInt)

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
                    manufactor = 'nvidia'
            
            if model == 'outra':
                manufactor = 'amd'
                for x in models_amd:
                    if name.find(x) != -1:
                        model= x                        

            series_nvidia = ['16', '20', '30']
            series_amd = ['6000']

            serie = 'outra'

            if manufactor == 'nvidia':
                for x in series_nvidia:
                    if model.find(x) != -1:
                        serie= x
            
            if manufactor == 'amd':
                if model != 'outra':
                    temp_model = int(model)
                    for x in series_amd:                        
                        if temp_model >= int(x) and temp_model < int(x) + 1000:
                            serie= x

            if any(x in name for x in matches_name):
                if brand != 'barrow' and serie != 'outra':
                    yield {
                        'manufactor': manufactor,
                        'serie': serie,
                        'model': model,
                        'brand': brand,
                        'name': name,
                        'link': link,
                        'price': price,
                        'priceInt': priceInt,
                        'store': 'Terabyte'
                        #'image': image,
                    }
