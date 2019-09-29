from newsapi import NewsApiClient
import pickle

with open('04-News-Headlines/news_api_key.txt','r') as f:
    my_api_key = f.read()

#api = NewsApiClient(api_key=my_api_key)
# get headlines and save data to temp file for development
#data = api.get_top_headlines(category='business', country='us')
#with open('04-News-Headlines/data.pkl','wb') as f:
#    pickle.dump(data, f)

with open('04-News-Headlines/data.pkl','rb') as f:
    data = pickle.load(f)

# options: get_everything(), get_sources(), get_top_headlines()

# extract specific items from the data pull
status = data.get('status') # confirms that the get-request was successful
total_results = data.get('totalResults') # the total number of results returned
articles = data.get('articles')
description = [row.get('description').replace(u'\xa0',' ') for row in articles] # remove non-breaking space (unicode)

for d in description:
    print(d)




