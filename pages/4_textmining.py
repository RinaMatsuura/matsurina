import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
from wordcloud import WordCloud
import MeCab
import tempfile
import os
from pathlib import Path
import matplotlib.font_manager as fm
from io import BytesIO

def get_font_path():
    """利用可能なフォントパスを取得"""
    # DejaVuフォントを優先的に使用
    dejavu_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if os.path.exists(dejavu_path):
        return dejavu_path
    
    # システムにインストールされているフォントを探す
    fonts = fm.findSystemFonts()
    
    # 日本語フォントを優先的に探す
    for font in fonts:
        try:
            if any(name in font.lower() for name in ['dejavu', 'gothic', 'mincho', 'noto', 'meiryo']):
                return font
        except:
            continue
    
    # DejaVuSans-Boldを最後の手段として使用
    return "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# MeCabの初期化をシンプルに
tagger = MeCab.Tagger()

st.header("テキスト分析 📊", divider="rainbow")

# ファイルアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

if uploaded_file is not None:
    try:
        # CSVファイルを読み込む（複数のエンコーディングを試す）
        try:
            # まずUTF-8で試す
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                # 次にShift-JISで試す
                uploaded_file.seek(0)  # ファイルポインタを先頭に戻す
                df = pd.read_csv(uploaded_file, encoding='shift-jis')
            except UnicodeDecodeError:
                # 最後にCP932で試す
                uploaded_file.seek(0)  # ファイルポインタを先頭に戻す
                df = pd.read_csv(uploaded_file, encoding='cp932')
        
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
                    # フォントパスの取得
                    font_path = get_font_path()
                    st.write(f"使用フォント: {font_path}")  # デバッグ用
                    
                    # ワードクラウドの生成
                    wordcloud = WordCloud(
                        background_color="white",
                        font_path=font_path,
                        width=800,
                        height=600,
                        regexp=r"[\w']+",
                        collocations=False,
                        min_font_size=10,
                        max_words=100
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
                    
                    # メモリ上でバイナリデータとして画像を保存
                    buf = BytesIO()
                    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
                    buf.seek(0)
                    
                    # ダウンロードボタン
                    btn = st.download_button(
                        label="📥 ワードクラウド画像をダウンロード",
                        data=buf,
                        file_name="wordcloud.png",
                        mime="image/png"
                    )

                except Exception as e:
                    st.error(f"ワードクラウドの生成中にエラーが発生しました: {str(e)}")
                    st.error("フォントパスを確認中...")
                    
                    try:
                        # システムフォントの一覧を表示（デバッグ用）
                        available_fonts = [f for f in fm.findSystemFonts()]
                        st.write("利用可能なフォント:", available_fonts[:5])  # 最初の5つだけ表示
                        
                    except Exception as e:
                        st.error(f"フォント情報の取得に失敗: {str(e)}")
                
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