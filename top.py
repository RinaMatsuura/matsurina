import streamlit as st
import os
from dotenv import load_dotenv

# 最初にページ設定を行う
st.set_page_config(
    page_title="松浦が実験のために色々できるページ",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# .envファイルを読み込む
load_dotenv(override=True)

def check_password():
    """パスワードチェックを行う"""
    def password_entered():
        """パスワードが正しいかチェック"""
        # 環境変数から認証情報を取得
        correct_username = os.environ.get('STREAMLIT_USERNAME')
        correct_password = os.environ.get('STREAMLIT_PASSWORD')
        
        # シンプルな文字列比較
        if (st.session_state["username"] == correct_username and 
            st.session_state["password"] == correct_password):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # CSSでサイドバーを完全に非表示（ログイン前）
    if "password_correct" not in st.session_state or not st.session_state["password_correct"]:
        st.markdown("""
            <style>
                [data-testid="collapsedControl"] {
                    display: none
                }
                section[data-testid="stSidebar"] {
                    display: none;
                }
            </style>
            """, unsafe_allow_html=True)
    
    # パスワードが未入力の場合、入力フォームを表示
    if "password_correct" not in st.session_state:
        st.title("🔒 ログイン")
        st.text_input("ユーザー名", key="username")
        st.text_input("パスワード", type="password", key="password")
        st.button("ログイン", on_click=password_entered)
        return False
    
    # パスワードが間違っている場合
    elif not st.session_state["password_correct"]:
        st.title("🔒 ログイン")
        st.text_input("ユーザー名", key="username")
        st.text_input("パスワード", type="password", key="password")
        st.button("ログイン", on_click=password_entered)
        st.error("ユーザー名またはパスワードが違います")
        return False
    
    # 認証成功
    return True

# パスワードチェック
if check_password():
    # タイトルとヘッダー
    st.title("松浦の実験するページ🧪")
    st.header("こんにちは :sunglasses:", divider="rainbow")

    # メインコンテンツ
    st.write("""
              - このページは松浦が余暇で作っているものなので、要望やエラーには本当に気まぐれにしか対応しません。ご了承ください。
              - 社内利用だけを想定して色々作っているので他社に配布しないでください。""")

    # 機能の説明
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔒 ハッシュ化")
        st.write("""
        - CSVファイルのデータをハッシュ化します
        - SHA-256
        - ハッシュ化したデータをCSVでダウンロードできます
        """)
        if st.button("ハッシュ化ページへ", type="primary", use_container_width=True):
            st.switch_page("pages/1_hashpage.py")

        st.subheader("🛒 Qoo10スクレイピング")
        st.write("""
        - Qoo10からレビューを取得！
        - アットコスメより取得スピードが早いよ
        - CSVでデータも取得できる
        """)
        if st.button("Qoo10スクレイピングページへ", type="primary", use_container_width=True):
            st.switch_page("pages/3_qoo10.py")

    with col2:
        st.subheader(":memo: @cosmeスクレイピング")
        st.write("""
        - @cosmeからレビューを取得！
        - 評価も取得できる
        - CSVでデータも取得できる
        """)
        if st.button("@cosmeスクレイピングページへ", type="primary", use_container_width=True):
            st.switch_page("pages/2_atcosme.py")

        st.subheader("📊 テキストマイニング")
        st.write("""
        - 分析したいテキストをアップロード
        - 分析したい品詞を選択
        - 分析結果をダウンロードできる！
        """)
        if st.button("テキストマイニングページへ", type="primary", use_container_width=True):
            st.switch_page("pages/4_textmining.py")

    # フッター
    st.sidebar.markdown("---")
    st.sidebar.write("バージョン: 1.0.0")
    st.sidebar.write("© 2024 まつりな")