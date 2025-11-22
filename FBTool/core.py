import requests
import json
import time

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
        """
        User ke diye hue specific post par comment karta hai
        Args:
            post: Post ID ya Post URL jo user ne mention ki
            text: Comment text
        """
        try:
            # Post ID extract karta hai agar URL diya ho
            post_id = self._extract_post_id(post)
            
            if not post_id:
                return {
                    "status": "error", 
                    "message": "Invalid post ID or URL"
                }
            
            # Facebook Graph API use karta hai comment ke liye
            url = f"{self.base_url}/{post_id}/comments"
            
            # Access token cookie se extract karta hai
            access_token = self._extract_token_from_cookie()
            
            payload = {
                'message': text,
                'access_token': access_token
            }
            
            response = self.session.post(url, data=payload)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "message": "Comment posted successfully",
                    "comment_id": result.get('id'),
                    "post_id": post_id
                }
            else:
                error_msg = response.json().get('error', {}).get('message', 'Unknown error')
                return {
                    "status": "error",
                    "message": f"Facebook API Error: {error_msg}",
                    "status_code": response.status_code
                }
                
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Comment failed: {str(e)}"
            }
    
    def _extract_post_id(self, post_input: str) -> str:
        """Post ID extract karta hai various formats se"""
        # Agar direct post ID hai
        if post_input.isdigit():
            return post_input
            
        # Agar URL hai to ID extract karta hai
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
                
        return post_input  # Fallback
    
    def _extract_token_from_cookie(self) -> str:
        """Cookie se access token extract karta hai"""
        try:
            # Cookie se xs token extract karta hai
            xs_match = re.search(r'xs=([^;]+)', self.cookie)
            if xs_match:
                return xs_match.group(1)
            return "dummy_token"  # Fallback
        except:
            return "dummy_token"
    
    def GetPostInfo(self, post_id: str) -> Dict:
        """Post ki information leta hai"""
        try:
            url = f"{self.base_url}/{post_id}"
            params = {
                'access_token': self._extract_token_from_cookie(),
                'fields': 'id,message,created_time,from'
            }
            
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                return {
                    "status": "success",
                    "post_info": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to get post info"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

# Regex import
import re
