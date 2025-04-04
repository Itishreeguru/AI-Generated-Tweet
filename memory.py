from langchain.memory import ConversationBufferMemory

def create_title_memory():
    return ConversationBufferMemory(input_key='topic', memory_key='chat_history')

def create_tweet_memory():
    return ConversationBufferMemory(input_key='title', memory_key='chat_history')
