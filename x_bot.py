import tweepy
import schedule
import time
from datetime import datetime

# Twitter credentials
api_key = "WVQHfKDC5K1F888sYCaIVAX3s"
api_secret = "78gXUcLxAhMtzOClKYkoWXTiFzEmNjqAZDZoLiWbIPnnItRDRU"
access_token = "1884495059837755392-G27kL0XiDqllhwbHfAV5HXShGLSZSv"
access_token_secret = "aAhI5JgRJluIfpml8NmrmLaWjwgMgCSmt8N8MEfxjZP2R"

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# List of tweets for each day (add as many as you want)
tweets = [
    "🌞 Good afternoon, world! 🌅 A brand new week is here, filled with possibilities. Let today be the start of something great.\nSmile, set your intentions, and take that first step toward your goals. You’ve got this! 💪 #MondayMotivation #NewBeginnings",

    "🚀 Progress isn’t always loud—sometimes it’s just showing up and trying again.\nEvery step forward, no matter how small, matters. Keep moving, stay focused, and trust that your journey is leading somewhere beautiful. #TuesdayThoughts #KeepGoing",

    "🌱 Challenges are not roadblocks—they're opportunities to grow stronger and wiser.\nEmbrace what tests you, for it shapes you into who you’re meant to be. Keep learning, keep rising. 🌿 #WednesdayWisdom #GrowthMindset",

    "💡 Stay curious, even when things feel routine. Ask questions, explore new ideas, and never stop learning.\nEvery day holds a lesson—if you’re willing to listen. 💡✨ #ThursdayThoughts #LifelongLearning",

    "🎉 You made it through the week—take a moment to appreciate your efforts and your progress.\nCelebrate your wins, big or small, and don’t forget to recharge. You deserve it. 🎉💖 #FridayFeeling #Gratitude",

    "😎 It’s the weekend! Time to relax, unwind, and enjoy the moments that bring you joy.\nWhether it’s adventure or rest, make today about what fills your soul. 😎🌈 #SaturdayVibes #WeekendJoy",

    "📝 Sundays are for slowing down and reflecting. Look back on the week with kindness, learn from it, and set your intentions for what’s next.\nA little planning today brings peace tomorrow. 📖🌙 #SundayReflection #MindfulLiving"
]

def send_daily_tweet():
    # Get the current weekday (0=Monday, 6=Sunday)
    weekday = datetime.now().weekday()
    tweet = tweets[weekday % len(tweets)]
    response = client.create_tweet(text=tweet)
    print(f"Tweet posted for {datetime.now().strftime('%A')}: {tweet}")

# Schedule the tweet to be sent every day at 9:00 AM
schedule.every().day.at("14:45").do(send_daily_tweet)

print("Bot is running and will tweet every day at 2:45PM.")
while True:
    schedule.run_pending()
    time.sleep(60)