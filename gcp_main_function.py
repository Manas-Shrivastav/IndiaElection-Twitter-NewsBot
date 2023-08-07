import base64
import pandas as pd
import openai
import tweepy
import csv
import requests
import random
import logging
# Triggered from a message on a Cloud Pub/Sub topic.
#@functions_framework.cloud_event
def post_tweet(event, context):
    # Set API Keys and Authentification
    twitter_api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    twitter_api_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    bearer_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    twitter_access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    twitter_access__secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    logging.info('Setting NewsAPI API Key')
    NEWSAPI_API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # replace with own API key

    logging.info('Setting OpenAI API Key')
    openai.api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # replace with own API key

    logging.info('Setting Twitter API Key')
    client= tweepy.Client(bearer_token, twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access__secret)
    auth=tweepy.OAuth1UserHandler(twitter_api_key, twitter_api_secret,
                                  twitter_access_token, twitter_access__secret)
    auth.set_access_token(twitter_access_token,
                          twitter_access__secret)
    twitter_api=tweepy.API(auth)

    CSV_NAME = 'news_log.csv'
    CSV_FACTS_NAME = 'fact_tweets.csv'
    CSV_NEWS_NAME = 'tweeted_news_articles.csv'


    #### NewsAPI
    def fetch_news(number=10):
        # Fetch tech news from NewsAPI
        url = f"https://newsapi.org/v2/everything?q=bjp&sortBy=publishedAt&apiKey={NEWSAPI_API_KEY}"
        response = requests.get(url).json()
        news_items = response["articles"]
        df = pd.DataFrame(news_items)
        df = df[["title", "description", "url"]].dropna()
        return df.head(number)



    #### OpenAI Engine
    def openai_request(instructions, task, sample = [], model_engine='gpt-3.5-turbo'):
        prompt = [{"role": "system", "content": instructions },
                  {"role": "user", "content": task }]
        prompt = sample + prompt
        completion = openai.ChatCompletion.create(model=model_engine, messages=prompt, temperature=0.2, max_tokens=400)
        return completion.choices[0].message.content


    #### Define OpenAI Prompt for news Relevance
    def select_relevant_news_prompt(news_articles, topics, n):
        instructions = f'Your task is to examine a list of News and return a list of boolean values that indicate which of the News are in scope of a list of topics. \
        Return a list of True or False values that indicate the relevance of the News.'
        task =  f"{news_articles} /n {topics}?"
        sample = [
            {"role": "user", "content": f"[New survey predicts major shift in voting patterns, Election Commission announces poll dates, Key candidates' debate on national television, Prominent party releases election manifesto] /n {topics}?"},
            {"role": "assistant", "content": "[True, True, True, True]"},
            {"role": "user", "content": f"[Famous actor enters the political race, Rumors of election rigging emerge, Candidate caught in a controversy, Sports star campaigns for a political party] /n {topics}?"},
            {"role": "assistant", "content": "[False, True, True, True]"},
            {"role": "user", "content": f"[New restaurant opens in the city, Unemployment rate drops, International trade agreements signed, Weather forecast for election day] /n {topics}?"},
            {"role": "assistant", "content": "[False, False, False, False]"},
            {"role": "user", "content": f"[Opposition Protests Short Duration Discussion on Manipur in Rajya Sabha Without Modi’s Presence, Party leaders attend religious event, Famous singer endorses a candidate, Sports championship held in the country, Launch of new mobile app] /n {topics}?"},
            {"role": "assistant", "content": "[True, False, False, False, False]"},]
        return instructions, task, sample


    #### Define OpenAI Prompt for news Relevance
    def check_previous_posts_prompt(title, old_posts):
        instructions = f'Your objective is to compare a news title with a list of previous news and determine whether it covers a similar topic that was already covered by a previous title. \
            Rate the overlap on a scale between 1 and 10 with 1 being a full overlap and 10 representing an unrelated topic. "'
        task =  f"'{title}.' Previous News: {old_posts}."
        sample = [
            {"role": "user", "content": "'Modi announces 2024 election campaign.' Previous News: [2024 election campaign announced by Modi, Modi's popularity ratings hit all-time high, Rahul Gandhi's popularity ratings plummet, Congress party in disarray]."},
            {"role": "assistant", "content": "1"},
            {"role": "user", "content": "'Opposition announces INDIA(an opposition unity) for 2024 election campaign.' Previous News: [2024 election campaign announced by Opposition, Modi's popularity ratings hit all-time high, Rahul Gandhi's popularity ratings plummet, Congress party in disarray]."},
            {"role": "assistant", "content": "2"},
            {"role": "user", "content": "'TMC win Bengal municipal elections with landslide victory.' Previous News: [Mamta Banerjee's popularity ratings surge, TMC party in good shape, BJP party in trouble]."},
            {"role": "assistant", "content": "5"},
            {"role": "user", "content": "'Kejriwal launches new anti-corruption campaign.' Previous News: [Kejriwal's popularity ratings surge, AAP party in good shape, BJP party in trouble]."},
            {"role": "assistant", "content": "9"},
            {"role": "user", "content": "'Yogi Adityanath unveils new economic plan.' Previous News : [Yogi Adityanath's popularity ratings rise, BJP party in good shape, Congress party in trouble]."},
            {"role": "assistant", "content": "7"},
            {"role": "user", "content": "'Priyanka Gandhi Vadra tours Uttar Pradesh.' Previous News : [Priyanka Gandhi Vadra's popularity ratings rise, Congress party in good shape, BJP party in trouble]."},
            {"role": "assistant", "content": "6"},
            {"role": "user", "content": "'Foxconn end joint venture with Vedanta for semiconductor plant .' Previous News : [Modi's popularity ratings decline, BJP party in trouble, Congress party in good shape]."},
            {"role": "assistant", "content": "10"}]
        return instructions, task, sample


    #### Define OpenAI Prompt for News Tweet
    def create_tweet_prompt(title, description, tiny_url):
        instructions = f'You are a twitter user that creates tweets with a maximum length of 280 characters.'
        task = f"Create an informative tweet on twitter with a satirical tone based on the following news title and description. \
            The tweet must use a maximum of 280 characters. \
            Include the {tiny_url}. But do not include any other urls.\
            Title: {title}. \
            Description: {description}. \
            Use hashtags to reach a wider audience. \
            Do not include any emojis in the tweet"
        return instructions, task


    #### Define OpenAI Prompt for news Relevance
    def previous_post_check(title, old_posts):
        if not old_posts:
              return 5
        instructions, task, sample = check_previous_posts_prompt(title, old_posts)
        response = openai_request(instructions, task, sample)
        return eval(response)


    #### Define OpenAI Prompt for News Tweet
    def create_fact_tweet_prompt(old_terms):
        instructions = f'You are a twitter user that creates tweets with a length below 280 characters.'
        task = f"Choose a  term from the field of Indian politics, election, political party or Indian government. Then create a twitter tweet that describes the term. Just return a python dictionary with the term and the tweet. "
        # if old terms not empty
        if old_terms != []:
            avoid_terms =f'Avoid the following terms, because you have previously tweetet about them: {old_terms}'
            task = task + avoid_terms
        sample = [
            {"role": "user", "content": f"Choose a technical term from the field of Indian politics, election, political party or Indian government. Then create a twitter tweet that describes the term. Just return a python dictionary with the term and the tweet."},
            {"role": "assistant", "content": "{'Vote bank': '#Vote bank is a group of voters who are likely to vote for a particular party or candidate. \
            Vote banks are often formed along religious, caste, or regional lines. #IndianElections2024'}"}]
        return instructions, task, sample

    # Load previous information from a csv file
    def get_history_from_csv(csv_name):
        try:
            # try loading the csv file
            df = pd.read_csv(csv_name)
        except:
            # create the csv file
            df = pd.DataFrame(columns=['title'])
            df.to_csv(csv_name, index=False)
        return df


    
    def check_tweet_length(tweet):
        return False if len(tweet) > 280 else True


    # Create the fact tweet
    def create_fact_tweet(chance_for_tweet = 0.5):
        df_old_facts = get_history_from_csv(CSV_FACTS_NAME)

        if random.random() < chance_for_tweet:
            # create a fact tweet
            instructions, tasks, sample = create_fact_tweet_prompt(list(df_old_facts.tail(10)['title']))
            tweet = openai_request(instructions, tasks, sample)
            tweet_text = list(eval(tweet).values())[0]

            # tweet creation
            print(f'Creating fact tweet: {tweet_text}')

            # check tweet length and post tweet
            if check_tweet_length(tweet):
                client.create_tweet(text=tweet_text)
                #twitter_api().return_status(tweet_text)
                term = list(eval(tweet).keys())[0]
                # save the fact in the csv file
                with open(f'{CSV_FACTS_NAME}', 'a', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([term])
            else:
                print('error tweet too long')
        else:
            print('No fact tweet created')

    def create_news_tweet(title, description, url):
        # create tiny url
        tiny_url = create_tiny_url(url)
        # define prompt for tweet creation
        instructions, task = create_tweet_prompt(title, description, tiny_url)
        tweet_text = openai_request(instructions, task)
        print(f'Creating new tweet: {tweet_text}')
        # check tweet length and post tweet
        if check_tweet_length(tweet_text):
            status = client.create_tweet(text=tweet_text)
            #status = twitter_api.update_status(tweet_text)
            print(f"Tweeted: {title}")
            with open(f'{CSV_NEWS_NAME}', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([title])
        else:
            status = 'error tweet too long'
        return status
    
    def create_tiny_url(url):
        response = requests.get(f'http://tinyurl.com/api-create.php?url={url}')
        return response.text



    #### Main Bot
    def main_bot():
        # Read the old CSV data
        # try opening the csv file and create it if it does not exist
        df_old_news = get_history_from_csv(CSV_NEWS_NAME)
        df_old_news = df_old_news.tail(16)
        # Fetch news data
        df = fetch_news()


        # Check the Relevance of the News and Filter those not relevant
        relevant_topics ="[Indian politics, election, Indian government, general election, BJP, modi, rahul gandhi, Congress, Lok Sabha Elections, politics, political party, citizens, voters]"
        instructions, task, sample = select_relevant_news_prompt(list(df['title']), relevant_topics, len(df))
        relevance = openai_request(instructions, task, sample)
        relevance_list = eval(relevance)
        # Ensure the lengths match by truncating or padding relevance_list
        relevance_list = relevance_list[:len(df)] + [False] * (len(df) - len(relevance_list))
    
        s = 0
        df = df[relevance_list]


        print(df.columns)
        print("Number of news articles fetched:", len(df))
        #print("Number of relevant news articles:", len(df[df['relevance']]))
        if len(df) > 0:
            for index, row in df.iterrows():
                if s == 1:
                    break
                logging.info('info:' + row['title'])
                title = row['title']
                title = title.replace("'", "")
                description = row['description']
                url = row['url']

                if (title not in df_old_news.title.values):
                    doublicate_check = previous_post_check(title, list(df_old_news.tail(10)['title']))
                    if doublicate_check > 3:
                        # Create a tweet
                        response = create_news_tweet(title, description, url)

                    else:
                        print(f"Already tweeted: {title}")
                else:
                    print("No news articles found")
                    create_fact_tweet(chance_for_tweet=0.5)

    print("Starting the bot...")
    main_bot()
    print("Bot execution completed.")