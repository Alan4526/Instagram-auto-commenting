from openai import OpenAI

client = OpenAI(
  api_key="YOUR_API_KEY"
)

system = """You should write short comment for instagram post to recommend based on article content like bellow.
"Great post! 😊",
"Love your content! 🔥",
"This is awesome! 🙌",
"Keep up the great work! 💯",
"Really inspiring! 🚀",
"Amazing feed! 👌",
"Such a cool post! 🎉",
"You're doing great! 💡",
"Love your style! 💕",
"Awesome work! 👏"
comment content mustn't be repeated.
You can access chatting history.
"""
chatLog = ""
articleContent = "give me comment."

def cleanText(text):
    return text.replace('"', '')

def getComment():
    global chatLog
    completion = client.chat.completions.create( 
        model= "gpt-4o-mini",
        store=True,
        messages=[
            {
              "role": "system",
              "content": system
            },
            {"role": "assistant", "content": chatLog},
            {"role": "user", "content": articleContent}
        ])

    content = cleanText(completion.choices[0].message.content)

    if (len(chatLog) > 3000): chatLog = ""
    
    chatLog += "Chat Bot: " + content
    chatLog += "User: " + articleContent

    return completion.choices[0].message.content
