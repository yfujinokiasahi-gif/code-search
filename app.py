import streamlit as st
import pandas as pd

# ページの設定（タブレットで見やすいように横幅を広く設定）
st.set_page_config(page_title="商品検索アプリ", layout="wide")

# アプリのタイトル
st.title("🔍 商品検索アプリ")
st.write("文字を入力すると、自動で絞り込まれます。")

# GoogleスプレッドシートのURL（後であなたのURLに書き換えます）
# ※デモ用に公開データを入れています
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/17zsMWCLzo-xUFg_16WGKSEqpFWCLsRCb82EBiml4BiM/export?format=xlsx"
@st.cache_data(ttl=60) # 60秒間データをキャッシュ（更新を反映しつつ動きを軽くする）
def load_data():
    # Excel（スプレッドシート）を読み込む
    return pd.read_excel(SPREADSHEET_URL)

try:
    df = load_data()
    
    # 検索窓を大きく表示
    query = st.text_input("ここに「品名」や「キーワード」を入力してください", key="search", placeholder="いちご、すいか、など...")

    st.markdown("---")

    # 検索処理
    if query:
        # 全ての列を対象に、文字が含まれているか検索（大文字小文字を区別しない）
        mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
        result = df[mask]
        
        if not result.empty:
            st.success(f"項目が {len(result)} 件見つかりました。")
            # パートさんが見やすいように大きな表で表示
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("一致する商品が見つかりませんでした。")
    else:
        # 何も入力されていない時は全件表示
        st.write("【商品リスト一覧】")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("データの読み込みに失敗しました。URLが正しいか確認してください。")
