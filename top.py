import streamlit as st

# 最初にページ設定を行う
st.set_page_config(
    page_title="松浦のテストページ",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# タイトルとヘッダー
st.title("松浦のテストページ 🏠")
st.header("こんにちは :sunglasses:", divider="rainbow")

# メインコンテンツ
st.write("""
          - このページたちは松浦が余暇で作ってるものなので、要望やエラーには本当に気まぐれにしか対応しません。ご了承ください。
          - 社内利用だけを想定して色々作っているので他社に配布しないでください。""")

# 機能の説明
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔒 ハッシュ化")
    st.write("""
    - CSVファイルのデータをハッシュ化します
    - SHA-256
    - ハッシュ化したデータをCSVでダウンロードできます
    """)
    if st.button("ハッシュ化ページへ", type="primary", use_container_width=True):
        st.switch_page("pages/1_hashpage.py")

with col2:
    st.subheader(":memo: @cosmeスクレイピング")
    st.write("""
    - @cosmeからレビューを取得！
    - 評価も取得できる
    - csvでデータも取得できる
    """)
    if st.button("@cosmeスクレイピングページへ", type="primary", use_container_width=True):
        st.switch_page("pages/2_atcosme.py")

with col3:
    st.subheader("📊 テキストマイニング")
    st.write("""
    - 分析したいテキストをアップロード
    - 分析したい品詞を選択
    - 分析結果をダウンロードできる！
    """)
    if st.button("テキストマイニングページへ", type="primary", use_container_width=True):
        st.switch_page("pages/3_textmining.py")

# フッター
st.sidebar.markdown("---")
st.sidebar.write("バージョン: 1.0.0")
st.sidebar.write("© 2024 まつりな")