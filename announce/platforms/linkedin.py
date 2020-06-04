import requests
from announce import const


def run(session, event):
    headers = {"Authorization": f"Bearer {session.get('access_token')}"}
    # r = requests.get(
    # f"https://api.linkedin.com/v2/organizations/{const.linkedin_org_id}",
    # headers=headers,
    # )
    # This must not be done. we need an org post.
    # r = requests.get("https://api.linkedin.com/v2/me", headers=headers)
    # uid = r.json()["id"]
    uid = const.linkedin_org_id
    data = {
        "author": f"urn:li:organization:{uid}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": event.description},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    if event.poster:
        r = requests.post(
            "https://api.linkedin.com/v2/assets?action=registerUpload",
            json={
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": f"urn:li:organization:{uid}",
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent",
                        }
                    ],
                }
            },
            headers=headers,
        )
        j = r.json()
        asset = j["value"]["asset"]
        url = j["value"]["uploadMechanism"]
        url = url["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"][
            "uploadUrl"
        ]
        event.poster.seek(0)
        h = {
            "Accept": "*/*",
            **headers,
        }
        r = requests.put(url, data=event.poster.read(), headers=h)
        data["specificContent"]["com.linkedin.ugc.ShareContent"][
            "shareMediaCategory"
        ] = "IMAGE"
        data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
            {"status": "READY", "media": asset, "title": {"text": event.title},}
        ]
    r = requests.post(
        "https://api.linkedin.com/v2/ugcPosts", json=data, headers=headers,
    )
    print(r.json())
    return const.Event(**{**event._asdict(), "linkedin_id": r.json()["id"]})
