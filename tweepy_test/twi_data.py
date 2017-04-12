import json
import pandas as pd
import re


tweets_data_path = 'twitter_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path,"rb")

for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

#print (len(tweets_data))
tweets = pd.DataFrame()
tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))
tweets['lang'] = list(map(lambda tweet: tweet['lang'], tweets_data))
tweets['country'] = list(map(lambda tweet: tweet['place']['country'] if \
                        tweet['place'] != None else None, tweets_data))

tweets_by_lang = tweets['lang'].value_counts()
tweets_by_cou = tweets['country'].value_counts()

#print(tweets_by_lang)

def word_in_text(word,text):
    word = word.lower()
    text = text.lower()
    match = re.search(word,text)
    if match:
        return True
    return False

tweets['python'] = tweets['text'].apply(lambda tweet:word_in_text('python',tweet))
tweets['django'] = tweets['text'].apply(lambda tweet:word_in_text('django',tweet))
tweets['java'] = tweets['text'].apply(lambda tweet:word_in_text('java',tweet))

'''
print (tweets['python'].value_counts()[True])
print (tweets['django'].value_counts()[True])
print (tweets['java'].value_counts()[True])
'''

tweets['programming'] = tweets['text'].apply(lambda tweet: word_in_text('programming', tweet))
tweets['tutorial'] = tweets['text'].apply(lambda tweet: word_in_text('tutorial', tweet))
tweets['relevant'] = tweets['text'].apply(lambda tweet: word_in_text('programming', tweet) \
                                          or word_in_text('tutorial', tweet))

'''
print (tweets['programming'].value_counts()[True])
print (tweets['tutorial'].value_counts()[True])
print (tweets['relevant'].value_counts()[True])
'''

def extract_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex,text)
    if match:
        return match.group()
    return ''

tweets['link'] = tweets['text'].apply(lambda tweet:extract_link(tweet))

tweets_relevant = tweets[tweets['relevant'] == True]
tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != '']


print (tweets_relevant_with_link[tweets_relevant_with_link['python'] == True]['link'])
print (tweets_relevant_with_link[tweets_relevant_with_link['java'] == True]['link'])
print (tweets_relevant_with_link[tweets_relevant_with_link['django'] == True]['link'])


