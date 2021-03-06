import pandas as pd
import praw
from sklearn.feature_extraction import DictVectorizer
from dateutil.relativedelta import relativedelta

da=pd.read_csv("Path to the series of names you want to retrieve an information on Reddit")

reddit = praw.Reddit(client_id='my client id',
                     client_secret='my client secret',
                     user_agent='my user agent',
                     username='my username',
                     password='my password')

#to get valid credentials, you should go to https://www.reddit.com/prefs/apps/, login or create new account on reddit and then create an application of appropriate type. For data mining purposes the simples private script application is goon enough

#With the following I will get some information for every name I have in da series
authors=[]
m=0
for l in da:
    authors.append(dict())
    #to get 100 most commented posts with l mentioned
    al=reddit.get("/r/subreddits/search.json?q="+l+"%20ICO&sort=comments&limit=100&order=desc")
    for i in al:
        try:
            k=i.author.name
# k stores author name; look for other information i contains with dir()
            try:
# if author already exists in dictionary related to theme l - increment count of comments by comments to this article:
                authors[m][k]+=i.num_comments
            except:
#otherwise just create author record with number of comments as comments' count
                authors[m].update({k:i.num_comments})
        except:
            pass
    m+=1

#create sparse dataframe in pandas, using the information we just obtained:
met=DictVectorizer(sparse=False)
auth=met.fit_transform(authors)
auth=pd.DataFrame(data=auth,columns=met.feature_names_)

auth.to_csv("Put your address here",index=False,encoding="utf-8")
