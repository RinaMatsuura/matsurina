import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
from wordcloud import WordCloud
import MeCab

# MeCabの初期化をシンプルに
tagger = MeCab.Tagger()  # 引数なしで初期化

st.header("テキスト分析 📊", divider="rainbow")

# ファイルアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

if uploaded_file is not None:
    try:
        # CSVファイルを読み込む
        df = pd.read_csv(uploaded_file, encoding='shift-jis')
        
        # カラム選択
        text_column = st.selectbox(
            "分析するカラムを選択してください",
            df.columns.tolist()
        )
        
        # 品詞選択
        pos_options = ["名詞", "動詞", "形容詞", "副詞"]
        selected_pos = st.multiselect(
            "抽出する品詞を選択してください",
            pos_options,
            default=["名詞"]
        )
        
        # テキストデータの前処理
        def process_text(text):
            # 単語と品詞の抽出
            words = []
            node = tagger.parseToNode(str(text))
            
            while node:
                # 品詞を取得
                pos = node.feature.split(',')[0]
                
                # 選択された品詞のみを抽出
                if pos in selected_pos:
                    word = node.surface
                    # 空でなく、1文字以上の単語を追加
                    if word and len(word) > 1:
                        words.append(word)
                node = node.next
                
            return words
        
        # 全テキストを結合して前処理
        all_words = []
        for text in df[text_column]:
            if pd.notna(text):
                all_words.extend(process_text(text))
        
        # テキストを空白区切りの文字列に変換
        txt = ' '.join(all_words)
        
        # ワードクラウド生成ボタン
        if st.button("🎨 ワードクラウドを生成"):
            with st.spinner("ワードクラウドを生成中..."):
                try:
                    # ワードクラウドの生成
                    wordcloud = WordCloud(
                        background_color="white",
                        font_path="/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
                        width=800,
                        height=600,
                        regexp=r"[\w']+",
                        collocations=False,  # 単語の重複を許可しない
                        min_font_size=10,    # 最小フォントサイズ
                        max_words=100        # 最大単語数
                    ).generate(txt)
                    
                    # プロットの作成
                    fig, ax = plt.subplots(figsize=(10, 8))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    
                    # Streamlitでプロット表示
                    st.pyplot(fig)
                    
                    # 頻出単語の表示
                    word_freq = Counter(all_words).most_common(20)
                    
                    st.subheader("頻出単語TOP20（表）")
                    freq_df = pd.DataFrame(word_freq, columns=['単語', '出現回数'])
                    st.dataframe(freq_df, use_container_width=True)
                    
                    # 画像のダウンロード
                    plt.savefig('wordcloud.png', bbox_inches='tight', pad_inches=0)
                    with open('wordcloud.png', 'rb') as file:
                        btn = st.download_button(
                            label="📥 ワードクラウド画像をダウンロード",
                            data=file,
                            file_name="wordcloud.png",
                            mime="image/png"
                        )
                except Exception as e:
                    st.error(f"ワードクラウドの生成中にエラーが発生しました: {str(e)}")
                    # 代替フォントを試す
                    try:
                        wordcloud = WordCloud(
                            background_color="white",
                            font_path="/System/Library/Fonts/AppleGothic.ttf",
                            width=800,
                            height=600,
                            regexp=r"[\w']+",
                            collocations=False,
                            min_font_size=10,
                            max_words=100
                        ).generate(txt)
                        fig, ax = plt.subplots(figsize=(10, 8))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"代替フォントでも失敗しました: {str(e)}")
                
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")

# 使い方の説明
with st.expander("💡 使い方"):
    st.write("""
    1. 分析したいテキストデータを含むCSVファイルをアップロード
    2. 分析するカラムを選択
    3. 抽出したい品詞を選択
    4. 「ワードクラウドを生成」ボタンをクリック
    5. 生成されたワードクラウドと頻出単語を確認
    6. 必要に応じて画像をダウンロード
    """)

# フッター
st.sidebar.markdown("---")
st.sidebar.write("バージョン: 1.0.0")
st.sidebar.write("© 2024 まつりな") 