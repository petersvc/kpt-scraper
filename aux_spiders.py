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
  properties = [
   {'name': 'model', 'items': []},
   {'name': 'brand', 'items': []},
   {'name': 'serie', 'items': []}
  ]

  for property in properties:
    allItems = list(map(lambda x: x[property['name']], data))
    for item in allItems:
      if item not in property['items']:
        property['items'].append(item)

  properties.append({'name': 'dataSize', 'items': [len(data), len(data)/30]})

  return properties

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

  properties = GetProperties(combined)

  combined = json.dumps(combined, separators=(',', ':'))
  properties = json.dumps(properties, separators=(',', ':'))

  return combined, properties

def CreateGpusJson():
  data, properties = ConcatGpusJsons()
  with open('c:/Users/peter/projetos/kpt_scraper/gpusData.json', 'w') as outfile:
      outfile.write(data)
  
  with open('c:/Users/peter/projetos/kpt_scraper/gpusDataProperties.json', 'w') as outfile:
      outfile.write(properties)

def PostGpus():
  with open('c:/Users/peter/projetos/kpt_scraper/gpusData.json') as gpus:
      gpusData = json.load(gpus)
  
  uri = 'http://localhost:4000/api/createGpuCollectionData'
  headers = {"Content-Type": "application/json; charset=utf-8"}
  session = requests.Session()
  session.verify = False

  #for gpu in gpusData:
    # session.post(uri, headers=headers, data=json.dumps(gpu))
  session.post(uri, headers=headers, data=json.dumps(gpusData))

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