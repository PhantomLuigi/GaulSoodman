import requests
import lxml.etree
import time
import random
import json

# Global session for maintaining login
main_session = requests.Session()

# Define your login credentials and forum URL
NAME = 'username'
PASS = 'password'
FORUM_URL = 'https://tbgforums.com/forums/'

# Function to log in
def login():
    global main_session
    obtain_login = main_session.get(FORUM_URL + "index.php?action=login")
    hidden_val = lxml.etree.HTML(obtain_login.text.encode()).xpath('//*[@id="frmLogin"]/input')
    form = {"user": NAME, "passwrd": PASS, "cookielength": 31536000}
    for v in hidden_val:
        form[v.get("name")] = v.get("value")
    login_req = main_session.post(
        FORUM_URL + "index.php?action=login2",
        data=form)
    if login_req.status_code == 200:
        print("Login successful")
    else:
        print("Failed to login")
    return login_req.status_code

def load_random_options():
    with open('random_options.json', 'r') as file:
        options = json.load(file)
    return options

# Function to scrape statistics from the forum
def scrape_stats():
    global main_session
    stats_page = main_session.get(FORUM_URL + "index.php?action=stats")
    stats_tree = lxml.etree.HTML(stats_page.text.encode())

    # Extract the desired statistics data
    total_posts_str = stats_tree.xpath('//dt[text()="Total Posts:"]/following-sibling::dd')[0].text.strip()
    total_posts = int(total_posts_str.replace(',', ''))
    total_topics = stats_tree.xpath('//dt[text()="Total Topics:"]/following-sibling::dd')[0].text.strip()
    total_members = stats_tree.xpath('//dt[text()="Total Members:"]/following-sibling::dd/a')[0].text.strip()
    average_posts_per_day = stats_tree.xpath('//dt[text()="Average posts per day:"]/following-sibling::dd')[0].text.strip()

    time.sleep(6)

    main_page = main_session.get(FORUM_URL)
    time.sleep(6)
    main_tree = lxml.etree.HTML(main_page.text.encode())
    
    newest_member_element = main_tree.xpath('//*[@id="upshrink_stats"]/p[1]/strong[1]/a')
    
    if newest_member_element:
        newest_member = newest_member_element[0].text
    else:
        newest_member = "Newest Member not found"

    options = load_random_options()

    tv_show = random.choice(options['tv_show_options'])
    movie = random.choice(options['movie_options'])
    song = random.choice(options['song_options'])
    video_game = random.choice(options['video_game_options'])
    message_of_the_day = random.choice(options['message_of_the_day_options'])
    word_of_the_day = random.choice(options['word_of_the_day_options'])
    ai_image_prompt = random.choice(options['ai_image_prompt_options'])
    total_posts += 1

    total_posts_with_commas = format(total_posts, ',')

    return {
        "total_posts": total_posts_with_commas,
        "total_topics": total_topics,
        "total_members": total_members,
        "average_posts_per_day": average_posts_per_day,
        "newest_member": newest_member,
        "tv_show": tv_show,
        "movie": movie,
        "song": song,
        "video_game": video_game,
        "message_of_the_day": message_of_the_day,
        "word_of_the_day": word_of_the_day,
        "ai_image_prompt": ai_image_prompt
    }

# Function to generate the daily message content
def generate_daily_message(stats):
    message = f"Hi, I'm Gaul Soodman, and here is today's message.\n\n"
    message += f"Current Forum Stats:\n"
    message += f"[quote]\n"
    message += f"Total Posts: {stats['total_posts']}\n"
    message += f"Total Topics: {stats['total_topics']}\n"
    message += f"Total Members: {stats['total_members']}\n"
    message += f"Average Posts Per Day: {stats['average_posts_per_day']}\n"
    message += f"Newest Member: {stats['newest_member']}\n"
    message += f"[/quote]\n\n"

    message += f"Today's Recommendations:\n"
    message += f"[quote]\n"
    message += f"TV Show: {stats['tv_show']}\n"
    message += f"Movie: {stats['movie']}\n"
    message += f"Song: {stats['song']}\n"
    message += f"Video Game: {stats['video_game']}\n"
    message += f"[/quote]\n\n"

    message += f"Daily Stuff:\n"
    message += f"[quote]\n"
    message += f"Message of the Day: {stats['message_of_the_day']}\n"
    message += f"Word of the Day: {stats['word_of_the_day']}\n"
    message += f"[/quote]\n\n"

    message += f"Daily AI Image Prompt:\n"
    message += f"[quote]\n"
    message += f"{stats['ai_image_prompt']}\n"
    message += f"(Post your results!)\n"
    message += f"[/quote]\n\n"

    message += f"Info:\n"
    message += f"[quote]\n"
    message += f"Gaul Soodman Bot by PhantomLuigi (Luigis_Pizza)\n"
    message += f"[url=\"https://discord.com/invite/gA5RMqMSAB\"] Join the Discord[/url] to suggest things for Gaul Soodman's Daily Message!\n"
    message += f"[/quote]"

    return message

# Function to post the daily message
def post_daily_message(content):
    global main_session
    obtain_post_page = main_session.get(FORUM_URL + f"index.php?action=post;topic=6602")
    hidden_val = lxml.etree.HTML(obtain_post_page.text.encode()).xpath('//*[@id="postmodify"]/input')
    form = {
        "topic": "6602",
        "check_timeout": 1,
        "subject": "Re: Gaul Soodman's Daily Message Centre",
        "icon": "xx",
        "message": content,
        "message_mode": 0,
        "notify": 0,
        "goback": 1
    }
    for v in hidden_val:
        form[v.get("name")] = v.get("value")
    postin = main_session.post(
        FORUM_URL + f"index.php?action=post;topic=6602",
        data=form)
    if postin.status_code == 200:
        print("Post successful")
    else:
        print("Failed to post")

# Main function
if login() == 200:
    while True:
        # Wait for 6 seconds before scraping stats
        time.sleep(6)
        print("Scraping stats...")

        stats = scrape_stats()
        daily_message = generate_daily_message(stats)
        print("Stats scraped. Generating the message...")

        # Wait for 6 seconds before posting the daily message
        time.sleep(6)
        print("Posting the daily message...")

        post_daily_message(daily_message)
        print("Daily message posted.")

        # Wait for 24 hours before posting the next daily message
        print("Waitng 24 hours till next post...")
        time.sleep(24 * 60 * 60)
        print("24 hours passed. Preparing to post...")
