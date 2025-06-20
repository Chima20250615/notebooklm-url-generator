import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

st.title("📄 NotebookLM用URL一覧ジェネレーター")
st.write("指定したWebサイト内の下層ページURLを一覧化します（NotebookLM用）")

# 入力：URL
base_url = st.text_input("対象サイトのトップURLを入力してね", "https://example.com")

if st.button("URL一覧を取得！"):
    try:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        parsed_base = urlparse(base_url)
        domain = f"{parsed_base.scheme}://{parsed_base.netloc}"

        links = set()

        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            full_url = urljoin(base_url, href)
            if full_url.startswith(domain):
                links.add(full_url)

        if links:
            st.success(f"{len(links)}件のURLを取得しました👇")
            for link in sorted(links):
                st.text(link)
        else:
            st.warning("内部リンクが見つかりませんでした。")

    except Exception as e:
        st.error(f"取得中にエラーが発生しました: {e}")
