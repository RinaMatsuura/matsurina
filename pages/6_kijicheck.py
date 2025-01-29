import streamlit as st
import openai
import pandas as pd  # pandasをインポートしてExcelやCSVを処理

# OpenAI APIキーの設定
openai.api_key = st.secrets["openai_api_key"]  # StreamlitのシークレットからAPIキーを取得

# ページタイトル
st.title("レギュレーションチェック")

# レギュレーションファイルのアップロード
regulation_file = st.file_uploader("レギュレーションファイルをアップロードしてください（ExcelまたはCSVファイル）", type=["xlsx", "csv"])

# URL入力フォーム
url = st.text_input("テキストを抽出したい記事のURLを入力してください:")

if st.button("チェック"):
    if regulation_file and url:
        try:
            # アップロードされたレギュレーションファイルの内容を読み込む
            if regulation_file.name.endswith('.xlsx'):
                regulation_text = pd.read_excel(regulation_file).to_string(index=False)  # Excelファイルを読み込む
            else:
                regulation_text = pd.read_csv(regulation_file).to_string(index=False)  # CSVファイルを読み込む

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
        st.warning("レギュレーションファイルと記事URLの両方を入力してください。")
