import tweepy as tp
import pandas as pd
import re
import sys
import os

def words_in_text(words,text):
        text = text.lower()
        for w in words:
            w = w.lower()
            match = re.search(w,text)
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


    def search_keyword(self,word,maxTweets,tweetsPerQry):
        result = []
        tw_count = 0
        while tw_count < maxTweets:
            try:
                new_tweets = self.api.search(q=word,count=tweetsPerQry)
                   
                if(not new_tweets):
                    print("No more tweets found")
                    break
                for t in new_tweets:
                    result.append(t._json)
                tw_count+=len(new_tweets)
                #print("Downloaded {0} tweets".format(tw_count))
            except tp.TweepError as e:
                print("error: " + str(e))
                break
        print("Done")

        return result

    def get_all_related_tweets(self,word_list,maxTweets,tweetsPerQry,textonly=True,):
        if tweetsPerQry > maxTweets:
            tweetsPerQry = maxTweets
        result_list = []
        self.keyword_list = word_list
        tw_per_word = maxTweets/len(word_list)

        for word in word_list:
            tweets_json = self.search_keyword(word,tw_per_word,tweetsPerQry)
            if textonly:
                for tw in tweets_json:
                    
                    result_list.append(tw['text'])
            else:
                result_list.append(tweets_json)
  
        return result_list



    
# This can only be used with textonly
    def most_relevant(self,twlist,return_num):
        num_keywords = len(self.keyword_list)
        wordlist = self.keyword_list
        tweet_df = pd.DataFrame()
        tweet_df['text'] = twlist
        relevant_tweets = []
        while num_keywords>0:
            tweet_df['relevant'] = tweet_df['text'].apply(\
                lambda tweet:words_in_text(wordlist,tweet))
            relevant_tweets = tweet_df[tweet_df['relevant']== True]['text'] 
            if len(relevant_tweets) < return_num:
                wordlist = wordlist[:-1]
                num_keywords -= 1
                tweet_df.drop('relevant',axis=1)
            else:
                break
        if len(relevant_tweets) == 0:
                return twlist[:(return_num//2)]+twlist[-(return_num//2):]
        return relevant_tweets[:return_num]





if __name__ == '__main__':

   tw = twi_util()
   tw.appAuth_api()

   #raw_tw = tw.get_all_related_tweets(["trump","china"],1000)
   #result = tw.most_relevant(raw_tw,5)
   #print(result)



