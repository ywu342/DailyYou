from textblob import TextBlob as tb
import numpy as np
import math


def _getNouns(title):
    tags = tb(title).tags
    nouns = [t[0] for t in tags if t[1] == 'NNP' or t[1] == 'NN' ]
    return nouns
    
def tf(word,blob):
    return blob.words.count(word)/len(blob.words)

def n_containing(word,bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def idf(word,bloblist):
    idf_score = math.log(len(bloblist)/(1+n_containing(word,bloblist)))
    return idf_score


def tfidf(word,blob,bloblist):
    return tf(word,blob) * idf(word,bloblist)


def _sort_words(news_list,title_list):
    sorted_list=[]
    for i in range(len(news_list)):
        nouns = _getNouns(title_list[i])
        score={n:tfidf(n,news_list[i],news_list) for n in nouns}
        sorted_pair = sorted(score.items(), key=lambda x: x[1],reverse=True)
        sorted_title = [x[0] for x in sorted_pair]
        if len(sorted_title) > 5:
            sorted_title = sorted_title
        sorted_list.append(sorted_title)
    return sorted_list


title_list = ['Google Reaches Deal With Russia Over Android',
             'Apple is having trouble getting the iPhone 8’s signature feature to actually work',
              'Genji is coming to Heroes of the Storm',
              'Cancelling The Production Of The NES Classic Edition To Protect The Nintendo Switch Makes No Sense',
              "Samsung is blocking users from customizing the Galaxy S8's Bixby button"]

news_list=[]
news_list.append(tb("A long-running dispute between Google and Russia’s antimonopoly watchdog has now reached some level of closure,\
           as Google has now reportedly arrived at an out-of-court settlement with Russia regarding the tech company’s Android OS. \
           The deputy head of the Federal Antimonopoly Service (FAS), Alexei Dotsenko, announced the news today, confirming the deal. \
           While Google has reportedly said in response that the interests of both parties have been satisfied, further corroborating\
           that a deal has indeed been reached.\
           As part of the settlement, Google will not be able to insist on the exclusivity of its own apps on Android devices in Russia.\
           In addition, Google will not be able to demand that other competing search engines and apps cannot be installed. Furthermore, \
           the giant tech company must offer a tool that will enable users to select the default search engine of their own choice on\
           Android-based smartphones and tablets."))
news_list.append(tb("The iPhone 8’s signature design feature will be a bezeless display extending from edge to edge. That means there’s\
                    no room for a physical home button on the device, so Apple has to “kill” it. However, more reports indicate the iPhone\
                    maker may not be able to do so this year.\
                    Technically, Apple already killed the physical home button with the iPhone 7 series. These devices do not have a home\
                    button that you can actually press. Furthermore, the iPhone 6s introduced the 3D Touch screen that theoretically allows \
                    Apple to relegate several home button functions to any region of the display."))

news_list.append(tb("While the Nintendo Switch is still in its infancy, the fact that the NES Classic Edition will cease production in North \
                    American territories makes very little sense, especially if the intent behind it is to protect the Switch.\
                    At present the Switch lacks any support for Virtual Console and that is obviously still an issue. However, to think that\
                    the NES Classic Edition competes with that directly is entirely misguided.\
                    Now, the reason I bring this up is that Dave Thier recently talked with Wedbush Security Analyst Michael Pachter about \
                    the current and entirely mystifying situation regarding the NES Classic Edition.\
                    Mystifying because it seems that only North American territories will cease production of this micro console, whereas its\
                    future in Europe and Japan is arguably more open ended."))
news_list.append(tb("The cyborg ninja Genji will soon be the latest member of the Overwatch squad to take up the fight in Heroes of the Storm. \
                Blizzard announced today that the one-time 'carefree youngest scion of the Shimada clan,'\
                who was grafted into a cyborg body by Overwatch after his older brother Hanzo hung a job on him, will enter the arena as 'an\
                opportunistic, highly-mobile Assassin who can tear apart a weak backline.'\
                Genji's basic abilities are Shuriken, which enables him to fling three throwing stars in a 'spread pattern,' each damaging \
                the first enemy it hits; Deflect, which grants protection for 1.25 seconds, "))
news_list.append(tb("Ahead of the phone's commercial launch later this week, Samsung has reportedly prevented the Bixby button on its Galaxy S8 \
                    from being remapped to perform other functions. It was previously reported that a third-party app would be able to change the \
                    button's purpose;instead of opening Samsung's personal assistant, perhaps some users would prefer that it trigger Google Assistant,\
                    launch the camera, or open a favorite app. According to a post at XDA Developers, a new Galaxy S8 firmware update from Samsung now\
                    shuts down the ability to remap the Bixby button. Previously, the button's command was 'intercepted' by the Accessibility Services built\
                    into Android."))
