import tweepy as tp
import sys
import os

class twi_util():

    def __init__(self):
        self.access_token = "823258283356069890-WnDgjbmQBCB4diRjRQo93BReweA9PyX"
        self.access_token_secret = "WltG8un0pZhADrlFi9xVPIkYzJMRa3fg9jNXHMPuy4jSD"
        self.api_key = "K0UJQEVg1WhQD8KK7r3BfQQ1T"
        self.api_secret = "srxUZe6xy8xyQbsonNFQW8mGlLPRL1XvIPlW88WSqs7dgUsybq"
        self.auth = None
        self.api = None

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


    def search_keyword(self,word,maxTweets,tweetsPerQry=100,sinceId=None,maxId=sys.maxsize):
        if tweetsPerQry > 100:
            tweetsPerQry = 100
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

    


    def most_relevant(self,)











class StdOutListener(tp.StreamListener):

    def on_data(self,data):
        print (data)
        return True

    def on_error(self,status):
        print (status)

if __name__ == '__main__':

    lis = StdOutListener()
    auth = tp.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    #stream = tp.Stream(auth,lis)

    #stream.filter(track=['python','django','java','c++'])
    api = tp.API(auth)
    follower = tp.Cursor(api.followers,'krachik').items(10)
    first_friend = follower.next().screen_name
    #friend_posts = tp.Cursor(api.user_timeline(),'krachik').items(10)
    friend_posts = api.user_timeline(screen_name=first_friend, count=10)

