

def check_for_emergency(text):
    trigger_keywords = ["help", "save me", "emergency", "sos", "danger"]
    for word in trigger_keywords:
        if word.lower() in text.lower():
            print("🚨 Emergency trigger detected from text input!")
            return True
    return False

# Example usage
if __name__ == "__main__":
    user_input = input("Type your message: ")
    if check_for_emergency(user_input):
        print("🚨 Take action! Send alert, record location.")
    else:
        print("✅ No emergency detected.")