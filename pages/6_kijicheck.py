import streamlit as st
import requests
import os
from dotenv import load_dotenv
import openai

# .envファイルを読み込む
load_dotenv()

# OpenAI APIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")

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

            # OpenAI APIを使用してテキストを抽出
            prompt = f":\n{url}\n\n内容:この記事のテキスト部分抜き出して"
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # 抽出したテキストを表示
            extracted_text = completion.choices[0].message.content
            st.subheader("抽出したテキスト:")
            st.text_area("テキスト", extracted_text, height=300)

        except requests.exceptions.RequestException as e:
            st.error(f"エラーが発生しました: {str(e)}")
        except Exception as e:
            st.error(f"OpenAI APIエラー: {str(e)}")
    else:
        st.warning("URLを入力してください。")
