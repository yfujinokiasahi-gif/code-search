import streamlit as st
import pandas as pd

# 1. ページの設定（横幅を広く設定）
st.set_page_config(page_title="商品検索アプリ", layout="wide")

# タイトルのみを表示（説明文は削除）
st.title("🔍 商品検索アプリ")

# 正しいスプレッドシートのURL
url = "https://docs.google.com/spreadsheets/d/17zsMWCLzo-xUFg_16WGKSEqpFWCLsRCb82EBiml4BiM/export?format=xlsx"

@st.cache_data(ttl="1m")  # 1分ごとに最新データを読み直す
def get_data():
    return pd.read_excel(url)

try:
    # データの読み込み
    df = get_data()
    
    # 2. 検索窓の文字を変更 ＆ 文字を大きくする設定
    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"] label p {
            font-size: 20px !important; 
            font-weight: bold;
        }
        </style>
        """, 
        unsafe_allow_index=True
    )
    
    query = st.text_input("ここに「品名」を入力", key="search", placeholder="いちご、すいか、など...")

    st.markdown("---")

    # 3 & 4. 検索処理と表示の制限
    if query:
        # すべての列を対象に検索（大文字小文字を区別しない）
        mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
        result = df[mask]
        
        if not result.empty:
            st.success(f"{len(result)} 件見つかりました。")
            
            # 【確実な方法】エラーを防ぐため、スプレッドシートの「左から1番目と2番目の列」を強制的に取得します
            display_cols = result.columns[:2].tolist()
            
            # 2列だけに絞り込んだ表を大きく表示
            st.dataframe(result[display_cols], use_container_width=True)
        else:
            st.warning("一致する商品が見つかりませんでした。違うキーワードを試してください。")
    else:
        # 4. 検索前は何も表示しない
        st.info("上の検索窓に品名を入力すると、ここに結果が表示されます。")

except Exception as e:
    st.error("データの読み込みに失敗しました。時間をおいてページを再読み込みしてください。")
