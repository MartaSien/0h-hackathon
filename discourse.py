'''
Class to fetch data from Discourse REST API
'''
import os
import requests
from dotenv import load_dotenv

DISCOURSE_URL = "https://kb.hs3.pl" # Database is hosted here
DATABASE_CAT_ID = 9 # Database category ID
PLACES = [
    "online",
    "cow-work",
    "garage",
    "lab",
    "audiolab",
    "server-room"
]

class DiscourseDatabase():
    def __init__(self):
        load_dotenv()
    
    def get_headers(self, auth=False):
        """Get request headers, optionally with auth data."""
        headers = {
            "content-type": "application/json",
        }
        if auth:
            headers["Api-Key"] = os.getenv("DISCOURSE_PAT")
            headers["Api-Username"] = os.getenv("DISCOURSE_USERNAME")
        return headers

    def get_tag_data(self, tag):
        """Get all topics based on tag"""
        url = f"{DISCOURSE_URL}/tag/{tag}.json"
        print(f"Fetching data from {url}")
        all_topics = []
        page = 0
        while True:
            params = {"per_page": 100, "page": page}
            res = requests.get(url, headers=self.get_headers(), params=params)
            res.raise_for_status()
            res_json = res.json()
            topics = res_json["topic_list"]["topics"]
            if not topics:
                break
            for topic in topics:
                all_topics.append(topic)
            print(f"Fetched page {page}: {len(topics)} topics, {len(all_topics)} total in category")
            page += 1
        return {"topic_list": {"topics": all_topics}}

    def get_first_post_id(self, topic_id: str):
        """Get the first post ID from the topic"""
        topic_url = f"{DISCOURSE_URL}/t/{topic_id}.json"
        topic_res = requests.get(topic_url, headers=self.get_headers(auth=True))
        topic_res.raise_for_status()
        topic_data = topic_res.json()
        return topic_data["post_stream"]["posts"][0]["id"]

    def get_post_contents(self, post_id: str):
        """Get content of the post"""
        post_url = f"{DISCOURSE_URL}/posts/{post_id}.json"
        post_res = requests.get(post_url, headers=self.get_headers(auth=True))
        post_res.raise_for_status()
        return post_res.json()

    def put_tags(self, topic_id: str, tags: list):
        """Put tags to a topic"""
        url = f"{DISCOURSE_URL}/t/{topic_id}.json"
        payload = {"tags": tags}
        res = requests.put(url, json=payload, headers=self.get_headers(auth=True))
        res.raise_for_status()
        print(f"Added {tags} to {url}")
