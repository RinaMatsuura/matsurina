import streamlit as st
import hashlib
import pandas as pd

##タイトルに区切り線を引く
st.header("csvデータをハッシュ化:sunglasses:", divider="orange")

def hash_value(value):
    """個々の値をSHA-256でハッシュ化する"""
    # 数値やNaNを文字列に変換
    value = str(value)
    if pd.isna(value):
        return value
    return hashlib.sha256(value.encode()).hexdigest()

uploaded_file = st.file_uploader("アップロードされたデータをSHA-256でハッシュ化するよ", type=["csv"])

if uploaded_file is not None:
    try:
        # CSVファイルを読み込む
        df = pd.read_csv(uploaded_file, encoding='shift-jis')
        
        # オリジナルのデータを表示
        st.write("元のデータのプレビュー:")
        st.data_editor(df)
        
        # ハッシュ化するカラムを選択
        columns_to_hash = st.multiselect(
            "ハッシュ化するカラムを選択してください",
            df.columns.tolist()
        )
        
        if columns_to_hash:  # カラムが選択されている場合
            # 選択されたカラムのみをハッシュ化
            hashed_df = df.copy()
            for column in columns_to_hash:
                hashed_df[column] = df[column].apply(hash_value)
            
            # ハッシュ化したデータを表示
            st.write("ハッシュ化したデータはこちらです:")
            st.data_editor(hashed_df)
            
            # 選択されたカラムのみのデータフレームを作成
            selected_df = hashed_df[columns_to_hash]
            
            # 選択されたカラムのみをCSVでダウンロード
            csv = selected_df.to_csv(index=False).encode('shift-jis')
            st.download_button(
                label="ハッシュ化したカラムをCSVでダウンロード",
                data=csv,
                file_name='hashed_columns.csv',
                mime='text/csv',
            )
        else:
            st.info("ハッシュ化するカラムを選択してください")

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
else:
    st.write("ファイルをアップロードしてください。頭のセルはラベルにしてください")

# フッター
st.sidebar.markdown("---")
st.sidebar.write("バージョン: 1.0.0")
st.sidebar.write("© 2024 まつりな")
