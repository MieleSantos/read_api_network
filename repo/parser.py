class RepoParser:
    @classmethod
    def parse_plataforms(cls, response):
        for i in range(len(response)):
            repo = response[i]
            # repo = Repo(repo["id"], repo["name"], repo["stargazers_count"])
            print(repo)


# {
#     "body": {
#         "platforms": [
#             {"text": "Facebook Ads", "value": "meta_ads"},
#             {"text": "Google Analytics", "value": "ga4"},
#             {"text": "TikTok", "value": "tiktok_insights"},
#         ]
#     },
#     "status_code": 200,
# }
