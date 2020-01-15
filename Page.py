import requests
import json
from urllib3 import disable_warnings
from io import StringIO

disable_warnings()


class Page:
    
    def __init__(
        self, *, pageId: str, userName: str, pageName: str, pageUrl: str, pageLikes: int, instagramId: str
    ):
        config = json.load(open("secrets/config.json"))
        self.pageId = pageId
        self.userName = userName
        self.pageName = pageName
        self.pageUrl = pageUrl
        self.pageLikes = pageLikes
        self.adId = config["ad_accout_id"]
        self.apiversion = config["api_version"]
        self.accessToken = f"access_token={Page.findAccesstoken(self.userName)}"
        self.graphUrl = f"https://graph.facebook.com/v{self.apiversion}/{self.pageId}"
        self.adUrl = f"https://graph.facebook.com/v{self.apiversion}/act_{self.adId}/ads?fields=creative{{effective_object_story_id}}"
        self.instagramId = instagramId

    def __str__(self):
        """Generates a descriptive string representation of the Page object
    
        Returns:
        [String] -- [Representation]
        """
        representation = (
            f"Page: {self.pageName}\nPageUsername: {self.userName}\nPageId: {self.pageId}"
            f"\nPageUrl: {self.pageUrl}\nPageLikes: {self.pageLikes}"
        )
        return representation

    @classmethod
    def fromName(cls, name: str) -> "Page":
        config = json.load(open("secrets/config.json"))
        apiversion = config["api_version"]
        accessToken = f"access_token={Page.findAccesstoken(name)}"
        url = f"https://graph.facebook.com/v{apiversion}/{name}?fields=link,username,name,id,fan_count,instagram_business_account&{accessToken}"
        response = requests.get(url, verify=False).json()
        return cls(
            pageId=response["id"],
            pageName=response["name"],
            userName=response["username"],
            pageUrl=response["link"],
            pageLikes=response["fan_count"],
            instagramId=response["instagram_business_account"]["id"]
        )

    @classmethod
    def fromId(cls, pageId: str) -> "Page":
        config = json.load(open("secrets/config.json"))
        apiversion = config["api_version"]
        accessToken = f"access_token={Page.findAccesstoken(pageId)}"
        url = f"https://graph.facebook.com/v{apiversion}/{pageId}?fields=link,username,id,name,fan_count,instagram_business_account&{accessToken}"
        response = requests.get(url, verify=False).json()
        return cls(
            pageId=response["id"],
            pageName=response["name"],
            userName=response["username"],
            pageUrl=response["link"],
            pageLikes=response["fan_count"],
            instagramId=response["instagram_business_account"]["id"]
        )


    def getUrl(self) -> str:
        return self.pageUrl

    def getUserName(self) -> str:
        return self.userName

    def getPageName(self) -> str:
        return self.pageName

    def getLikes(self) -> str:
        return self.pageLikes

    def getPageId(self) -> str:
        return self.pageId

    def getAccessToken(self) -> str:
        return self.accessToken

    def getPostIds(self) -> list:
        """ Gets postids for latest posts"""
        maxcount = 80
        try:
            postIds1 = requests.get(
                f"{self.graphUrl}?fields=posts&{self.accessToken}", verify=False
            )
            if (
                json.load(StringIO(postIds1.headers["x-business-use-case-usage"]))[
                    self.pageId
                ][0]["call_count"]
                > maxcount
            ):
                time.sleep(2)
            postIds2 = requests.get(
                f"{postIds1.json()['posts']['paging']['next']}", verify=False
            )
            postIds3 = requests.get(
                f"{postIds2.json()['paging']['next']}", verify=False
            )
            postIds = (
                postIds1.json()["posts"]["data"]
                + postIds2.json()["data"]
                + postIds3.json()["data"]
            )
            ids = [post["id"].split("_")[1] for post in postIds]
            return ids
        except Exception as e:
            print(e)

    def getAdIds(self):
        adIds = requests.get(
            f"{self.adUrl}&limit=1000&{self.accessToken}", verify=False
        ).json()["data"]
        ids = [
            ad["creative"]["effective_object_story_id"].split("_")[1]
            for ad in adIds
            if ad["creative"]["effective_object_story_id"].split("_")[0] == self.pageId
        ]
        return ids

    def getAllIds(self) -> list:
        adIds = self.getAdIds()
        postIds = self.getPostIds()
        return postIds + adIds

    @staticmethod
    def findAccesstoken(name) -> str:
        with open("pages.json", "r") as f:
            file = json.load(f)
        for page in file["data"]:
            if page["id"] == name:
                return page["access_token"]
            if page["name"] == name:
                return page["access_token"]
            if page["username"] == name:
                return page["access_token"]

    def getMetrics(self, since: str = "", until: str = "", period: str = "", date_preset: str = "", metrics: str = ""):
        if since is not "":
            since = f"&since={since}"
        if until is not "":
            until = f"&untill={until}"
        if period is not "":
            period = f"&period={period}"
        if date_preset is not "":
            date_preset = f"&date_preset={date_preset}"
        url = f"https://graph.facebook.com/v{self.apiversion}/{self.userName}/insights/{metrics}?{self.accessToken}{since}{until}{period}{date_preset}"
        dataJson = requests.get(url, verify=False).json()["data"]
        return dataJson
        

    def getPageImpressions(
        self, since: str = "", until: str = "", period: str = "", date_preset: str = ""
    ) -> json:
        metrics = "page_impressions_unique,page_impressions_organic_unique,page_impressions_paid_unique"
        return self.getMetrics(since=since, until=until, period=period, date_preset=date_preset, metrics=metrics)

    def getPageLikes(
        self, since: str = "", until: str = "", period: str = "", date_preset: str = ""
    ) -> json:
        metrics = "page_fans,page_fan_adds,page_fan_removes"
        return self.getMetrics(since=since, until=until, period=period, date_preset=date_preset, metrics=metrics)

    def getPageReactions(
        self, since: str = "", until: str = "", period: str = "day", date_preset: str = ""
    ) -> json:
        metrics = "page_actions_post_reactions_total"
        return self.getMetrics(since=since, until=until, period=period, date_preset=date_preset, metrics=metrics)

    def getPageReach(
        self, since: str = "", until: str = "", period: str = "day", date_preset: str = ""
    ) -> json:
        metrics = "page_actions_post_reactions_total"
        return self.getMetrics(since=since, until=until, period=period, date_preset=date_preset, metrics=metrics)


    # def getPage

    def getInstagramImpressions(
                self, since: str = "", until: str = "", period: str = "&period=day", date_preset: str = ""
    ) -> json:
        """Gets the impression and reach from instagram, perod defaults to day as intagram api requires period to be set."""
        if since is not "":
            since = f"&since={since}"
        if until is not "":
            until = f"&untill={until}"
        if period is not "&period=day":
            period = f"&period={period}"
        if date_preset is not "":
            date_preset = f"&date_preset={date_preset}"
        metrics = "impressions, reach, profile_views, website_clicks, text_message_clicks, follower_count"
        url = f"https://graph.facebook.com/v{self.apiversion}/{self.instagramId}/insights/{metrics}?{self.accessToken}{since}{until}{period}{date_preset}"
        dataJson = requests.get(url, verify=False).json()
        return dataJson

    def getInstagramFollowers(
                self, since: str = "", until: str = "", period: str = "&period=day", date_preset: str = ""
    ) -> json:
        """Gets the impression and reach from instagram, perod defaults to day as intagram api requires period to be set."""
        if since is not "":
            since = f"&since={since}"
        if until is not "":
            until = f"&untill={until}"
        if period is not "&period=day":
            period = f"&period={period}"
        if date_preset is not "":
            date_preset = f"&date_preset={date_preset}"
        metrics = "followers_count, media_count"
        url = f"https://graph.facebook.com/v{self.apiversion}/{self.instagramId}?fields={metrics}&{self.accessToken}{since}{until}{period}{date_preset}"
        dataJson = requests.get(url, verify=False).json()
        return dataJson


