import streamlit as st
import openai
import pandas as pd  # pandasをインポートしてExcelやCSVを処理

# 固定のレギュレーションファイルのパス
REGULATION_FILE_PATH = "regulation.xlsx"  # 固定のExcelファイルのパスを指定

# ページタイトル
st.title("準備中のページ（使わないで）")

# URL入力フォーム
url = st.text_input("レギュレーションチェックしたい記事のURLを入力してください:")

if st.button("チェック"):
    if url:
        try:
            # 固定のレギュレーションファイルの内容を読み込む
            regulation_text = pd.read_excel(REGULATION_FILE_PATH).to_string(index=False)  # Excelファイルを読み込む

            # OpenAI APIを使用してレギュレーションと記事を比較
            prompt = f"""
            以下のレギュレーションに基づいて、指定されたURLの内容がレギュレーションに抵触するかどうかを判断してください。

            ## レギュレーション
            {regulation_text}

            ## 記事URL
            {url}

            ## 指示
            記事がレギュレーションに抵触する場合は、その部分を指摘してください。
            """
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # または "gpt-4" を使用
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # 抽出したテキストを表示
            result_text = completion.choices[0].message['content']
            st.subheader("チェック結果:")
            st.text_area("結果", result_text, height=300)

        except Exception as e:
            st.error(f"OpenAI APIエラー: {str(e)}")
    else:
        st.warning("記事URLを入力してください。")
