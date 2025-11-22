import time
import json
import os
from FBTools import Start

# Colors - YE WALA CODE REPLACE KAREIN
class C:
    R = "\033[0m"   # Reset
    G = "\033[92m"  # Green
    Y = "\033[93m"  # Yellow  
    B = "\033[94m"  # Blue
    R2 = "\033[91m" # Red
    P = "\033[95m"  # Pink
    C = "\033[96m"  # Cyan - YE ADD KAREIN

def load_cookies(cookie_path):
    """Cookie file load karta hai"""
    try:
        with open(cookie_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        parts = [f"{c['name']}={c['value']}" for c in data if 'name' in c and 'value' in c]
        return "; ".join(parts)
    except Exception as e:
        print(C.R2 + f"Cookie Error: {e}" + C.R)
        return None

def comment_on_specific_post(fb, post_url, comment_text):
    """User ke specific post par comment karta hai"""
    print(f"\n{C.Y}📝 Post URL: {post_url}{C.R}")
    print(f"{C.Y}💬 Comment: {comment_text}{C.R}")
    print(f"{C.B}🔄 Processing...{C.R}")
    
    result = fb.CommentToPost(post=post_url, text=comment_text)
    return result

def main_interface():
    """Main user interface"""
    os.system("clear")
    print(C.P + "🎯 SPECIFIC POST COMMENT TOOL" + C.R)
    print(C.Y + "🔧 User Mentioned Post Par Comment Karein" + C.R)
    print("──────────────────────────────────────────")
    
    # Cookie load karein
    cookie_path = input(C.Y + "Cookie file path: " + C.R).strip()
    if not os.path.exists(cookie_path):
        print(C.R2 + "❌ Cookie file not found!" + C.R)
        return
    
    cookie_string = load_cookies(cookie_path)
    if not cookie_string:
        print(C.R2 + "❌ Invalid cookie file!" + C.R)
        return
    
    # Login karein
    print(C.B + "🔑 Logging in..." + C.R)
    try:
        fb = Start(cookie=cookie_string)
        print(C.G + "✅ Login successful!" + C.R)
    except Exception as e:
        print(C.R2 + f"❌ Login failed: {e}" + C.R)
        return
    
    # Main loop
    while True:
        print(f"\n{C.C}Options:{C.R}")
        print(f"{C.G}1. Specific Post Par Comment Karein{C.R}")
        print(f"{C.G}2. Exit{C.R}")
        
        choice = input(f"\n{C.Y}Select option (1-2): {C.R}").strip()
        
        if choice == '1':
            print(f"\n{C.P}🎯 POST COMMENT INTERFACE{C.R}")
            print("─────────────────────────")
            
            # User se post URL lein
            post_url = input(f"{C.Y}📝 Post URL ya Post ID dalen: {C.R}").strip()
            if not post_url:
                print(C.R2 + "❌ Post URL required!" + C.R)
                continue
            
            # User se comment text lein  
            comment_text = input(f"{C.Y}💬 Apna comment likhen: {C.R}").strip()
            if not comment_text:
                print(C.R2 + "❌ Comment text required!" + C.R)
                continue
            
            # Comment karein
            try:
                result = comment_on_specific_post(fb, post_url, comment_text)
                
                if result.get("status") == "success":
                    print(C.G + f"✅ Comment posted successfully!{C.R}")
                    print(C.G + f"📌 Comment ID: {result.get('comment_id')}{C.R}")
                    print(C.G + f"🎯 Post ID: {result.get('post_id')}{C.R}")
                else:
                    print(C.R2 + f"❌ Failed: {result.get('message')}{C.R}")
                    
            except Exception as e:
                print(C.R2 + f"❌ Error: {e}{C.R}")
                
        elif choice == '2':
            print(C.Y + "👋 Allah Hafiz!" + C.R)
            break
        else:
            print(C.R2 + "❌ Invalid option!" + C.R)

if __name__ == "__main__":

    main_interface()
