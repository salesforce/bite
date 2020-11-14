import re, os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request
from urllib.parse import urljoin
from pathlib import Path


class HWZSpider(scrapy.spiders.CrawlSpider):

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
    }

    name = "hwz_spider"
    # Crawl links limited to this domain
    domain_name = "https://forums.hardwarezone.com.sg"
    #start_urls = ["https://forums.hardwarezone.com.sg/infotech-clinics-1/"]
    main_subforums = ["/infotech-clinics-1/"]
    #main_subforums = ["/digital-entertainment-lifestyle-hub-225/",]
    show_all_threads = '?pp=200&daysprune=-1'
    show_all_pages = '?pp=50'
    filter_tokens = ['/misc.php?', '/external.php?', 'www.hardwarezone.com.sg']
    parents = {}

    def __init__(self):
        self.start_urls = [self.domain_name+sf for sf in self.main_subforums]

    def has_filter_tokens(self, url):
        for token in self.filter_tokens:
            if token in url:
                return True
        return False

    def parse(self, response):
        """Every URL processed in this function unless otherwise specified,
        yielded Requests also come here, duplicated Request urls are automatically handled by scrapy
        """
        subforum_list = response.xpath('//table[@class="tborder" and @width="100%"]/tbody//tr/td/div')

        if self.domain_name in response.url and response.url[-5-len(self.show_all_pages):-len(self.show_all_pages)] == '.html':
            self.scrape(response)

            # Thread page navigation
            thread_nav = response.xpath(
                '//div[contains(@id, "posts")]/following-sibling::table[1]')
            for thread_page_a in thread_nav.xpath('.//li'):
                href = thread_page_a.xpath('./a/@href').get()
                if href:
                    url = urljoin(self.domain_name, href.split('?')[0]+self.show_all_pages)
                    print('55',url)
                    yield Request(url)

        elif subforum_list and response.url[len(self.domain_name):] in self.main_subforums:
            # list of subforums
            ends_with = '"/" = substring(., string-length(.) - string-length("/") +1)'
            parent = response.url[len(self.domain_name)+1:-1]
            Path(parent).mkdir(parents=True, exist_ok=True)
            for subforum in subforum_list.xpath('./a/@href[starts-with(.,"/") and' + ends_with + ']').getall():
                self.parents[subforum.strip('/')] = parent
                url = urljoin(self.domain_name, subforum+self.show_all_threads)
                print('67',url)
                yield Request(url)
        else:
            # subforum page with list of threads
            threads_table = response.xpath('//table[contains(@id, "threadslist")]')  # List of threads
            threads_table_body = threads_table.xpath(
                './tbody[contains(@id, "threadbits_forum")]')
            for trow in threads_table_body.xpath('./tr//td[contains(@class,"alt1")]'):
                href = trow.xpath('.//a/@href').get()
                if href and not self.has_filter_tokens(href):
                    url = urljoin(self.domain_name, href+self.show_all_pages)
                    print('79',url)
                    yield Request(url)

            # Forum thread navigation
            forum_nav = response.xpath(
                '//table[contains(@id, "threadslist")]/following-sibling::table[1]')
            for forum_page_a in forum_nav.xpath('//li'):
                href = forum_page_a.xpath('./a/@href').get()
                if href:
                    url = urljoin(self.domain_name, href.split('?')[0]+self.show_all_threads)
                    print('89',url)
                    yield Request(url)

    def scrape(self, response):
        """ Scrape individual page in thread
        """
        print("Scraping from {}".format(response.url))
        subforum = re.search('/(.+?)/',response.url[len(self.domain_name):]).group(1)
        posts_table = response.xpath('//div[contains(@id, "posts")]')
        with open(os.path.join(self.parents[subforum],subforum), 'a+') as out:
            for post in posts_table.xpath('./div[contains(@class, "post-wrapper")]'):
                post_message = post.xpath('.//div[contains(@class, "post_message")]/text()').get()
                if post_message and post_message.strip() and '^M' not in post_message and len(post_message.split()) > 2:
                    out.write(post_message.strip()+'\n')

process = CrawlerProcess(settings={})
process.crawl(HWZSpider)
process.start()
