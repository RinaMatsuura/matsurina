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
import japanize_matplotlib

def get_font_path():
    """利用可能なフォントパスを取得"""
    # Notoフォントを優先的に使用（Streamlit Cloudで利用可能）
    noto_paths = [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"
    ]
    
    for path in noto_paths:
        if os.path.exists(path):
            return path
    
    # IPAフォントを試す
    ipa_paths = [
        "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",
        "/usr/share/fonts/truetype/ipafont/ipag.ttf"
    ]
    
    for path in ipa_paths:
        if os.path.exists(path):
            return path
    
    # システムにインストールされているフォントを探す
    fonts = fm.findSystemFonts()
    
    # 日本語フォントを優先的に探す
    for font in fonts:
        try:
            if any(name in font.lower() for name in ['noto', 'ipa', 'gothic', 'mincho', 'meiryo']):
                return font
        except:
            continue
    
    # 最後の手段としてDejaVuを使用
    return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

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
        
        # ワードクラウド生成ボタン
        if st.button("🎨 ワードクラウドを生成"):
            with st.spinner("ワードクラウドを生成中..."):
                try:
                    # フォントパスの取得
                    font_path = get_font_path()
                    st.write(f"使用フォント: {font_path}")  # デバッグ用
                    
                    # ワードクラウドの生成
                    wordcloud = WordCloud(
                        font_path=font_path,
                        background_color="white",
                        width=800,
                        height=600,
                        regexp=r"[\w']+",
                        collocations=False,
                        min_font_size=10,
                        max_words=100,
                        prefer_horizontal=0.7,  # 横書きの比率を調整
                        font_step=1,  # フォントサイズの調整ステップを小さくする
                        normalize_plurals=False,  # 複数形の正規化を無効化
                        repeat=True  # 単語の繰り返しを許可
                    ).generate(" ".join(all_words))  # 単語リストを直接使用
                    
                    # プロットの作成
                    plt.rcParams['font.family'] = 'IPAexGothic'  # プロット全体のフォント設定
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
                    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, dpi=300)  # DPIを上げる
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