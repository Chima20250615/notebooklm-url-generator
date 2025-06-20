import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

st.title("📄 NotebookLM用URL一覧ジェネレーター（Markdown付き）")
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

            # 通常URL表示（シンプルな確認用）
            for link in sorted(links):
                st.text(link)

# Markdown出力用
st.markdown("---")
st.subheader("📋 タイトル付きMarkdown形式（NotebookLMに貼り付けOK）")
markdown_output = ""

for link in sorted(links):
    try:
        r = requests.get(link, timeout=5)
        r.encoding = r.apparent_encoding  # ← ここで自動判定
        inner_soup = BeautifulSoup(r.text, 'html.parser')
        title = inner_soup.title.string.strip() if inner_soup.title else "（タイトルなし）"
    except Exception as e:
        title = "（タイトル取得失敗）"

    markdown_output += f"- [{title}]({link})\n"

st.text_area("🔗 コピーして使ってね", markdown_output, height=300)

        else:
            st.warning("内部リンクが見つかりませんでした。")

    except Exception as e:
        st.error(f"取得中にエラーが発生しました: {e}")
