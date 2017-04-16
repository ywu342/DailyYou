import tweepy as tp
import pandas as pd
import re
import sys
import os

def words_in_text(words,text):
        text = text.lower()
        for w in words:
            w = w.lower()
            match = re.search(word,text)
            if not match:
                return False
        return True
    
class twi_util():

    def __init__(self):
        self.access_token = "823258283356069890-WnDgjbmQBCB4diRjRQo93BReweA9PyX"
        self.access_token_secret = "WltG8un0pZhADrlFi9xVPIkYzJMRa3fg9jNXHMPuy4jSD"
        self.api_key = "K0UJQEVg1WhQD8KK7r3BfQQ1T"
        self.api_secret = "srxUZe6xy8xyQbsonNFQW8mGlLPRL1XvIPlW88WSqs7dgUsybq"
        self.auth = None
        self.api = None
        self.keyword_list = []

    def oauth_api(self):
        self.auth = tp.OAuthHandler(self.api_key,self.api_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tp.API(self.auth)

    def appAuth_api(self):
        self.auth = tp.AppAuthHandler(self.api_key,self.api_secret)
        self.api = tp.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        if(not self.api):
            print("Can't Authehticate")
            sys.exit(-1)


    def search_keyword(self,word,maxTweets,tweetsPerQry,sinceId,maxId):
        result = []
        tw_count = 0
        while tw_count < maxTweets:
            try:
                if(maxId <= 0):
                    if(not sinceId):
                        new_tweets = self.api.search(q=word,count=tweetsPerQry)
                    else:
                        new_tweets = self.api.search(q=word,count=tweetsPerQry,since_id=sinceId)
                else:
                    if(not sinceId):
                        new_tweets = self.api.search(q=word,count=tweetsPerQry,max_id=str(maxId-1))
                    else:
                        new_tweets = self.api.search(q=word,count=tweetsPerQry,max_id=str(maxId-1),since_id=sinceId)

                if(not new_tweets):
                    print("No more tweets found")
                    break
                for t in new_tweets:
                    result.append(t._json)
                tw_count+=len(new_tweets)
                #print("Downloaded {0} tweets".format(tw_count))
                maxId = new_tweets[-1].id
            except tp.TweepError as e:
                print("error: " + str(e))
                break
        print("Done")

        return result

    def get_all_related_tweets(self,textonly=True,word_list,maxTweets,tweetsPerQry=100,sinceId=None,maxId=sys.maxsize):
        if tweetsPerQry > 100:
            tweetsPerQry = 100
        result_list = []
        self.keyword_list = word_list

        for word in word_list:
            tweets_json = self.search_keyword(word,maxTweets,tweetsPerQry,sinceId,maxId)
            if textonly:
                for tw in tweets_json:
                    #return as list of lists
                    #result_list.append(tw['text'])

                    #return as a whole list
                    result_list += tw['text']
            else:
                #return as list of lists
                #result_list.append(tweets_json)
                result_list += tweets_json
        #return as a whole list
        return result_list



    
# This can only be used with textonly
    def most_relevant(self,twlist,return_num):
        num_keywords = len(self.word_list)
        wordlist = self.word_list
        tweet_df = pd.DataFrame()
        tweet_df['text'] = twlist
        relevant_tweets = []
        while num_keywords>0:
            tweet_df['relevant'] = tweet_df['text'].apply(\
                lambda tweet:words_in_text(wordlist,tweet))
            relevant_tweets = tweet_df[tweet_df['relevant']== True] 
            if len(relevant_tweets) < return_num:
                wordlist = wordlist[:-1]
                num_keywords -= 1
                tweet_df.drop('relevant',axis=1)
            else:
                break
        return relevant_tweets[:return_num]





if __name__ == '__main__':

   

