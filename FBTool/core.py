import requests
import json
import re
from typing import Dict, Optional

class Start:
    def __init__(self, cookie: str):
        self.cookie = cookie
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36",
            "Cookie": cookie,
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded"
        })
        self.base_url = "https://graph.facebook.com"

    def CommentToPost(self, post: str, text: str) -> Dict:
        """User ke diye hue specific post par comment karta hai"""
        try:
            post_id = self._extract_post_id(post)
            if not post_id:
                return {"status": "error", "message": "Invalid post ID or URL"}

            url = f"{self.base_url}/{post_id}/comments"
            access_token = self._extract_token_from_cookie()
            if not access_token:
                return {"status": "error", "message": "Invalid access token in cookie"}

            payload = {'message': text, 'access_token': access_token}

            response = self.session.post(url, data=payload)
            try:
                result = response.json()
            except json.JSONDecodeError:
                return {"status": "error", "message": "Invalid response from Facebook"}

            if response.status_code == 200 and 'id' in result:
                return {
                    "status": "success",
                    "message": "Comment posted successfully",
                    "comment_id": result.get('id'),
                    "post_id": post_id
                }
            else:
                error_msg = result.get('error', {}).get('message', 'Unknown error')
                return {
                    "status": "error",
                    "message": f"Facebook API Error: {error_msg}",
                    "status_code": response.status_code
                }

        except Exception as e:
            return {"status": "error", "message": f"Comment failed: {str(e)}"}

    def _extract_post_id(self, post_input: str) -> Optional[str]:
        """Post ID extract karta hai various formats se"""
        if post_input.isdigit():
            return post_input

        patterns = [
            r'facebook\.com/.+?/posts/(\d+)',
            r'story_fbid=(\d+)',
            r'/(\d+)/?$',
            r'post_id=(\d+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, post_input)
            if match:
                return match.group(1)

        return None  # Fallback agar ID extract nahi hui

    def _extract_token_from_cookie(self) -> Optional[str]:
        """Cookie se access token extract karta hai"""
        try:
            xs_match = re.search(r'xs=([^;]+)', self.cookie)
            if xs_match:
                return xs_match.group(1)
            return None
        except Exception:
            return None

    def GetPostInfo(self, post_id: str) -> Dict:
        """Post ki information leta hai"""
        try:
            url = f"{self.base_url}/{post_id}"
            params = {
                'access_token': self._extract_token_from_cookie(),
                'fields': 'id,message,created_time,from'
            }
            response = self.session.get(url, params=params)
            try:
                result = response.json()
            except json.JSONDecodeError:
                return {"status": "error", "message": "Invalid response from Facebook"}

            if response.status_code == 200:
                return {"status": "success", "post_info": result}
            else:
                return {"status": "error", "message": result.get('error', {}).get('message', 'Failed to get post info')}

        except Exception as e:
            return {"status": "error", "message": str(e)}
