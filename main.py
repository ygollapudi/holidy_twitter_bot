import tweepy
from datetime import datetime, date
#from secret import consumer_key, consumer_secret, access_token, access_secret removes for security

handle = 'YashGollapudi'

# get authentication info
client = tweepy.Client( bearer_token=bearer,
                        consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token=access_token,
                        access_token_secret=access_secret)
# client = tweepy.Client(bearer)
#auth.set_access_token(access_token, access_secret)
auth = tweepy.OAuth2BearerHandler(bearer)
# log into the API
api = tweepy.API(auth)
print('[{}] Logged into Twitter API as @{}\n-----------'.format(
    datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
    handle
))

# string array of words that will trigger the on_status function
trigger_words = [
    '@' + handle # respond to @mentions,
]

# override the default listener to add code to on_status
class MyStreamListener(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        # log the incoming tweet
        # incoming tweet was What is the latest in " "
        holidays={1:[[1,"New year"],[18,"Marlin Luther King Jr"]],
            5: [31,"Memorial"],
            6: [4,"Independence"],
            9: [6,"Labour"],
            11: [[11,"Veterans"],[25,"Thanksgiving"]],
            12: [[24,"Christmas"],[31,"New Year"]]
            }

        usr = str(client.get_tweet(tweet.data['id'], expansions=['author_id'], user_fields=['username']).includes).split('=')[3].split('>')[0]
        if usr == 'YashGollapudi':
            return
        print('[{}] Received: "{}" from @{}'.format(
            datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
            tweet.text,
            usr

        ))

        dat=str(date.today())
        #dat="2021-11-1"
        time1=365
        event=" b day"
        date_now=dat.split("-")
        if int(date_now[1]) in holidays.keys():
            options=holidays[int(date_now[1])]
            for k in options:
                if int(date_now[2])<k[0]:
                    time1 = k[0]-int(date_now[2])
                    event = k[1]
            if event ==" b day":
                time1=30-int(date_now[2])
                d_now=int(date_now[1])+1
                while d_now not in holidays.keys():
                    time1+=30
                    d_now+=1
                el =holidays[d_now]
                for e in el:
                    if isinstance(e,list):
                        event=e[1]
                        time1+=int(e[0])
                        break
                    else:
                        if isinstance(e,int):
                            time1+=int(e)
                        event=e
        else:
            time1=30-int(date_now[2])
            d_now=int(date_now[1])+1
            while d_now not in holidays.keys():
                time1+=30
                d_now+=1
            el =holidays[d_now]
            for e in el:
                if isinstance(e,list):
                    event=e[1]
                    time1+=int(e[0])
                    break
                else:
                    if isinstance(e,int):
                        time1+=int(e)
                    event=e



        responseText = '@'+ usr + " Next Holiday is about "+ str(time1) +" days away and it is the " + event +" day"
        response = client.create_tweet(
            text=responseText,
            in_reply_to_tweet_id=tweet.data['id']
        )
        print('[{}] Responded to @{} with {} day'.format(
            datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
            usr,event
        ))
        return


# create a stream to receive tweets
try:
    # streamListener = MyStreamListener(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token= access_token, access_token_secret=access_secret)
    # stream = tweepy.Stream(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token= access_token, access_token_secret=access_secret)
    # stream.filter(track=trigger_words)
    twitter_stream = MyStreamListener(bearer_token=bearer)
    twitter_stream.add_rules(tweepy.StreamRule(trigger_words[0]))
    twitter_stream.filter()
except KeyboardInterrupt:
    print('\nGoodbye')


