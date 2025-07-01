import tweepy
import schedule 
import time
from datetime import datetime
import os 
import google.generativeai as genai
import requests
from PIL import Image # Pillow library for image manipulation
from io import BytesIO # To handle image data in memory before saving
import random # To pick a random image from Pexels search results

# Twitter credentials
api_key = "WVQHfKDC5K1F888sYCaIVAX3s"
api_secret = "78gXUcLxAhMtzOClKYkoWXTiFzEmNjqAZDZoLiWbIPnnItRDRU"
access_token = "1884495059837755392-G27kL0XiDqllhwbHfAV5HXShGLSZSv"
access_token_secret = "aAhI5JgRJluIfpml8NmrmLaWjwgMgCSmt8N8MEfxjZP2R"

# Gemini API key
gemini_api_key = "AIzaSyBJ714Ns8afSyKjmZF2olDxMJ0wMZiCpwU"
genai.configure(api_key=gemini_api_key)
pexels_api_key = "yntoI7N5aqEjghTr35NxI8jIVNgP6TnpLOrpyOer7M9zpoX1dfPn3cjP"

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Gemini AI model for text generation
gemini_text_model = genai.GenerativeModel('gemini-1.5-flash')

# Prompts for Gemini AI text generation
# Derive the image search query from the generated text or a related concept.
daily_prompts = [
    {
        "text_prompt": "What animal do you see in this image?",
        "image_keywords_fallback": "lion, savannah, wildlife",
        "poll_options": ["Lion", "Tiger", "Leopard", "Cheetah"]
    },
    {
        "text_prompt": "Which city is shown in this skyline?",
        "image_keywords_fallback": "city skyline, skyscrapers, night",
        "poll_options": ["New York", "London", "Dubai", "Tokyo"]
    },
    {
        "text_prompt": "What season does this scene represent?",
        "image_keywords_fallback": "autumn, leaves, park",
        "poll_options": ["Spring", "Summer", "Autumn", "Winter"]
    },
    {
        "text_prompt": "Which sport is being played in this image?",
        "image_keywords_fallback": "football, stadium, match",
        "poll_options": ["Football", "Basketball", "Tennis", "Cricket"]
    },
    {
        "text_prompt": "What type of food is shown here?",
        "image_keywords_fallback": "pizza, food, cheese",
        "poll_options": ["Pizza", "Burger", "Pasta", "Salad"]
    },
    {
        "text_prompt": "Which mode of transport is this?",
        "image_keywords_fallback": "train, railway, travel",
        "poll_options": ["Train", "Bus", "Car", "Bicycle"]
    },
    {
        "text_prompt": "What time of day is it in this photo?",
        "image_keywords_fallback": "sunset, evening, sky",
        "poll_options": ["Morning", "Afternoon", "Evening", "Night"]
    }
]

#funtion that helps in geberation of images
def generate_image_and_poll_with_gemini():
    prompt = (
        "Generate a JSON object for a Twitter post. "
        "It should have: "
        "'image_keywords' (a comma-separated string of 2-4 keywords for an interesting, general-topic image), "
        "'poll_question' (a short, fun or thought-provoking question about the image), "
        "'poll_options' (a list of 4 short voting options, each max 25 chars, relevant to the image/question). "
        "Do NOT make it motivational. "
        "Example: {\"image_keywords\": \"cat, window, rain\", \"poll_question\": \"What do you think this cat is looking at?\", \"poll_options\": [\"A bird\", \"The rain\", \"A person\", \"Nothing\"]}"
    )
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        import json, re
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            data = json.loads(match.group())
            if (
                "image_keywords" in data and
                "poll_question" in data and
                "poll_options" in data and
                len(data["poll_options"]) == 4
            ):
                return data
    except Exception as e:
        print(f"Error generating with Gemini: {e}")
    # Fallback
    return {
        "image_keywords": "cat, window, rain",
        "poll_question": "What do you think this cat is looking at?",
        "poll_options": ["A bird", "The rain", "A person", "Nothing"]
    }

def search_pexels_image(query):
    """Searches Pexels for an image and returns the URL of a random image."""
    PEXELS_API_URL = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": pexels_api_key
    }
    params = {
        "query": query,
        "per_page": 15, # Request a few images to choose from
        "orientation": "landscape" # Prefer landscape images for Twitter
    }

    try:
        response = requests.get(PEXELS_API_URL, headers=headers, params=params)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        photos = data.get('photos', [])
        if photos:
            # Pick a random photo from the results
            selected_photo = random.choice(photos)
            # You can choose different sizes: original, large, medium, small, portrait, landscape, tiny
    
            return selected_photo['src']['large']
        else:
            print(f"No Pexels images found for query: '{query}'")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from Pexels API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during Pexels search: {e}")
        return None


