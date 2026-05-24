import streamlit as st
import pandas as pd

# 1. ページの設定（タブレットで見やすいように横幅を広く設定）
st.set_page_config(page_title="商品検索アプリ", layout="wide")

# アプリのタイトルと説明
st.title("🔍 商品検索アプリ")
st.write("文字を入力すると、自動で絞り込まれます。データは自動で最新に更新されます。")

# 正しいスプレッドシートのURL（完全に組み込み済みです）
url = "https://docs.google.com/spreadsheets/d/17zsMWCLzo-xUFg_16WGKSEqpFWCLsRCb82EBiml4BiM/export?format=xlsx"

# 読み込みエラーを完全に回避するため、キャッシュの仕組みをよりシンプルな形に変更します
@st.cache_data(ttl="1m")  # 1分（1minute）ごとに最新データを読み直す設定
def get_data():
    return pd.read_excel(url)

try:
    # データの読み込みを実行
    df = get_data()
    
    # 2. 検索窓を大きく表示
    query = st.text_input("ここに「品名」や「キーワード」を入力してください", key="search", placeholder="いちご、すいか、など...")

    st.markdown("---")

    # 3. 検索処理
    if query:
        # すべての列を対象に、検索ワードが含まれている行を絞り込む
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
    st.error("データの読み込みに失敗しました。時間をおいてページを再読み込みしてください。")
    st.info(f"エラーの詳細: {e}")  # 万が一ダメだった場合に、何が原因か特定するための手がかりを表示します
