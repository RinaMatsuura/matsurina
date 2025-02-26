import streamlit as st
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.header("@cosmeスクレイピング 🔍", divider="orange")

# 商品ID入力フォーム
default_id = "10205860"
product_id = st.text_input(
    "@cosmeの商品IDを入力してください。分からない場合は「💡 商品IDってどこに書いてあるの？」をクリックしてください。",
    value=default_id,
    help="@cosmeの商品ページURLから商品IDの数字部分のみを入力してください"
)

# URLの生成
base_url = f"https://www.cosme.net/products/{product_id}/review/?page="

# 生成されたURLを表示
st.caption(f"スクレイピング対象のURL: {base_url}1")

# ページ数入力フォーム
max_pages = st.number_input(
    "何ページまで取得しますか？",
    min_value=1,
    max_value=1000,
    value=3,
    step=1,
    help="取得したいページ数を入力してください（1以上の数値）"
)

# 実行ボタンを目立つように配置
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    start_button = st.button("🚀 スクレイピングを開始", use_container_width=True)

##########
results = []
##########

if start_button:
    # 実行状況を表示するコンテナ
    status_container = st.container()
    with status_container:
        st.markdown("### 実行状況")
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        try:
            # 処理開始メッセージ
            st.info("🔄 スクレイピングを開始します...")
            
            # 指定されたページ数までループ
            for i in range(1, max_pages + 1):
                load_url = base_url + str(i)
                
                # URLアクセス状況を表示
                progress_text.write(f"🌐 URL: {load_url} にアクセス中...")
                
                html = requests.get(load_url)
                soup = BeautifulSoup(html.content,"html.parser")

                review_count = 0
                reviews = soup.select("span.read-more a.cmn-viewmore")
                
                # レビューが見つからない場合はループを終了
                if not reviews:
                    st.warning(f"⚠️ ページ {i} にレビューが見つかりませんでした。ここまでのデータを処理します。")
                    break
                
                for element in reviews:
                    review_url = element.get("href")
                    
                    #取り出したURLの口コミを取り出す
                    review_html = requests.get(review_url)
                    soup = BeautifulSoup(review_html.content,"html.parser")
                    review_text = soup.select_one("p.read").get_text().strip()
                    
                    #スコア情報を取得
                    if soup.select_one("div.rating.clearfix p.reviewer-rating"):
                        score = soup.select_one("div.rating.clearfix p.reviewer-rating").extract().text
                        matches = re.findall(r"[0-9]+", score)
                        if matches:
                            score = int(matches[0])
                        else:
                            score = None
                    else:
                        score = None

                    # 年齢と肌タイプ情報を取得
                    age = None
                    skin_type = None
                    reviewer_info = soup.select_one("p.reviewer-info")
                    if reviewer_info:
                        info_text = reviewer_info.text
                        # 具体的な年齢（例：32歳）を検索
                        age_match = re.search(r'(\d+)歳', info_text)
                        if age_match:
                            age = age_match.group(0)  # "32歳" のように保存
                        else:
                            # 年代（例：40代前半）を検索
                            age_range_match = re.search(r'(\d+代[前中後半]*)', info_text)
                            if age_range_match:
                                age = age_range_match.group(0)  # "40代前半" のように保存
                        
                        # 肌タイプを検索（例：乾燥肌、混合肌、普通肌など）
                        skin_match = re.search(r'[/／]\s*([^/／\s]*肌)', info_text)
                        if skin_match:
                            skin_type = skin_match.group(1)
                        
                    results.append({
                        "score": score, 
                        "age": age,
                        "skin_type": skin_type,
                        "comment": review_text
                    })
                    review_count += 1
                    
                # 進捗状況を更新
                progress = int((i / max_pages) * 100)
                progress_bar.progress(progress)
                progress_text.write(f"✅ ページ {i}/{max_pages} の処理が完了 (進捗: {progress}%)")
                st.write(f"📝 {review_count}件のレビューを取得しました")
                
            # データフレーム作成と表示
            df = pd.DataFrame(results)
            st.success("🎉 データの取得が完了しました！")
            
            # 取得結果のサマリーを表示
            st.markdown("### 取得結果サマリー")
            st.write(f"- 実際に取得したページ数: {i}ページ")
            st.write(f"- 総レビュー数: {len(results)}件")
            
            # データプレビュー
            st.markdown("### データプレビュー")
            st.data_editor(df)
            
            # CSVダウンロードボタン
            st.markdown("### データのダウンロード")
            csv = df.to_csv(index=False).encode('shift-jis')
            st.download_button(
                label="📥 データをCSVでダウンロード",
                data=csv,
                file_name='cosme_reviews.csv',
                mime='text/csv',
            )
            
        except Exception as e:
            st.error(f"⚠️ エラーが発生しました: {str(e)}")
else:
    st.info("👆 上のボタンをクリックしてスクレイピングを開始してください")

# 使い方の説明を上部に移動
with st.expander("💡 商品IDってどこに書いてあるの？"):
    st.write("""
    1. @cosmeで対象商品のページを開く
    2. URLの「products/」の後の数字部分をコピー
    
    例）https://www.cosme.net/products/10212664/review
    　　→ 「10212664」が商品IDです
    """)

# 使い方の説明
with st.expander("💡 使い方"):
    st.write("""
    1. @cosmeの商品レビューページのURLを入力
    2. 取得したいページ数を入力
    3. 「スクレイピングを開始」ボタンをクリック
    4. データ取得が完了するまで待機
    5. 取得したデータを確認
    6. 必要に応じてCSVファイルをダウンロード
    """)

# フッター
st.sidebar.markdown("---")
st.sidebar.write("バージョン: 1.0.0")
st.sidebar.write("© 2024 まつりな")