def download_image(image_url):
    """Downloads an image from a URL and saves it temporarily."""
    if not image_url:
        return None

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        
        image_filename = f"temp_pexels_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        
        # Ensure the image data is actually an image
        if 'content-type' in response.headers and 'image' in response.headers['content-type']:
            with open(image_filename, 'wb') as out_file:
                for chunk in response.iter_content(chunk_size=8192):
                    out_file.write(chunk)
            print(f"Downloaded image to: {image_filename}")
            return image_filename
        else:
            print(f"URL did not return an image: {image_url}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from URL {image_url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during image download: {e}")
        return None

def generate_content_and_image_for_tweet(text_prompt, image_keywords_fallback):
    """Generates text with Gemini and finds an image from Pexels."""
    generated_text = None
    image_path = None
    image_search_query = image_keywords_fallback # Start with fallback

    try:
        # 1. Generate text with Gemini
        text_response = gemini_text_model.generate_content(text_prompt)
        generated_text = text_response.text
        print(f"Generated text: {generated_text[:50]}...")
        
    except Exception as e:
        print(f"Error generating text with Gemini: {e}")
        generated_text = None # Ensure text is None if generation fails

    if generated_text: # Only try to get an image if text generation was successful
        image_url = search_pexels_image(image_search_query)
        if image_url:
            image_path = download_image(image_url)

    return generated_text, image_path

def send_daily_tweet():
    """Generates content with AI, posts to Twitter with an image, and cleans up."""
    weekday = datetime.now().weekday()
    current_day_prompts = daily_prompts[weekday % len(daily_prompts)]

    # Debugging print to confirm Pexels key is loaded
    if pexels_api_key:
        print(f"Pexels API Key loaded (first 5 chars): {pexels_api_key[:5]}*")
    else:
        print("Pexels API Key NOT loaded. Check .env file.")

    text, image_path = generate_content_and_image_for_tweet(
        current_day_prompts["text_prompt"],
        current_day_prompts["image_keywords_fallback"]
    )

    if text and image_path:
        try:
            # Upload the image to Twitter
            media = api.media_upload(image_path)
            # Post the tweet with the generated text and attached image
            response = client.create_tweet(text=text, media_ids=[media.media_id])
            print(f"Tweet posted for {datetime.now().strftime('%A')}: {text}")
        except tweepy.TweepyException as e:
            print(f"Error posting tweet with image: {e}")
        finally:
            # Clean up the temporary image file
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"Cleaned up temporary image: {image_path}")
    elif text: # Post text only if image generation failed but text succeeded
        try:
            response = client.create_tweet(text=text)
            print(f"Tweet posted (text only) for {datetime.now().strftime('%A')}: {text}")
        except tweepy.TweepyException as e:
            print(f"Error posting text-only tweet: {e}")
    else:
        print(f"Skipping tweet for {datetime.now().strftime('%A')} due to content generation failure.")

def send_ai_generated_image_and_poll():
    data = generate_image_and_poll_with_gemini()
    image_keywords = data["image_keywords"]
    poll_question = data["poll_question"]
    poll_options = data["poll_options"]

    # 1. Get image from Pexels
    image_url = search_pexels_image(image_keywords)
    image_path = download_image(image_url) if image_url else None

    # 2. Post image tweet
    if image_path:
        try:
            media = api.media_upload(image_path)
            image_tweet = client.create_tweet(text="", media_ids=[media.media_id])
            image_tweet_id = image_tweet.data["id"]
            print("Image posted.")
        except Exception as e:
            print(f"Error posting image: {e}")
            image_tweet_id = None
        finally:
            if os.path.exists(image_path):
                os.remove(image_path)
    else:
        image_tweet_id = None

    # 3. Post poll as a reply to the image tweet (or as a standalone if image failed)
    try:
        poll_response = client.create_tweet(
            text=poll_question,
            poll_options=poll_options,
            poll_duration_minutes=1440,
            in_reply_to_tweet_id=image_tweet_id if image_tweet_id else None
        )
        print("Poll posted:", poll_question)
        print("Options:", poll_options)
    except Exception as e:
        print(f"Error posting poll: {e}")


# Schedule the tweet to be sent every day at your specified time in EAT (Kampala timezone)
schedule.every().day.at("07:45").do(send_daily_tweet)
print(f"Arthur's_x_bot is running and will tweet(X) every day at 07:45 PM EAT (current time: {datetime.now().strftime('%I:%M %p %Z')}).")
while True:
    schedule.run_pending()
    time.sleep(60)