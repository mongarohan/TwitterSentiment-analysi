import tweepy                        #twitter library for twitter API
from textblob import TextBlob            #library to process textual data
import sys
import csv
import matplotlib.pyplot as plt             #for plotting graph
from PyQt5 import QtCore, QtGui, QtWidgets      #for GUI
from imgGen import gen                   #second script

'''
to convert ui in xml format to python script: pyuic5 -x <filename.ui> -o <filename.py>
'''
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(720, 423)
        Form.setStyleSheet("background-image: url(colorful-line-on-black-background.jpg);")
        self.title = QtWidgets.QLabel(Form)
        self.title.setGeometry(QtCore.QRect(180, 20, 611, 61))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.desc = QtWidgets.QLabel(Form)
        self.desc.setGeometry(QtCore.QRect(80, 100, 581, 211))
        self.desc.setMinimumSize(QtCore.QSize(351, 141))
        font = QtGui.QFont()
        font.setFamily("Sitka Small")
        font.setPointSize(15)
        self.desc.setFont(font)
        self.desc.setObjectName("desc")
        self.b1 = QtWidgets.QPushButton(Form)
        self.b1.setGeometry(QtCore.QRect(190, 350, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.b1.setFont(font)
        self.b1.setAutoFillBackground(False)
        self.b1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(255, 255, 255);")
        self.b1.clicked.connect(gen)              #connected function from second script ie. imgGen.py
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("trending_up_white_192x192.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b1.setIcon(icon)
        self.b1.setAutoRepeatInterval(100)
        self.b1.setObjectName("b1")
        self.b1_2 = QtWidgets.QPushButton(Form)
        self.b1_2.setGeometry(QtCore.QRect(440, 350, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.b1_2.setFont(font)
        self.b1_2.setStyleSheet("color: rgb(255, 255, 255);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("search-3-xxl.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b1_2.setIcon(icon1)
        self.b1_2.setObjectName("b1_2")
        self.b1_2.clicked.connect(self.showNameDialog)          #to show input dialogue box
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(100, 20, 55, 51))
        self.label.setStyleSheet("image: url(Icon_Twitter.png);")
        self.label.setText("")
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def showNameDialog(self):
        topic, ok = QtWidgets.QInputDialog.getText(None, 'Topic', 'Enter the Topic:')
        self.generate(topic)           #to get input from user and save it in topic variable for later use
        print(ok)

    def generate(self,topic):
        '''
        keys are provided by twitter after registration of app on their portal
        '''
        consumer_key= ''
        consumer_secret= ''

        access_token=''
        access_token_secret=''

        #authenticating
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)
        #giving topics to access tweets by default 15 tweets are accessed
        public_tweets = api.search(topic)

        with open('sentiment.csv', 'a', newline='\n') as  f:
        	writer = csv.DictWriter(f, fieldnames=['Tweet', 'Sentiment', 'polarity', 'subjectivity'])    #setting header to csv
        	writer.writeheader()
        	p_count, nu_count, n_count= 0,0,0
        	for tweet in public_tweets:
        		foo = tweet.text.encode('utf-8').strip()         #encoding is important to avoid any conflicts as not all tweets are in utf-8

                #Cleaning tweet
        		#cleanedtext = "".join([word for word in text.split(' ') if len(word) > 0 and word[0] != '@' and word[0] != '#' and 'http' not in word and word != 'RT'])
                #not needed as textblob cleans text inbuilt

        		analysis = TextBlob(tweet.text)
        		sub = analysis.sentiment.subjectivity
        		sentiment = analysis.sentiment.polarity

        		if sentiment > 0:
        			polarity = 'Positive'
        			p_count = p_count+1
        		elif sentiment == 0:
        			polarity = 'neutral'
        			nu_count = nu_count+1
        		else:
        			polarity = 'Negative'
        			n_count = n_count+1


        		#insert into csv(cleanedtext, sentiment, polarity, subjectivity)

        		writer.writerow({'Tweet':foo, 'Sentiment':polarity, 'polarity':sentiment, 'subjectivity': sub})



        #plotting line graph for polarity (range:-1 to 1)
        with open('sentiment.csv', 'r') as f:
            data = list(csv.reader(f))
        plt.close('all')
        pol = [i[2] for i in data[1::]]
        f, ax = plt.subplots()
        ax.plot(range(len(pol)), pol)
        ax.set_title('Polarity')
        f.savefig('polarity.png')

        #plotting linegraph for subjectivity(range:0 to 1)
        sub = [i[3] for i in data[1::]]
        f1, ax0 = plt.subplots()
        ax0.plot(range(len(sub)), sub)
        ax0.set_title('Subjectivity')
        f1.savefig('subjectivity.png')

        #plotting pie chart
        labels = 'negative', 'positive', 'neutral'
        sizes = [p_count, nu_count, n_count]
        explode = (0.1, 0, 0)
        f2, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        ax1.set_title('sentiment')
        f2.savefig('sentiment.png')

        plt.show()       # to display all 3 plotted graphs



    #part of ui formatting
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.title.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ffffff;\">Twitter Sentiment Analysis</span></p></body></html>"))
        self.desc.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">Discover </span><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#ffffff;\">game-changing insights</span><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\"> within the billions of</span></p><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">conversations happening online every day.</span></p><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">Twitter sentiment Analysis tells you more about the topics,</span></p><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#ffffff;\">trends</span><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\"> and</span><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#ffffff;\"> people</span><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\"> impacting the world</span></p></body></html>"))
        self.b1.setText(_translate("Form", "Trending"))
        self.b1_2.setText(_translate("Form", "Search"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
