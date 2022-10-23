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

def GetProperties(data):
  #properties = ['model', 'brand']
  properties = [
    {
      'name': 'model', 'items': [] 
    },
    {
      'name': 'brand', 'items': []
    }
  ]
  models = []
  brands = []

  for property in properties:
    propertyFinds = list(map(lambda x: x[property['name']], data))
    propertiesArray = []
    if property == 'model':
      propertiesArray = models
    else:
      propertiesArray = brands
    for property in propertyFinds:
      if property not in propertiesArray:
        propertiesArray.append(property)

  return models, brands

def ConcatGpusJsons():
  with open('c:/Users/peter/projetos/kpt_scraper/kabumGpus.json') as kgpus:
        dk = json.load(kgpus)

  with open('c:/Users/peter/projetos/kpt_scraper/pichauGpus.json') as pgpus:
      dp = json.load(pgpus)

  with open('c:/Users/peter/projetos/kpt_scraper/terabyteGpus.json') as tgpus:
      dt = json.load(tgpus)

  with open('c:/Users/peter/projetos/kpt_scraper/terabyteGpus2.json') as tgpus2:
      dt2 = json.load(tgpus2)

  combined = dt + dt2 + dk + dp

  models, brands = GetProperties(combined)

  combined = json.dumps(combined, separators=(',', ':'))

  return combined

def CreateGpusJson():
  data = ConcatGpusJsons()
  with open('c:/Users/peter/projetos/kpt_scraper/gpusData.json', 'w') as outfile:
      outfile.write(data)

def PostGpus():
  with open('c:/Users/peter/projetos/kpt_scraper/gpusData.json') as gpus:
      gpusData = json.load(gpus)
  
  uri = 'https://localhost:7298/api/Gpus'
  headers = {"Content-Type": "application/json; charset=utf-8"}
  session = requests.Session()
  session.verify = False

  for gpu in gpusData:
      session.post(uri, headers=headers, data=json.dumps(gpu))

def Scraper():
  configure_logging()
  settings = get_project_settings()

  runner = CrawlerRunner(settings)

  runner.crawl(KabumGpuSpider)
  runner.crawl(PichauGpuSpider)
  runner.crawl(TerabyteGpuSpider)
  runner.crawl(TerabyteGpuSpider2)

  d = runner.join()

  d.addBoth(lambda _: reactor.stop())  # type: ignore

  reactor.run()  # type: ignore