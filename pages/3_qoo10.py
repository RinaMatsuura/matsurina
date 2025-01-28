import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_reviews(base_url, max_pages=None):
    """Qoo10の全ページまたは指定ページ数までのレビューを取得する関数"""
    all_reviews = []
    page = 1
    
    try:
        while True:
            # 指定ページ数に達したら終了
            if max_pages and page > max_pages:
                break
                
            # ヘッダーを設定してブロックを回避
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # URLにページ番号を追加
            url = f"{base_url}#customerReview?page={page}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # レビューテキストを取得
            review_elements = soup.find_all('p', class_='review_txt')
            
            # レビューが見つからない場合は終了
            if not review_elements:
                break
                
            # レビューを追加
            for review in review_elements:
                all_reviews.append(review.text.strip())
            
            # ページング情報を取得
            paging = soup.find('div', id='pagingQA')
            if not paging:
                break
                
            # 進捗状況を表示
            st.write(f"ページ {page} を取得中...")
            
            # サーバーに負荷をかけないよう少し待機
            time.sleep(2)
            
            page += 1
            
        return all_reviews
        
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        return all_reviews  # エラーが発生しても、それまでに取得したレビューは返す

def main():
    st.title("Qoo10レビュー取得")
    
    # URLの入力
    url = st.text_input("Qoo10の商品URLを入力してください", "https://www.qoo10.jp/g/1018510911/")
    
    # ページ数の選択
    page_option = st.radio(
        "取得するページ数を選択してください",
        ["指定ページ数まで", "全ページ ※膨大な場合時間がかかります"],
        horizontal=True
    )
    
    max_pages = None
    if page_option == "指定ページ数まで":
        max_pages = st.number_input("取得するページ数", min_value=1, value=5, step=1)
    
    if st.button("レビューを取得"):
        with st.spinner("レビューを取得中..."):
            reviews = get_reviews(url, max_pages)
            
            if reviews:
                # レビュー数を表示
                st.success(f"{len(reviews)}件のレビューを取得しました！")
                
                # レビューを表示
                with st.expander("レビュー一覧"):
                    for i, review in enumerate(reviews, 1):
                        st.write(f"{i}. {review}")
                
                # CSVダウンロードボタン
                df = pd.DataFrame(reviews, columns=['レビュー'])
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="CSVでダウンロード",
                    data=csv,
                    file_name="qoo10_reviews.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()