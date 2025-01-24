import streamlit as st
import hmac

def check_password():
    """パスワードチェックを行う"""
    def password_entered():
        """パスワードが正しいかチェック"""
        if hmac.compare_digest(st.session_state["username"], "matsuri") and \
           hmac.compare_digest(st.session_state["password"], "test123"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # パスワードを削除
            del st.session_state["username"]  # ユーザー名を削除
        else:
            st.session_state["password_correct"] = False

    # ログイン前はサイドバーを非表示
    st.set_page_config(
        page_title="ログイン",
        page_icon="🔒",
        initial_sidebar_state="collapsed"
    )
    
    # CSSでサイドバーを完全に非表示
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
    # ログイン後のページ設定
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
              - このページたちは松浦が余暇で作ってるものなので、要望やエラーには本当に気が向いたらしか対応しません。ご了承ください。
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