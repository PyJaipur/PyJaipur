import requests


def run(session, event):
    headers = {"Authorization": f"Bearer {session.get('access_token')}"}
    uid = requests.get("https://api.linkedin.com/v2/me", headers=headers).json()["id"]
    data = {
        "author": f"urn:li:person:{uid}",
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
                    "owner": f"urn:li:person:{uid}",
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
        r = requests.post(url, files=event.poster, headers=headers)
        data["specificContent"]["shareMediaCategory"] = "IMAGE"
        data["specificContent"]["media"] = [
            {
                "status": "READY",
                "description": {"text": "Center stage!"},
                "media": asset,
                "title": {"text": event.title},
            }
        ]
    r = requests.post(
        "https://api.linkedin.com/v2/ugcPosts", json=data, headers=headers,
    )
    return event
