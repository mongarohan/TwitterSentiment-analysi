import urllib.request			# to acces any website
import cv2						#opencv library for computer vision
import numpy as np				#library for scientific computation
from bs4 import BeautifulSoup	#library to pull data from xml and html files
from random import randint
import math
import operator
import time
from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt



def gen():
	#function to return avg sentiment(polarity)
	def getSentiment(api, key):
		public_tweets = api.search(key)
		AvgSentiment = 0
		noOfTweets = len(public_tweets)
		sum1 = 0
		for tweet in public_tweets:
			text = tweet.text
			#cleanedtext = ' '.join([word for word in text.split(' ') if len(word) > 0 and word[0] != '@' and word[0] != '#' and 'http' not in word and word != 'RT'])
			#print(cleanedtext)
			analysis = TextBlob(text)
			sentiment = analysis.sentiment.polarity
			sum1 += sentiment

			if sentiment == 0:
				#ignore since not a opinion, its a general statement
				noOfTweets -= 1
		if noOfTweets > 0:
			AvgSentiment = sum1/noOfTweets
		return AvgSentiment

	def getxy(coordinates,raduis):					#to get non overlapping coordinates
		x2 = 0
		y2 = 0
		while True:						#loop iteration which runs until finding a circle which doesnt intersect with previous ones
			x2 = randint(2*radius,width-radius)			#getting random coordinates
			y2 = randint(2*radius,height-radius)
			flag = 0								#Flag which holds true whenever a new circle was found
			for key, value in coordinates.items():
				x1 = int(key.split()[0])
				y1 = int(key.split()[1])
				ans = math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))		#calculates distances from previous drawn circles
				if ans < value + radius+50:
					flag = 1													# if the distance is not to small - adds the new circle to the list
					break
			if flag == 0:
				break
		return x2, y2

	def drawOnImage(img, radius, AvgSentiment, key):
		#circle(img,coordinate,BGR,thickness)
		img = cv2.circle(img,(x,y), radius, (0, 127.5+(AvgSentiment*127.5), 127.5+(AvgSentiment*-127.5)), -1)		#to generate cirle for each key with its color maipulated
		font = cv2.FONT_HERSHEY_PLAIN
		string = key
		#coordinates.append(str(x)+" "+str(y)+" "+key)
		#putText(img,text,coordinates,font, font scale,BGR, thickness,line type)
		cv2.putText(img,string,(x-8*len(string)-5,y), font, 2,(255,255,255),2,cv2.LINE_AA)
		string = str(value)+'+'
		cv2.putText(img,string,(x-8*len(string)-5,y+40), font, 2,(255,255,255),2,cv2.LINE_AA)
		return img

	#authenticating to twitter
	consumer_key= 'AkRmo6wpXHoxeTQ2HWD6ASpaR'
	consumer_secret= '4DnZKUcfewfvqRqKQsjzbIved5S2mp1KsaaLeIr4NFUiam2Imi'

	access_token='869627589865766912-4Jb7jlGRGN3EZKb8NKOz5dv4HougcP9'
	access_token_secret='m84ro1geHgbYduoWfQkIet4YXKynUkjArng4dZss5uiYF'

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	#Query the website and return the html to the variable 'url'
	url=urllib.request.urlopen("http://www.google.com/trends/hottrends/atom/feed").read().decode("utf-8")

	#Parse the html in the 'page' variable, and store it in Beautiful Soup format
	soup=BeautifulSoup(url, features="xml")
	title = []
	#to get all trending topics
	for element in soup.find_all('title'):
		#print(element.string)
		if element.string == "Hot Trends":
			continue
		title.append(element.string)
	#to get views on each title
	views = []
	for element in soup.find_all('approx_traffic'):
		view = element.string.replace(',','')
		view = view.strip('+')
		views.append(int(view))


	#saving titles and views in a dictionary called trends
	i = 0
	trends = dict()
	for element in title:
		trends[element] = views[i]
		i += 1

	#generating black background for image
	height = 2280
	width = 3120
	img = np.zeros((height,width,3), np.uint8)		#np.zero sets BGR 3 dim array as zero giving black background

	sum = 0
	for view in views:
		sum = sum + view
	trends = sorted(trends.items(), key=operator.itemgetter(1))  #sorting on the base of views
	trends = dict(trends)
	coordinates = dict()
	flag = 0
	for key, value in trends.items():
		radius = int(float(value)/float(sum)*250+100)			#to get varied radius length according to views

		AvgSentiment = getSentiment(api, key)				#calling function from above
		print(key, AvgSentiment)

		if flag == 0:					#generating first coordinate for circle
			x = randint(2*radius,width-radius)
			y = randint(2*radius,height-radius)
			coordinates[str(x)+" "+str(y)] = radius
			flag = 1
		elif flag == 1:					#generating not first coordinate
			x,y = getxy(coordinates, radius)
			coordinates[str(x)+" "+str(y)] = radius				#saved as coordinate[x y]

		img = drawOnImage(img, radius, AvgSentiment, key)			#calling function from above

	imgname = "./"+str(time.strftime("%d%m%Y"))+".png" 		#name generated on current date
	print(imgname)
	cv2.imwrite(imgname,img)
