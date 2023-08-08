# IndiaElection-Twitter-NewsBot
As the 2024 General Elections in India draw near, the need for accurate, real-time information has never been more critical. Imagine having a dedicated ally that not only keeps you abreast of the latest political developments but also engages you in insightful conversations and delivers news with a dash of wit. Enter our project – the 2024 India Elections NewsBot (Powered by ChatGPT and NewsAPI).

# Step 1: Set Up a [Twitter Developer Account](https://developer.twitter.com/en/docs/developer-portal/overview)

Create a New account [Twitter Developer Account](https://developer.twitter.com/): Visit the Twitter Developer Platform and create an account if you don't have one.

Create a New [Twitter App](https://developer.twitter.com/apps): After logging in, create a new Twitter App. This will generate API keys and access tokens required for authentication.

Retrieve [API Keys and Tokens](https://developer.twitter.com/en/docs/authentication/oauth-1-0a/api-key-and-secret): In the "Keys and Tokens" section of your Twitter App, you'll find your API Key, API Secret Key, Access Token, and Access Token Secret. These are essential for authentication.

# Step 2: Set Up an OpenAI Account

Create an [OpenAI Account](https://auth0.openai.com/u/signup/identifier?state=hKFo2SBUS3NnYTFjQnUtRVZ0WDV0SlpPU3VaSHcycjBkbHl1QaFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIE9hR2NuVXJaT3JkeWlEampQRGJzd2Q5eU1zbHowWnJIo2NpZNkgRFJpdnNubTJNdTQyVDNLT3BxZHR3QjNOWXZpSFl6d0Q): Head to the OpenAI website and create an account if you haven't already.

Retrieve Your [API Key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key): In your OpenAI account settings, locate your API key. This key is used to interact with the OpenAI GPT-3 API.

Please note that to access OpenAI's developer features, you'll need to provide your card details. The cost for running the bot is approximately $0.05 per day, depending on the assigned tasks.

# Step 3: Set Up a NewsAPI Account

Create a [NewsAPI Account](https://newsapi.org/register): Go to the NewsAPI website and register for an account.

Obtain Your API Key: Upon registration, you'll receive an API key. This key allows you to fetch news data from the NewsAPI.

# Step 4: Set Up [Tweepy](https://www.tweepy.org/) and Other Dependencies

Install Required Dependencies: Use the command pip install pandas openai tweepy requests to install the necessary Python packages.

# Step 5: Implement the Code

After setting up the prerequisites, refer to the `newsbot.py` file to understand how the bot is built and its workflow.

# Step 6: Testing and Execution

Test the Bot Locally: Before deployment, run your bot locally to ensure it functions correctly. Execute the [Python script](https://colab.google/) to verify that the bot interacts with APIs and generates tweets accurately.

# Step 7: Set Up Cloud Functions (Optional)

Create a Cloud Function: If you wish to automate your bot, you can use cloud platforms like [Google Cloud Functions](https://cloud.google.com/functions/) or [AWS Lambda](https://aws.amazon.com/lambda/). Deploy your code on the chosen platform. We have used GCP, and for that you will have to create an account and provide card details to google and then you’ll receive a 3 month trial period, after that if you wish to continue, google will charge. 

You refer and edit the gcp_main_function.py and requirements.txt files according to your code.

Additionally, you can configure Environment Variables by safely storing your API keys and tokens as environment variables within the cloud platform.

# Step 8: Schedule Bot Execution

Set Up Scheduled Execution: To automate regular bot updates, configure a scheduler such as Cron jobs or a [cloud platform scheduler](https://www.cloudthat.com/resources/blog/scheduling-cloud-functions-using-gcp-cloud-scheduler#:~:text=Cloud%20Scheduler%20is%20a%20fully%20managed%20service%20in,of%20tasks%2C%20eliminating%20the%20need%20for%20manual%20intervention.). This ensures your bot runs at specific intervals.

For detailed instructions on deploying your Twitter bot on Google Cloud Platform (GCP) and scheduling tweets, refer to this video "[Simple Twitter Bot With Python Tutorial](https://www.youtube.com/watch?v=83o6rU5XArs&t=1403s)".

# Step 9: Monitor and Maintain

Monitor and Troubleshoot: Regularly review the bot's logs for errors or issues. Observe its performance to ensure smooth operation.

Maintain and Update: Periodically update the bot's code, prompts, or features based on user feedback and changing needs.

By following these comprehensive steps, you'll successfully set up and deploy your own Twitter bot using the provided code. Document your repository with clear instructions so that others can replicate your bot creation process.

