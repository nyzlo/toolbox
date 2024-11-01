import scrapy
import re
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from modules.misc import Colors, save_results


class ArakaaliSpoder(scrapy.Spider):
	# Manadatory variable for built in Scrapy background calls
	name = "Arakaali"

	def __init__(self, start_url, *args, **kwargs):
		self.start_urls = [start_url] # Scrapy requires a list even tho arakaali only wants 1 URL
		self.link_extractor = LinkExtractor()
		self.visited_urls = set()
		self.links = set()
		self.comments = set()
		self.emails = set()
		self.js_files = set()
		self.extra_files = set()

	def parse(self, response):
		# Check if the url is 200 & text to avoid crawling invalid endpoints
		try:
			if response.status != 200 or 'text' not in response.headers.get(b"Content-Type", b"Missing Content-Type").decode("utf-8"):
				logging.info(f"Skipping non-200/text response: {response.url} ({response.status})")
				return
		except Exception as e:
			logging.error(f"Failure decoding Content-Type")

		self.visited_urls.add(response.url)

		# Extract links & crawl
		try:
			logging.info(f"Extracting data from {self.start_urls}")
			links = self.link_extractor.extract_links(response)
			
			for link in links:
				if link.url.startswith(self.start_urls[0]): # Restrict spoder to the target domain
					self.links.add(link.url)
					yield response.follow(link.url, callback=self.parse)  # Follow link and repeat

			# Extract comments
			comments = response.xpath("//comment()").getall()
			self.comments.update(comments)

			# Extract emails
			emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', response.text)
			self.emails.update(emails)

			# Extract JS files
			js_files = response.css("script[src]::attr(src)").getall()
			for file in js_files:
				self.js_files.add(response.urljoin(file))

			# Extract non-JS files
			interesting_files = re.compile(r'\.(pdf|docx?|xls?|pptx?|zip|rar|txt)$', re.IGNORECASE)
			extra_files = response.css("link[href]::attr(href)").getall()		
			for file in extra_files:
				if interesting_files.search(file):
					self.extra_files.add(response.urljoin(file))
			logging.info("Data extraction success!")
			
		except Exception as e:
			logging.error("Data extracton failed: {e}")
			print(f"Failed to extract data from {self.start_urls}")

	# Scrapy built in function call on finished crawl - transform and store data
	def closed(self, reason):
		try:
			logging.info("Converting and saving results to JSON")
			results = {
				"comments": list(self.comments),
				"links": list(self.links),
				"emails": list(self.emails),
				"js_files": list(self.js_files),
				"extra_files": list(self.extra_files)
			}
			save_results(results, "arakaali", "results.json")
			logging.info("Success!")
		except Exception as e:
			logging.error(f"Failed to convert and save results to JSON")

def run_spoder(start_url):
	try:
		if not start_url.startswith(("http://", "https://")):
			start_url = f"https://{start_url}"
		process = CrawlerProcess(settings={
			"LOG_ENABLED": False, # Disable CrawlerProcess's annoying default verbose logger
			"REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7" # Disable log warnings regarding deprecated values 
		})
		process.crawl(ArakaaliSpoder, start_url=start_url)
		logging.info(f"Starting crawl on {start_url}")
		print(f"{Colors.GREEN}Crawling {start_url}{Colors.RESET}") 
		process.start()
		logging.info(f"Successful crawl!")
		print(f"{Colors.GREEN}\nSuccessful crawl!{Colors.RESET}")

	except Exception as e:
		logging.error(f"Crawl failed - big disaster: {e}")
		print(f"\n{Colors.RED}Crawl failed - sometimes unlucky: {e}{Colors.RESET}")

	logging.info(f"Crawl completed for: {start_url}")
	print(f"\n{Colors.YELLOW}Logs: arakaali/log.txt{Colors.RESET}")
	print(f"\n{Colors.YELLOW}Results: arakaali/results.json{Colors.RESET}")

		