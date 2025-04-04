from langchain_community.utilities import WikipediaAPIWrapper

wiki = WikipediaAPIWrapper()

def get_wikipedia_summary(topic):
    return wiki.run(topic)
