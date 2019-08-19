# Importing of Modules
import scrapy
import requests

# url variable to store user input (Will not be used if the user input "Yes" later as other links is not working due to
# security reasons)
url = input("URL: ")
print("Status code:")
print("-----------")
# "r" variable to store the GET request from "url"
r = requests.get(url)
# "r.status_code" to get the status code from the GET request
print("\t *", r.status_code)
print("-----------")
try:
    # "ans" variable to store user input. (Choosing No will use "url" variable, choosing Yes doesn't)
    ans = input("Do you want to change the header user-agent? ")
    if(ans=="Yes"):
        # "device" variable to store what device the user wishes to change the header to
        device = input("Please enter Device OS you want to change to: ")
        print("-----------")
        url2 = "http://172.18.58.238/headers.php/"
        headers = {
            'User-Agent': device
        }
        # "rh" variable to store GET request for the header
        rh = requests.get(url2, headers=headers)
        print(rh.text)
        print("-----------")
        input()
    elif(ans=="No"):
        print("-----------")
        h = requests.head(url)
        for x in h.headers:
            print("\t ", x, ":", h.headers[x])
        print("-----------")
        input()
    else:
        print("Error! Please enter Yer or No (It's case sensitive)")
except:
    print("Error")


# Scrapy Class
# To run this Class: scrapy runspider DA_McDonalds.py
# To run and save output to a file: scrapy runspider DA_McDonalds.py -o results.json -t json
class NewSpider(scrapy.Spider):
    name = "new_spider"
    start_urls = [url]
    def parse(self, response):

        xpath_selector = '//img'
        for x in response.xpath(xpath_selector):
            newsel = '@src'
            yield {
                'Image Link': x.xpath(newsel).extract_first(),
            }

        # To recurse next page
        Page_selector = '.next a ::attr(href)'
        next_page = response.css(Page_selector).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
