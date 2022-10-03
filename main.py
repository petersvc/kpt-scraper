import json
import requests
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from scrapy_project.spiders.KabumGpus import KabumGpuSpider
from scrapy_project.spiders.PichauGpus import PichauGpuSpider
from scrapy_project.spiders.TerabyteGpus import TerabyteGpuSpider
from scrapy_project.spiders.TerabyteGpus2 import TerabyteGpuSpider2

def main():
    scraper()
    concatGpusJsons()
    addGpus()

def scraper():
    configure_logging()
    settings = get_project_settings()

    runner = CrawlerRunner(settings)

    runner.crawl(KabumGpuSpider)
    runner.crawl(PichauGpuSpider)
    runner.crawl(TerabyteGpuSpider)
    runner.crawl(TerabyteGpuSpider2)

    d = runner.join()

    d.addBoth(lambda _: reactor.stop())

    reactor.run()
    
def concatGpusJsons():

    with open('c:/Users/peter/projetos/backend/python/scrapy_project/kabumGpus.json') as kgpus:
        dk = json.load(kgpus)

    with open('c:/Users/peter/projetos/backend/python/scrapy_project/pichauGpus.json') as pgpus:
        dp = json.load(pgpus)

    with open('c:/Users/peter/projetos/backend/python/scrapy_project/terabyteGpus.json') as tgpus:
        dt = json.load(tgpus)

    with open('c:/Users/peter/projetos/backend/python/scrapy_project/terabyteGpus2.json') as tgpus2:
        dt2 = json.load(tgpus2)

    combined = dk + dp + dt + dt2
    combined = json.dumps(combined)

    with open('c:/Users/peter/projetos/backend/python/scrapy_project/gpusData.json', 'w') as outfile:
        outfile.write(combined)

def addGpus():
    with open('c:/Users/peter/projetos/backend/python/scrapy_project/gpusData.json') as gpus:
        gpusData = json.load(gpus)
    
    uri = 'https://localhost:7298/api/Gpus'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    session = requests.Session()
    session.verify = False

    for gpu in gpusData:
        session.post(uri, headers=headers, data=json.dumps(gpu))

if __name__ == '__main__':
    main()