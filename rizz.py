import random
import re

# =====================
# 🚫 CRINGE FILTER
# =====================
CRINGE_WORDS = [
    "m'lady", "queen", "goddess", "angel", "perfect",
    "marry me", "wife", "soulmate", "obsessed",
    "can't live without", "simp", "mommy"
]

def is_cringe(text):
    text = text.lower()
    return any(word in text for word in CRINGE_WORDS)


# =====================
# 🧊 ICEBREAKERS
# =====================
ICEBREAKERS = [
    "Hey, random question — coffee or tea?",
    "Okay this might be random, but what’s your favorite food?",
    "Quick poll: night owl or morning person?",
    "What’s something small that made you smile today?",
    "Serious question — favorite music genre?"
]


# =====================
# 💬 RESPONSE GENERATOR
# =====================
REPLY_TEMPLATES = {
    "short": [
        "That makes sense.",
        "Yeah, I get that.",
        "Honestly, same.",
        "That’s fair."
    ],
    "engaging": [
        "That’s interesting — what got you into that?",
        "How long have you been into that?",
        "What do you like most about it?",
        "That actually sounds fun."
    ],
    "playful": [
        "Okay, that’s a good answer.",
        "I respect that choice 😄",
        "Valid, not gonna lie.",
        "Alright, you might be onto something."
    ]
}


# =====================
# 🧠 CONVERSATION MEMORY
# =====================
class ConversationMemory:
    def __init__(self):
        self.topics = []
        self.last_message = ""

    def remember(self, message):
        keywords = re.findall(r"\b\w+\b", message.lower())
        important = [k for k in keywords if len(k) > 4]
        self.topics.extend(important[:2])
        self.last_message = message

    def recall_topic(self):
        return random.choice(self.topics) if self.topics else None


memory = ConversationMemory()


# =====================
# 📱 STYLE ADAPTER
# =====================
def adapt_style(text, platform):
    if platform in ["dm", "instagram"]:
        return text.replace(".", "").replace(" —", ",")
    if platform == "whatsapp":
        return text
    return text


# =====================
# 🤖 MAIN RIZZ ENGINE
# =====================
def generate_reply(her_message, platform="dm"):
    memory.remember(her_message)

    tone = random.choice(["short", "engaging", "playful"])
    reply = random.choice(REPLY_TEMPLATES[tone])

    follow_up = ""
    topic = memory.recall_topic()
    if topic:
        follow_up = f" By the way, how did you get into {topic}?"

    final = reply + follow_up

    if is_cringe(final):
        final = random.choice(REPLY_TEMPLATES["short"])

    return adapt_style(final, platform)


def generate_icebreaker(platform="dm"):
    line = random.choice(ICEBREAKERS)
    if is_cringe(line):
        return generate_icebreaker(platform)
    return adapt_style(line, platform)


# =====================
# ▶️ CLI DEMO
# =====================
if __name__ == "__main__":
    print("🤖 Rizz Assistant v1.0\n")
    print("Mode:")
    print("1 - Icebreaker")
    print("2 - Reply to her message")
    mode = input("Choose mode (1/2): ").strip()

    platform = input("Platform (dm / whatsapp / instagram): ").strip().lower()

    if mode == "1":
        print("\n💬 Icebreaker:\n")
        print("👉", generate_icebreaker(platform))

    elif mode == "2":
        her_msg = input("\nHer message: ")
        print("\n💬 Suggested reply:\n")
        print("👉", generate_reply(her_msg, platform))

    else:
        print("❌ Invalid mode")
