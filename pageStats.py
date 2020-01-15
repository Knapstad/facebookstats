from Page import Page
import datetime
from urllib3 import disable_warnings

# from pandas.io.json import normalize_json
disable_warnings()
nabohjelp = Page.fromName("obosnabohjelp")

pagelist = [nabohjelp]

for page in pagelist:
    facebook_likes = page.getPageLikes(period="day", date_preset="today")
    facebook_impressions = page.getPageImpressions(period="day", date_preset="today")
    facebook_reactions = page.getPageReactions(period="day", date_preset="today")
    instagram_stats = page.getInstagramImpressions(period="day")
    instagram_folowers = page.getInstagramFolowers()

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
"instagtram_profile_views" : instagram_stats.get("data",[{}])[2].get("values",[{}])[-1].get("value",0),
"instagtram_website_clicks" : instagram_stats.get("data",[{}])[3].get("values",[{}])[-1].get("value",0),
"instagtram_text_message_clicks" : instagram_stats.get("data",[{}])[4].get("values",[{}])[-1].get("value",0)
"date":  datetime.datetime.now().isoformat()[0:-3]+"z"
}
]




