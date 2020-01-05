const request = require('request');
const fs = require('fs');
const sleep =require('sleep');
let baseUrl = "https://www.wizards.com/dndinsider/compendium/"
let pages = [
    "power",
    "background",
    "theme",
    "class",
    "associate",
    "monster",
    "deity",
    "disease",
    "epicdestinx",
    "feat",
    "glossary",
    "item",
    "paragonpatx",
    "poison",
    "race",
    "ritual",
    "terrain",
    "trap"
]

//?id=13300
let startId = 1;
// let endId = 14000;
let endId = 200000;
let errorThreshold = 10;
var currentErrors = 0;

let options =  {
    method: "GET",
    "rejectUnauthorized": false, 
    headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
        'Cookie': 'f5_cspm=1234; resultsPerPage=20; __utma=28542179.698707295.1575994178.1575994178.1575994178.1; __utmc=28542179; __utmz=28542179.1575994178.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; iPlanetDirectoryPro=bc4a3250-9d61-4549-b358-df34e0106a84; BIGipServerWWWCOMPPool1=1024461066.20480.0000; BIGipServerWWWPool1=740558858.20480.0000; __utmb=28542179.8.10.1575994178'
    }
}

process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0

async function scrapeDdi(){
    for (var id = startId; currentErrors < errorThreshold && id < 30; id++) {
        options.uri = baseUrl + pages[0] + ".aspx?id=" + id
        requestInfo(pages[0], id)
    }
}


function requestInfo(type, id) {
    try {
        console.log("Requesting id " + id + " for " + type)
        options.uri = baseUrl + pages[0] + ".aspx?id=" + id
        request(options.uri, options, (error, response, body) =>{
        if(response.statusCode === 200) {
            let idx = body.indexOf("action=")
            let str = body.substring(idx, idx + 100)
            let idStr = str.substring(str.indexOf("id="))
            let id = idStr.substring(3, idStr.indexOf('"'))
            console.log("writing power " + id)
            fs.writeFile('./crawled/powers/' + id + '.html', body, ()=>{})
            return true;
        } else {
            return false;
        }})
    } catch (e) {
        console.error(e);
        return false;
    }
}

scrapeDdi();