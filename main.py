import os
import json
from FBTools import Start

# Terminal colors
class C:
    R = "\033[0m"   # Reset
    G = "\033[92m"  # Green
    Y = "\033[93m"  # Yellow  
    B = "\033[94m"  # Blue
    R2 = "\033[91m" # Red
    P = "\033[95m"  # Pink
    CYAN = "\033[96m"  # Cyan

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

def comment_on_post(fb, post_url, comment_text):
    """Specific post par comment karta hai"""
    result = fb.CommentToPost(post=post_url, text=comment_text)
    return result

def main_interface():
    """Main interface"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(C.P + "🎯 SPECIFIC POST COMMENT TOOL" + C.R)
    print(C.Y + "🔧 User Mentioned Post Par Comment Karein" + C.R)
    print("──────────────────────────────────────────")

    cookie_path = input(C.Y + "Cookie file path: " + C.R).strip()
    if not os.path.exists(cookie_path):
        print(C.R2 + "❌ Cookie file not found!" + C.R)
        return

    cookie_string = load_cookies(cookie_path)
    if not cookie_string:
        print(C.R2 + "❌ Invalid cookie file!" + C.R)
        return

    try:
        fb = Start(cookie=cookie_string)
        print(C.G + "✅ Login successful!" + C.R)
    except Exception as e:
        print(C.R2 + f"❌ Login failed: {e}" + C.R)
        return

    while True:
        print(f"\n{C.CYAN}Options:{C.R}")
        print(f"{C.G}1. Specific Post Par Comment Karein{C.R}")
        print(f"{C.G}2. Exit{C.R}")

        choice = input(f"\n{C.Y}Select option (1-2): {C.R}").strip()

        if choice == '1':
            post_url = input(f"{C.Y}📝 Post URL ya Post ID dalen: {C.R}").strip()
            if not post_url:
                print(C.R2 + "❌ Post URL required!" + C.R)
                continue

            comment_text = input(f"{C.Y}💬 Apna comment likhen: {C.R}").strip()
            if not comment_text:
                print(C.R2 + "❌ Comment text required!" + C.R)
                continue

            result = comment_on_post(fb, post_url, comment_text)
            if result.get("status") == "success":
                print(C.G + f"✅ Comment posted successfully!{C.R}")
                print(C.G + f"📌 Comment ID: {result.get('comment_id')}{C.R}")
                print(C.G + f"🎯 Post ID: {result.get('post_id')}{C.R}")
            else:
                print(C.R2 + f"❌ Failed: {result.get('message')}{C.R}")

        elif choice == '2':
            print(C.Y + "👋 Allah Hafiz!" + C.R)
            break
        else:
            print(C.R2 + "❌ Invalid option!" + C.R)

if __name__ == "__main__":
    try:
        main_interface()
    except KeyboardInterrupt:
        print(C.Y + "\n👋 Program exited by user" + C.R)
