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
            # ユーザーエージェントとリファラーを指定してURLからHTMLを取得
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": url  # リファラーをURLに設定
            }
            response = requests.get(url, headers=headers)
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
