from NHLSummaryParser import NHLSummaryParser
import urllib2

url = "http://www.nhl.com/scores/htmlreports/20132014/GS020378.HTM"
response = urllib2.urlopen(url)
html = response.read()

p = NHLSummaryParser()
p.feed(html)
print html

print p.summary_data
for x in p.goal_data:
	print x
for x in p.away_penalty_data:
	print x
for x in p.home_penalty_data:
	print x
for x in p.period_data:
	print x
for x in p.goalie_data:
	print x
for x in p.stars_data:
	print x
