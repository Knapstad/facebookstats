import requests
import datetime
import json
import time

from Page import Page
from urllib3 import disable_warnings

disable_warnings()
nabohjelp = Page.fromName("obosnabohjelp")
config = json.load(open("secrets/config.json"))
endpoint = config["powerbi_url"]
pagelist = [nabohjelp]

def deliver_payload():
    """gets and delivers data from facebook and instagram to powerbi endpoint"""

    for page in pagelist:
        facebook_likes = page.getPageLikes(period="day", date_preset="today")
        facebook_impressions = page.getPageImpressions(period="day", date_preset="today")
        facebook_reactions = page.getPageReactions(period="day", date_preset="today")
        instagram_stats = page.getInstagramImpressions(period="day")
        instagram_followers = page.getInstagramFollowers()

    payload =[
    {
    "facebook_page_fans" : facebook_likes[0].get("values",[{}])[0].get("value", 0),
    "facebook_page_fan_adds" : facebook_likes[1].get("values",[{}])[0].get("value", 0),
    "facebook_page_fan_removes" : facebook_likes[2].get("values",[{}])[0].get("value", 0),
    "facebook_page_impressions_unique" : facebook_impressions[0].get("values",[{}])[0].get("value"),
    "facebook_page_impressions_organic_unique" : facebook_impressions[1].get("values",[{}])[0].get("value"),
    "facebook_page_impressions_paid_unique" : facebook_impressions[2].get("values",[{}])[0].get("value"),
    "facebook_page_post_like" : facebook_reactions[0].get("values")[0].get("value").get("like", 0),
    "facebook_page_post_haha" : facebook_reactions[0].get("values")[0].get("value").get("haha", 0),
    "facebook_page_post_love" : facebook_reactions[0].get("values")[0].get("value").get("love", 0),
    "facebook_page_post_wow" : facebook_reactions[0].get("values")[0].get("value").get("wow", 0),
    "facebook_page_post_sorry" : facebook_reactions[0].get("values")[0].get("value").get("sorry", 0),
    "facebook_page_post_anger" : facebook_reactions[0].get("values")[0].get("value").get("anger", 0),
    "facebook_page_post_reactions" : sum(facebook_reactions[0].get("values")[0].get("value").values()),
    "instagram_impressions" : instagram_stats.get("data",[{}])[0].get("values",[{}])[-1].get("value",0),
    "instagram_reach" : instagram_stats.get("data",[{}])[1].get("values",[{}])[-1].get("value",0),
    "instagram_profile_views" : instagram_stats.get("data",[{}])[2].get("values",[{}])[-1].get("value",0),
    "instagram_website_clicks" : instagram_stats.get("data",[{}])[3].get("values",[{}])[-1].get("value",0),
    "instagram_text_message_clicks" : instagram_stats.get("data",[{}])[4].get("values",[{}])[-1].get("value",0),
    "instagram_followers": instagram_followers.get("followers_count", 0),
    "instagram_media_count": instagram_followers.get("media_count", 0),
    "date":  (datetime.datetime.now()-datetime.timedelta(hours=1)).isoformat()[0:-3]+"Z",
    "update" : (datetime.datetime.now()-datetime.timedelta(hours=1)).isoformat()[14:16]
    }
    ]
    requests.post(endpoint, json=payload, verify=False)
    print(payload[0]["date"])
    print(payload[0])

if __name__ == "__main__":
    while True:
        deliver_payload()
        
        for i in range(60):
            time.sleep(1)



