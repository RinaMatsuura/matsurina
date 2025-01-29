import streamlit as st
import os
from openai import OpenAI

st.title("音声文字起こし 🎤")

# ファイルアップローダーの追加
uploaded_file = st.file_uploader("音声ファイルをアップロード", type=['mp3', 'm4a', 'wav', 'mp4'])

if uploaded_file is not None:
    # 一時ファイルとして保存
    with st.spinner("ファイルを処理中..."):
        temp_file_path = os.path.join("/tmp", uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        try:
            # OpenAI APIキーの設定
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            # Whisper APIを使用して文字起こし
            with open(temp_file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

            # 文字起こし結果の表示
            st.subheader("📝 文字起こし結果")
            st.write(transcription.text)

            # GPT-4による要約と整理
            st.subheader("🔍 会話の分析")
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": """
                    # システム設定
                    あなたは会話文の整理と文字起こしの専門家です。以下の指示に従って会話を整理してください：

                    ## 必須タスク
                    1. 複数の話者の発言を明確に区別し、整理してください
                    2. 以下のフォーマットで出力してください：

                    ### サマリー
                    - 会話の要約
                    - 次のアクション項目

                    ### 会話ログ
                    スピーカーA：発言内容
                    スピーカーB：発言内容
                    （時系列順に記載）

                    ## 出力形式
                    - 話者の区別は「話者名：」の形式で明示
                    - 時系列順に会話を整理
                    - 箇条書きで見やすく整形
                    """},
                    {"role": "user", "content": f"以下のテキストをまとめてください：\n{transcription.text}"}
                ],
                temperature=0,
                max_tokens=4096,
                top_p=0.1,
                presence_penalty=0,
                frequency_penalty=0
            )

            st.write(response.choices[0].message.content)

            # 一時ファイルの削除
            os.remove(temp_file_path)

        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

# 使い方の説明
with st.expander("💡 使い方"):
    st.write("""
    1. 音声ファイル（mp3, m4a, wav, mp4）をアップロード
    2. 自動で文字起こしが開始されます
    3. 文字起こし結果が表示されます
    4. GPT-4による会話の分析結果が表示されます
    """)

# フッター
st.sidebar.markdown("---")
st.sidebar.write("バージョン: 1.0.0")
st.sidebar.write("© 2024 まつりな")