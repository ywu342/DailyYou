#from tweepy.streaming import StreamListener
#from tweepy import OAuthHandler
#from tweepy import Stream
import tweepy as tp


access_token = "823258283356069890-WnDgjbmQBCB4diRjRQo93BReweA9PyX"
access_token_secret = "WltG8un0pZhADrlFi9xVPIkYzJMRa3fg9jNXHMPuy4jSD"
consumer_key = "K0UJQEVg1WhQD8KK7r3BfQQ1T"
consumer_secret = "srxUZe6xy8xyQbsonNFQW8mGlLPRL1XvIPlW88WSqs7dgUsybq"



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

