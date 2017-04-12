import webhoseio
import json, datetime, time
from fileinput import filename

class WebhoseUtil():
    
    def __init__(self):
        webhoseio.config(token="b1f36fd9-527a-4fba-aa07-e87606333561")
        self.output = None

    def request(self, category):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_string = yesterday.strftime("%s")
        #print(yesterday_string)
        q = "language:(english) performance_score:>4 (site_type:news) site_category:"+category
        self.output = webhoseio.query("filterWebData", {"q":q, "sort":"performance_score", "latest":"true"})
        return self.output
    
    def numOfPosts(self):
        return len(self.output['posts'])
    
    def saveToFile(self, filename):
        if(self.output is None):
            raise Exception("should request first")
        with open(filename, 'w') as outfile:
            json.dump(self.output, outfile)
            outfile.close()
            
    def loadJson(self, filename):
        with open(filename, 'r') as infile:
            self.output = json.load(infile)
            infile.close()
    
    def getNextBatch(self):
        if(self.output is None or webhoseio is None):
            raise Exception("should request first")
        self.output = webhoseio.get_next()
        return self.output
    
    def getTitle(self, postNum):
        if(self.output is None):
            raise Exception("should request first")
        return self.output['posts'][postNum]['title']
    
    def getText(self, postNum):
        if(self.output is None):
            raise Exception("should request first")
        return self.output['posts'][postNum]['text']
    
    def getAuthor(self, postNum):
        if(self.output is None):
            raise Exception("should request first")
        return self.output['posts'][postNum]['author']
    
    def getPubTime(self,postNum):
        if(self.output is None):
            raise Exception("should request first")
        timestamp = self.output['posts'][postNum]['published']
        ts = time.strptime(timestamp[:16], "%Y-%m-%dT%H:%M")
        #datetime.utcfromtimestamp(timestamp)
        return time.strftime("%m/%d/%Y", ts)
    
    def getUrl(self,postNum):
        if(self.output is None):
            raise Exception("should request first")
        return self.output['posts'][postNum]['url']
    
    def getImg(self,postNum):
        if(self.output is None):
            raise Exception("should request first")
        return self.output['posts'][postNum]['thread']['main_image']

    def getSite(self,postNum):
        if(self.output is None):
            raise Exception("should request first")
        return self.output['posts'][postNum]['thread']['site']
    
    def getPerform(self,postNum):
        if(self.output is None):
            raise Exception("should request first")
        return self.output['posts'][postNum]['thread']['performance_score']
    

if __name__ == "__main__":
    wh = WebhoseUtil()
    terminated = False
    print("----------------------------------------------------------\nCommands: <cmd> <postnum>\n----------------------------------------------------------")
    while not terminated:
        m = input()
        command = m.split(" ")[0]
        if(command == 'q'):
            terminated = True
            break
        elif(command == 'save'):
            wh.saveToFile('./test_jsons/education.json')
        elif(command == 'req'):
            wh.request("education")
        elif(command == 'title'):
            if(len(m.split(" "))<2):
                print("Missing arg")
                continue
            print(wh.getTitle(int(m.split(" ")[1])))
        elif(command == 'site'):
            if(len(m.split(" "))<2):
                print("Missing arg")
                continue
            print(wh.getSite(int(m.split(" ")[1])))
        elif(command == 'img'):
            if(len(m.split(" "))<2):
                print("Missing arg")
                continue
            print(wh.getImg(int(m.split(" ")[1])))
        elif(command == 'url'):
            if(len(m.split(" "))<2):
                print("Missing arg")
                continue
            print(wh.getUrl(int(m.split(" ")[1])))
        elif(command == 'time'):
            if(len(m.split(" "))<2):
                print("Missing arg")
                continue
            print(wh.getPubTime(int(m.split(" ")[1])))
        elif(command == 'text'):
            if(len(m.split(" "))<2):
                print("Missing arg")
                continue
            print(wh.getText(int(m.split(" ")[1])))
        elif(command == 'author'):
            if(len(m.split(" "))<2):
                print("Missing arg")
                continue
            print(wh.getAuthor(int(m.split(" ")[1])))
        elif(command == 'perf'):
            if(len(m.split(" "))<2):
                print("Missing arg")
                continue
            print(wh.getPerform(int(m.split(" ")[1])))
        elif(command == 'len'):
            print(wh.numOfPosts())
        elif(command == 'next'):
            wh.getNextBatch()
        elif(command == 'load'):
            wh.loadJson('./test_jsons/entertainment.json')
        else:
            pass
