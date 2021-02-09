import requests
import json
import pandas as pd
from iexfinance.stocks import Stock
from datetime import datetime
##API Token##
api_token = ''
blacklist = ['DD','GOOD','NEXT','GAIN','HEAR','NEW','YOLO','HEAR','FOR','GO']

stocks = pd.read_excel('stocks.xlsx')
symbols = stocks['symbol'].to_list()

s = requests.Session()
s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'})
r = s.get('https://www.reddit.com/')
r = s.get('https://gateway.reddit.com/desktopapi/v1/subreddits/wallstreetbets?sort=new')
data = json.loads(r.text)
token = data['token'] 
count = 0
stocks = []
scores = []
for i in data['posts'].keys():
    words = data['posts'][i]['title'].split(' ')
    score = data['posts'][i]['score']
    count = count +1
    print(count)
    for word in words:
        if word in symbols and len(word) > 1 and word not in blacklist:
            if word in stocks:
                index = stocks.index(word)
                scores[index] = int(scores[index]) + int(score)
            else:
                stocks.append(word)
                scores.append(score)

for i in range(0,50):
    url = 'https://gateway.reddit.com/desktopapi/v1/subreddits/wallstreetbets?after={}&sort=new'.format(token)
    r = s.get(url)
    data = json.loads(r.text)
    try:
        token = data['token'] 
    except:
        print(data)
        break
    for i in data['posts'].keys():
        count = count +1
        print(count)
        words = data['posts'][i]['title'].split(' ')
        score = data['posts'][i]['score']
        for word in words:
            if word in symbols and len(word) > 1 and word not in blacklist:
                if word in stocks:
                    index = stocks.index(word)
                    scores[index] = int(scores[index]) + int(score)
                else:
                    stocks.append(word)
                    scores.append(score)
data_dict = {
    'Symbol':stocks,
    'Upvotes':scores,
    'CompanyName':[],
    'Change':[],
    'latestPrice':[]
}


for i in range(0,len(stocks)):
    batch = Stock(stocks[i],token=api_token,output_format='json')
    batch = batch.get_quote()
    data_dict['CompanyName'].append(batch['companyName'])
    data_dict['Change'].append(batch['changePercent'])
    data_dict['latestPrice'].append(batch['latestPrice'])

df = pd.DataFrame(data_dict)
timestamp = str(data['posts'][list(data['posts'].keys())[-1]]['created'])[0:10]
timestamp = int(timestamp)
dt_object = datetime.fromtimestamp(timestamp)
print("Last Scrapped Post at:", dt_object)

df.to_excel('reddit.xlsx')




