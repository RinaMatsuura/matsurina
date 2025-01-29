import streamlit as st
import requests
from bs4 import BeautifulSoup

# ページタイトル
st.title("URLからテキストを抽出するページ")

# URL入力フォーム
url = st.text_input("テキストを抽出したいURLを入力してください:")

if st.button("テキストを抽出"):
    if url:
        try:
            # URLからHTMLを取得
            response = requests.get(url)
            response.raise_for_status()  # HTTPエラーが発生した場合は例外を投げる

            # BeautifulSoupでHTMLを解析
            soup = BeautifulSoup(response.text, 'html.parser')

            # ページ内のテキストを抽出
            text = soup.get_text(separator='\n', strip=True)

            # 抽出したテキストを表示
            st.subheader("抽出したテキスト:")
            st.text_area("テキスト", text, height=300)

        except requests.exceptions.RequestException as e:
            st.error(f"エラーが発生しました: {str(e)}")
    else:
        st.warning("URLを入力してください。")
