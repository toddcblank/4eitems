import requests

baseUrl = "https://www.wizards.com/dndinsider/compendium/"
pages = [
    "background",
    "theme",  
    "class",
    "associate",
    "monster",
    "deity",
    "disease",
    "epicdestiny",
    "feat",
    "glossary",
    "item",
    "paragonpath",
    "poison",
    "race",
    "ritual",
    "terrain",
    "trap",
    "power"
]

startIds = {
    "background": 840,
    "theme": 200,  
    "class": 225,
    "associate": 200,
    "monster": 601,
    "deity": 200,
    "disease": 200,
    "epicdestiny": 200,
    "feat": 2839,
    "glossary": 100,
    "item": 100,
    "paragonpath": 1,
    "poison": 20,
    "race": 70,
    "ritual": 99,
    "terrain": 100,
    "trap": 100,
    "power": 1000 
}

# //?id=13300
# // let endId = 14000;
# endId = 200000;
errorThreshold = 1000

ddiCookies = {
    'f5_cspm': '1234',
    'resultsPerPage': '20',
    '__utma': '28542179.698707295.1575994178.1575994178.1575994178.1',
    '__utmc': '28542179',
    '__utmz': '28542179.1575994178.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '__utmt': '1',
    'iPlanetDirectoryPro': '223904fe-0e20-4767-8724-ab60586778b1',
    'BIGipServerWWWCOMPPool1': '1024461066.20480.0000',
    'BIGipServerWWWPool1': '740558858.20480.0000',
    '__utmb': '28542179.8.10.1575994178'
}



# options =  {
#     method: "GET",
#     "rejectUnauthorized": false, 
#     headers: {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
#         'Sec-Fetch-User': '?1',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#         'Sec-Fetch-Site': 'none',
#         'Sec-Fetch-Mode': 'navigate',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
#     }
# }

# process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0

def scrapeDdi():
    for page in pages:
        currentErrors = 0

        startId = startIds[page]
        print("Starting at " + str(startId) + " for " + page)
        id = startId
        while (currentErrors < errorThreshold):
            resourceUrl = baseUrl + page + ".aspx?id=" + str(id)
            if not(requestInfo(resourceUrl, id, page)):
                currentErrors = currentErrors + 1
                # print("Errors: " + str(currentErrors))
            else:
                currentErrors = 0

            id = id + 1
        print("Stopped scraping " + page + " at " + str(id))



def requestInfo(resourceUrl, id, type):
    # print("Requesting id " + str(id) + " from " + resourceUrl)
    response = requests.get(resourceUrl, cookies=ddiCookies, verify=False)
    if response.status_code == 200:
        # console.log("writing power " + id)
        # fs.writeFile('./crawled/powers/' + id + '.html', body, ()=>{})
        # print("Found " + type + " " + str(id))
        outputFile = open("./crawled/" + type + "-" + str(id) + ".html", "wb")
        outputFile.write(response.content)
        return True
    else:
        return False

scrapeDdi()