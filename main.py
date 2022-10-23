from aux_spiders import *

def main():
    Scraper()
    ConcatGpusJsons()
    CreateGpusJson()
    PostGpus()

if __name__ == '__main__':
    main()