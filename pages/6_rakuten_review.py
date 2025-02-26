import streamlit as st
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

st.header("楽天市場レビュースクレイピング 🔍※準備中", divider="orange")

# 商品ID入力フォーム
default_id = "354955_10000308"
product_id = st.text_input(
    "楽天の商品IDを入力してください。分からない場合は「💡 商品IDってどこに書いてあるの？」をクリックしてください。",
    value=default_id,
    help="楽天市場の商品レビューページURLから商品IDを入力してください"
)

# URLの生成
base_url = f"https://review.rakuten.co.jp/item/1/{product_id}?p="

# 生成されたURLを表示
st.caption(f"スクレイピング対象のURL: {base_url}1")

# ページ数入力フォーム
max_pages = st.number_input(
    "何ページまで取得しますか？",
    min_value=1,
    max_value=100,
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
            
            # Chromeドライバーの設定
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # ヘッドレスモードで実行
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(options=chrome_options)
            wait = WebDriverWait(driver, 10)
            
            # 指定されたページ数までループ
            for i in range(1, max_pages + 1):
                load_url = base_url + str(i)
                
                # URLアクセス状況を表示
                progress_text.write(f"🌐 URL: {load_url} にアクセス中...")
                
                driver.get(load_url)
                time.sleep(3)  # ページの読み込みを待つ
                
                # レビュー要素が表示されるまで待機
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='review-detail']")))
                except:
                    st.warning(f"⚠️ ページ {i} にレビューが見つかりませんでした。ここまでのデータを処理します。")
                    break
                
                # レビューを取得
                reviews = driver.find_elements(By.CSS_SELECTOR, "div[class*='review-detail']")
                review_count = 0
                
                for review in reviews:
                    # レビュー本文を取得
                    try:
                        review_text = review.find_element(By.CSS_SELECTOR, "div[class*='review-body']").text.strip()
                    except:
                        continue
                    
                    # 評価を取得
                    score = None
                    try:
                        score_element = review.find_element(By.CSS_SELECTOR, "div[class*='review-rating'] span")
                        score_text = score_element.text.strip()
                        score_match = re.search(r'(\d+)', score_text)
                        if score_match:
                            score = int(score_match.group(1))
                    except:
                        pass
                    
                    # レビュアー情報を取得
                    age = None
                    gender = None
                    try:
                        reviewer_info = review.find_element(By.CSS_SELECTOR, "div[class*='reviewer-info']")
                        info_text = reviewer_info.text
                        
                        # 年齢を取得
                        age_match = re.search(r'(\d+)代', info_text)
                        if age_match:
                            age = f"{age_match.group(1)}代"
                            if "前半" in info_text:
                                age += "前半"
                            elif "後半" in info_text:
                                age += "後半"
                        
                        # 性別を取得
                        if "女性" in info_text:
                            gender = "女性"
                        elif "男性" in info_text:
                            gender = "男性"
                    except:
                        pass
                    
                    results.append({
                        "score": score,
                        "age": age,
                        "gender": gender,
                        "comment": review_text
                    })
                    review_count += 1
                
                # 進捗状況を更新
                progress = int((i / max_pages) * 100)
                progress_bar.progress(progress)
                progress_text.write(f"✅ ページ {i}/{max_pages} の処理が完了 (進捗: {progress}%)")
                st.write(f"📝 {review_count}件のレビューを取得しました")
            
            # ブラウザを閉じる
            driver.quit()

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
                file_name='rakuten_reviews.csv',
                mime='text/csv',
            )
            
        except Exception as e:
            st.error(f"⚠️ エラーが発生しました: {str(e)}")
else:
    st.info("👆 上のボタンをクリックしてスクレイピングを開始してください")

# 使い方の説明
with st.expander("💡 商品IDってどこに書いてあるの？"):
    st.write("""
    1. 楽天市場の商品レビューページを開く
    2. URLの「item/1/」の後の数字部分をコピー
    
    例）https://review.rakuten.co.jp/item/1/354955_10000308
    　　→ 「354955_10000308」が商品IDです
    """)

# フッター
st.sidebar.markdown("---")
st.sidebar.write("バージョン: 1.0.0")
st.sidebar.write("© 2024 まつりな") 
