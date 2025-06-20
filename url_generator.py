import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

st.title("📄 NotebookLM用URL一覧ジェネレーター（Markdown出力付き）")
st.write("指定したWebサイト内の下層ページURLを一覧化し、タイトル付きMarkdown形式でも出力できます")

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

            # Markdown形式で整形する
            markdown_output = ""
            for link in sorted(links):
                try:
                    r = requests.get(link, timeout=3)
                    inner_soup = BeautifulSoup(r.text, 'html.parser')
                    title = inner_soup.title.string.strip() if inner_soup.title else "（タイトルなし）"
                except:
                    title = "（タイトル取得失敗）"

                markdown_output += f"- [{title}]({link})\n"

            st.text_area("📋 Markdown形式（コピーしてNotebookLMへ貼り付けてね）", markdown_output, height=300)
        else:
            st.warning("内部リンクが見つかりませんでした。")

    except Exception as e:
        st.error(f"取得中にエラーが発生しました: {e}")
