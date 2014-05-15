import HTMLParser, urllib2

class NHLRealtimeParser(HTMLParser.HTMLParser):
        def __init__(self):
                HTMLParser.HTMLParser.__init__(self)
		self.players = []
		self.goalies = []

        def handle_starttag(self, tag, attributes):
                print "1"

        def handle_data(self, data):
                print "2"

        def handle_endtag(self, tag):
                print "3"

url = "http://www.nhl.com/ice/boxscore.htm?id=2012020676"
response = urllib2.urlopen(url)
html = response.read()
p = NHLRealtimeParser()
p.feed(html)
print p.players
print p.goalies
