import snscrape.modules.twitter as sntwitter 
from snscrape.modules.twitter import TwitterSearchScraper
import pandas as pd 
import streamlit as st 
import io
import pymongo
import datetime

#import the image
st.image('https://www.bestproxyreviews.com/wp-content/uploads/2020/05/Twitter-scraping.jpg')

#write the subheading
st.subheader("""
        Let's find some tweets to scrape....Hope twitter doesn't mind it! :smile:
        """)

#creating database connection
client = pymongo.MongoClient("mongodb+srv://aisha1818:<password>@cluster0.fj8db6r.mongodb.net/test")
db = client.test
collection = db["tweetercollection"]

#defining a fuctional block ,to scrape the data from twitter 
def fun(search_term,output_csv,file_name,limit):
       query = search_term
       tweet_list=[]
       counter=0
       for tweet in sntwitter.TwitterSearchScraper(query).get_items():
          if counter >= limit:
             break
          else:
             counter += 1  
             tweet_list.append([tweet.date,tweet.content,tweet.user.username,tweet.user.displayname,tweet.id,tweet.replyCount,tweet.retweetCount,tweet.likeCount,tweet.lang,tweet.source,tweet.url])
       df=pd.DataFrame(tweet_list,columns=["Date","content","tweet","username","displayname","Id","replycount","retweetcount","likecount","lang","source"])
       st.table(df)
       if output_csv == 'Yes':
          buffer = io.StringIO()
          df.to_csv(buffer, index=False)
          buffer.seek(0)
          st.write('Downloading file: %s' % file_name)
          st.file_downloader(file_name,buffer.getvalue(), 'text/csv')
       for i, row in df.iterrows():
            data = {"search_term":search_term, "timestamp":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),**row.to_dict()}
            collection.insert_one(data)
       st.success("Data stored in mongoDB!")


#creating the frontend forms using streamlit library
with st.form(key='Twitter_form'):
    search_term=st.text_input("**What do you want to search for?**")
    limit=st.slider("**How many tweets do you want to get?**",1,1000,step=20)
    output_csv=st.radio("**Download csv file?**",['Yes','No'])
    file_name=st.text_input("**Name the csv file:**",max_chars=20)
    submit_button=st.form_submit_button(label='**Search**')

 #if submit button is pressed ,its designed to perform actions: 
try:
    if submit_button:
        fun(search_term,output_csv,file_name,limit)
except Exception as e:
    st.error("Error: " + str(e))   
       
