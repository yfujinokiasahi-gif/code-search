import streamlit as st
import pandas as pd

# 1. ページの設定（タブレットで見やすいように横幅を広く設定）
st.set_page_config(page_title="商品検索アプリ", layout="wide")

# アプリのタイトルと説明
st.title("🔍 商品検索アプリ")
st.write("文字を入力すると、自動で絞り込まれます。データは1分ごとに最新に更新されます。")

# あなたのGoogleスプレッドシートのURL
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/17zsMWCLzo-xUFg_16WGKSEqpFWCLsRCb82EBiml4BiM/export?format=xlsx"

# 【超重要】ttl=60 を追加して、1分（60秒）経ったら自動で最新データを読み直す設定にします
@st.cache_data(ttl=60)
def load_data():
    return pd.read_excel(SPREADSHEET_URL)

try:
    df = load_data()
    
    # 2. 検索窓を大きく表示（パートさんが押しやすい位置に）
    query = st.text_input("ここに「品名」や「キーワード」を入力してください", key="search", placeholder="いちご、すいか、など...")

    st.markdown("---")

    # 3. 検索処理
    if query:
        # すべての列を対象に、検索ワードが含まれている行を絞り込む（大文字小文字を区別しない）
        mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
        result = df[mask]
        
        if not result.empty:
            st.success(f"項目が {len(result)} 件見つかりました。")
            # タブレットの画面いっぱいに大きな表で表示
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("一致する商品が見つかりませんでした。違うキーワードを試してください。")
    else:
        # 何も入力されていない時は全件表示
        st.write("【商品リスト一覧】")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("データの読み込みに失敗しました。スプレッドシートの共有設定やURLを確認してください。")
