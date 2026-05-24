import streamlit as st
import pandas as pd

# 1. ページの設定（横幅を広く設定）
st.set_page_config(page_title="商品検索アプリ", layout="wide")

# タイトル（サイズ微調整済み）
st.markdown("### **🔍 商品検索アプリ**")

# 正しいスプレッドシートのURL
url = "https://docs.google.com/spreadsheets/d/17zsMWCLzo-xUFg_16WGKSEqpFWCLsRCb82EBiml4BiM/export?format=xlsx"

@st.cache_data(ttl="1m")  # 1分ごとに最新データを読み直す
def get_data():
    return pd.read_excel(url)

# ひらがな ⇔ カタカナの変換関数
def hira_to_kata(text):
    return "".join([chr(ord(c) + 96) if "ぁ" <= c <= "ん" else c for c in text])

def kata_to_hira(text):
    return "".join([chr(ord(c) - 96) if "ァ" <= c <= "ン" else c for c in text])

try:
    # データの読み込み
    df = get_data()
    
    # 2. 検索窓のタイトル部分（サイズ微調整済み）
    st.markdown("#### **ここに「品名」を入力**")
    query = st.text_input(label="検索窓", label_visibility="collapsed", key="search", placeholder="いちご、すいか、など...")

    st.markdown("---")

    # 3 & 4. 検索処理と表示の制限
    if query:
        # 入力された文字のひらがな版・カタカナ版を用意
        query_hira = kata_to_hira(query)
        query_kata = hira_to_kata(query)
        
        # 行全体のデータを確実に文字列に変換して検索する処理（エラー回避対策）
        def match_row(row):
            # 空欄や数字があっても、すべて確実に文字(str)に変換して結合します
            row_str = " ".join([str(x) for x in row])
            return (query_hira in kata_to_hira(row_str)) or (query_kata in hira_to_kata(row_str))

        mask = df.apply(match_row, axis=1)
        result = df[mask]
        
        if not result.empty:
            st.success(f"{len(result)} 件見つかりました。")
            
            # スプレッドシートの「左から1番目と2番目の列」だけを取得
            display_cols = result.columns[:2].tolist()
            
            # 2列だけに絞り込んだ表を大きく表示
            st.dataframe(result[display_cols], use_container_width=True)
        else:
            st.warning("一致する商品が見つかりませんでした。違うキーワードを試してください。")
    else:
        # 4. 検索前は何も表示しない
        st.info("上の検索窓に品名を入力すると、ここに結果が表示されます。")

except Exception as e:
    st.error(f"データの読み込みに失敗しました。時間をおいてページを再読み込みしてください。 (詳細: {e})")
