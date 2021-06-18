import tweepy
from textblob import TextBlob
import pandas as pd
import re
import matplotlib.pyplot as plt

consumerKey= "MDU0jlllUa4SH01za7ac7PEGU"
consumerSecret= "LVQXLy1dLOGVour75k451nUr1KQb5MyIT7eb0ZCvhOaqY6Fuzv"
accessToken= "1393082152816893952-6gpf005t5zR0aT8LayuYkhbdmseJAY"
accessTokenSecret= "0l7SUcMFfFlE7FmCwhrTmJxoGzAZuIw4zIBTgmEBLa0px"


authenticate = tweepy.OAuthHandler(consumerKey , consumerSecret)
authenticate.set_access_token(accessToken, accessTokenSecret)
api=tweepy.API(authenticate, wait_on_rate_limit = True)

posts = api.user_timeline(screen_name="narendramodi", count= 100, lang= "en", tweet_mode="extended")

df=pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

def cleanTxt(text):
 text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
 text = re.sub('#', '', text) # Removing '#' hash tag
 text = re.sub('RT[\s]+', '', text) # Removing RT
 text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
 
 return text

df['Tweets'] = df['Tweets'].apply(cleanTxt)

def getSubjectivity(text):
   return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
   return  TextBlob(text).sentiment.polarity

df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)

def getAnalysis(score):
 if score < 0:
  return 'Negative'
 elif score == 0:
  return 'Neutral'
 else:
  return 'Positive'

df['Analysis'] = df['Polarity'].apply(getAnalysis)

ptweets = df[df.Analysis == 'Positive']
ptweets = ptweets['Tweets']
ptweets

round( (ptweets.shape[0] / df.shape[0]) * 100 , 1)

ntweets = df[df.Analysis == 'Negative']
ntweets = ntweets['Tweets']
ntweets

round( (ntweets.shape[0] / df.shape[0]) * 100, 1)

df['Analysis'].value_counts()

plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind = 'pie')
plt.show()
