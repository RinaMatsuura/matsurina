import streamlit as st
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
            # OpenAI APIを使用してURLの内容を要約
            prompt = f"以下のURLの内容を要約してください:\n{url}\n\n内容:この記事のテキスト部分を抜き出して"
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # または "gpt-4" を使用
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # 抽出したテキストを表示
            extracted_text = completion.choices[0].message['content']
            st.subheader("抽出したテキスト:")
            st.text_area("テキスト", extracted_text, height=300)

        except Exception as e:
            st.error(f"OpenAI APIエラー: {str(e)}")
    else:
        st.warning("URLを入力してください。")