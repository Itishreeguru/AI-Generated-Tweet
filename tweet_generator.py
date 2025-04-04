import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv
import groq

# ✅ Load Groq API key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# ✅ Initialize Groq Client
client = groq.Client(api_key=groq_api_key)

# ✅ Streamlit Page Config
st.set_page_config(page_title="AI Tweet Generator", page_icon="🐦")
st.title('🧠 AI Tweet Generator (Groq + LangChain)')

# --- USER INPUT ---
topic = st.text_input("Enter a Tweet Topic:")
sentiment = st.selectbox("Select Sentiment:", ["Positive", "Neutral", "Negative"])
generate_reply = st.checkbox("Generate a reply to a tweet?")
reply_to = st.text_area("Paste a tweet to reply to (if checked):", disabled=not generate_reply)

# --- PROMPT TEMPLATES ---
title_template = PromptTemplate(
    input_variables=['topic', 'sentiment'],
    template="Write a short, engaging, {sentiment} tweet about {topic} in a Twitter-friendly style."
)

hashtag_template = PromptTemplate(
    input_variables=['topic'],
    template="Generate 3 trending hashtags for a tweet about {topic}."
)

tweet_template = PromptTemplate(
    input_variables=['title', 'wikipedia_research'],
    template="Using this TITLE: {title} and Wikipedia info: {wikipedia_research}, write a concise tweet in a fun and informative tone."
)

reply_template = PromptTemplate(
    input_variables=['input_tweet'],
    template="Generate a clever and relevant reply to this tweet: {input_tweet}"
)

# --- UTILITIES ---
wiki = WikipediaAPIWrapper()
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')

def generate_response(prompt_text):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt_text}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API Error: {e}"

# --- GENERATION FLOW ---
if topic:
    st.info("⏳ Generating tweet content...")
    
    # Title
    tweet_title = generate_response(
        title_template.format_prompt(topic=topic, sentiment=sentiment).to_string()
    )
    st.write("✅ **Generated Tweet Title:**", tweet_title)
    
    # Wikipedia Info
    wiki_research = wiki.run(topic)
    st.write("📚 **Wikipedia Research:**", wiki_research)
    
    # Final Tweet
    tweet = generate_response(
        tweet_template.format_prompt(title=tweet_title, wikipedia_research=wiki_research).to_string()
    )
    st.success("✍️ **Generated Tweet:**")
    st.write(tweet)
    
    # Hashtags
    hashtags = generate_response(
        hashtag_template.format_prompt(topic=topic).to_string()
    )
    st.info("🏷️ **Hashtag Suggestions:**")
    st.write(hashtags)

# --- Optional Reply Generator ---
if generate_reply and reply_to:
    st.divider()
    st.write("💬 **Generated Reply Tweet:**")
    reply = generate_response(
        reply_template.format_prompt(input_tweet=reply_to).to_string()
    )
    st.write(reply)
