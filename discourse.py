'''
Class to fetch data from Discourse REST API
'''
import requests
from dotenv import load_dotenv

DISCOURSE_URL = "https://kb.hs3.pl" # Database is hosted here

class DiscourseDatabase():    
    def get_headers(self, ):
        """Get request headers, optionally with auth data."""
        headers = {
            "content-type": "application/json",
        }
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

    def get_post_contents(self, post_id: str):
        """Get content of the post"""
        post_url = f"{DISCOURSE_URL}/posts/{post_id}.json"
        post_res = requests.get(post_url, headers=self.get_headers())
        post_res.raise_for_status()
        return post_res.json()
