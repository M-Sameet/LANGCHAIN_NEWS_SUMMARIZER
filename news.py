import streamlit as st
import os
import requests
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    raise ValueError("Google API key not found. Please set it in the .env file.")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GOOGLE_API_KEY, temperature=0)


def summerizer(cont):
    prompt_template_name = PromptTemplate(
        input_variables=['cont'],
        template="I need to summerize text in 8 to 10 lines. here is my text '{cont}'."
    )

    name_chain = LLMChain(llm=llm, prompt=prompt_template_name)

    response = name_chain.run({'cont': cont})

    return response


def fetch_news(api_key, query, language='en', page_size=5):
    url = 'https://newsapi.org/v2/everything'

    # Parameters for the API request
    params = {
        'q': query,
        'language': language,
        'pageSize': page_size,
        'apiKey': api_key
    }

    # Make the request to the News API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        return articles
    else:
        print(f"Failed to fetch news: {response.status_code}")
        return None


# Streamlit app layout
st.title("News Fetcher App")

# Input fields for the API key and query
api_key = "<YOUR_NEWS_API_KEY>"
query = st.text_input("Enter the topic you want to search for")

fetch_news(api_key, query)

# Button to fetch news
if st.button("Fetch News"):
    if api_key and query:
        news_articles = fetch_news(api_key, query)
        print(news_articles)

        if news_articles:
            for idx, article in enumerate(news_articles, start=1):
                title = ({article['title']})
                print(title)

                st.subheader(f"{idx}. {article['title']}")
                st.write(f"Source: {article['source']['name']}")
                st.write(f"Published at: {article['publishedAt']}")
                # st.write(f"Description: {article['description']}")
                cont = article.get("content")
                with st.spinner("Fetching..."):
                    response = summerizer(cont)
                    st.write("content: ")
                    st.write(response)

                    st.write("---")
        else:
            st.write("No articles found.")
    else:
        st.warning("Please enter both API Key and a search topic.")