import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set the title of the app
st.title("News Search")

# Get the search keyword from the user input
keyword = st.text_input("Enter a keyword", "디지털혁신")

# Define the function to get the news search results from Naver
def search_news(keyword):
    url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={keyword}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', {'class': 'news_area'})

    results = []
    for article in articles[:10]:
        title_tag = article.find('a', {'class': 'news_tit'})
        title = title_tag['title']
        link = title_tag['href']
        content = article.find('div', {'class': 'news_dsc'}).text.strip()
        media = article.find('a', {'class': 'info press'}).text.strip()
        date = article.find('span', {'class': 'info'}).text.strip()

        results.append({
            'Title': title,
            'Content': content,
            'Media': media,
            'Date': date,
            'Link': link
        })

    return results

# Search for news with the keyword and display them in a table
results = search_news(keyword)
if len(results) > 0:
    df = pd.DataFrame(results)
    df['Title'] = df.apply(lambda x: f'<a href="{x.Link}" target="_blank">{x.Title}</a>', axis=1)
    df.drop('Link', axis=1, inplace=True)
    st.write(df.to_html(escape=False), unsafe_allow_html=True)
else:
    st.write(f"No results found for {keyword}")
