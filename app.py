import streamlit as st
import pandas as pd

# 1. ページの設定（横幅を広く設定）
st.set_page_config(page_title="商品検索アプリ", layout="wide")

# タイトルのみを表示（説明文は削除しました）
st.title("🔍 商品検索アプリ")

# 正しいスプレッドシートのURL
url = "https://docs.google.com/spreadsheets/d/17zsMWCLzo-xUFg_16WGKSEqpFWCLsRCb82EBiml4BiM/export?format=xlsx"

@st.cache_data(ttl="1m")  # 1分ごとに最新データを読み直す
def get_data():
    return pd.read_excel(url)

try:
    # データの読み込み
    df = get_data()
    
    # 2. 検索窓の文字を変更 ＆ CSSを使って文字を4ポイント大きく設定
    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"] label p {
            font-size: 20px !important; /* 元のサイズから約4ポイント大きく変更 */
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
        # 全列を対象に検索
        mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
        result = df[mask]
        
        if not result.empty:
            st.success(f"{len(result)} 件見つかりました。")
            
            # 【重要】「呼び出しNo.」と「品名」の2列だけを抽出して表示
            # スプレッドシートの実際の列名に合わせて自動で選択します
            available_columns = result.columns.tolist()
            display_cols = []
            
            # 「呼び出しNo.」に近い列名を探す
            no_col = [c for c in available_columns if "呼出し" in str(c) or "No" in str(c) or "no" in str(c)]
            if no_col:
                display_cols.append(no_col[0])
                
            # 「品名」に近い列名を探す
            name_col = [c for c in available_columns if "品名" in str(c) or "商品" in str(c)]
            if name_col:
                display_cols.append(name_col[0])
            
            # もし上記で見つからなければ、存在する最初の2列を表示
            if not display_cols:
                display_cols = available_columns[:2]
                
            # 2列だけに絞り込んだ表を大きく表示
            st.dataframe(result[display_cols], use_container_width=True)
        else:
            st.warning("一致する商品が見つかりませんでした。違うキーワードを試してください。")
    else:
        # 4. 検索前は何も表示しない（案内文のみ）
        st.info("上の検索窓に品名を入力すると、ここに結果が表示されます。")

except Exception as e:
    st.error("データの読み込みに失敗しました。時間をおいてページを再読み込みしてください。")
