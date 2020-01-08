from Page import Page
import json
import requests
from urllib3 import disable_warnings

disable_warnings()


class Post:
    """Takes postId and page and generates a post element
    """

    def __init__(self, *, postId: str, page: Page):

        self.postId = postId
        self.page = page
        self.pageId = page.getPageId()
        self.postUrl = f"{page.getUrl()}posts/{self.postId}"
        self.accessToken = page.getAccessToken()
        with open("secrets/config.json", "r") as cfg:
            cfg = json.load(cfg)
            self.verify = cfg["verify"]
            self.apiversion = cfg["api_version"]
        self.likes = self.findLikes()

    def __str__(self):
        representation = f"PostId:\t{self.postId}\nPage:\t {self.page.getPageName()}\nLikes: \t{self.likes}"
        return representation

    def findLikes(self) -> str:
        """Does a lookup agains facebook api and returnes number of postlikes
        
        Returns:
            str -- [number of postlikes]
        """

        likesUrl = (
            f"https://graph.facebook.com/v{self.apiversion}/"
            f"{str(self.page.getPageId())}_{str(self.postId)}/likes?summary=true&"
            f"{self.accessToken}"
        )
        req = requests.get(likesUrl, verify=False)
        req = req.json()["summary"]["total_count"]
        return req

    def getLikes(self) -> str:
        """Returnes the number of likes the post has
        
        Returns:
            str -- [number of post likes]
        """
        return self.likes

    def getPostUrl(self) -> str:
        """Gets and returned the post Url as a string
        
        Returns:
            str -- [postUrl]
        """
        return self.postUrl

    def getPostId(self):
        """Gets and returned the post id as a string
        
        Returns:
            str -- [postId]
        """
        return self.postId
