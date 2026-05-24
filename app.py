import streamlit as st
import pandas as pd

# 1. ページの設定（横幅を広く設定）
st.set_page_config(page_title="商品検索アプリ", layout="wide")

# 【今回の目玉】余白を限界まで削り、スマホでも横並びを強制する魔法の設定
st.markdown(
    """
    <style>
    /* 1. 画面上部・左右の余白を限界まで削る */
    .block-container {
        padding-top: 0.4rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    /* 2. パーツ同士の上下の間隔（すき間）を極限まで詰める */
    div[data-testid="stVerticalBlock"] {
        gap: 0.1rem !important;
    }
    div[data-testid="element-container"] {
        margin-bottom: 0rem !important;
    }
    /* 3. スマホ画面でも検索窓と件数表示が「縦に崩れず横並び」になるように強制 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        margin-top: -0.4rem !important;
    }
    div[data-testid="column"]:nth-of-type(1) {
        flex: 3 1 0% !important; /* 検索窓を広めに */
    }
    div[data-testid="column"]:nth-of-type(2) {
        flex: 1.5 1 0% !important; /* 件数表示エリア */
        padding-left: 10px !important;
    }
    </style>
    """,
    unsafe_allow_index=True
)

# タイトル
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
    
    # 2. 検索窓のタイトル部分
    st.markdown("#### **ここに「品名」を入力**")
    
    # 検索窓と件数を横並びにするための枠組み（レイアウト）を作成
    col1, col2 = st.columns([3, 1.5])
    
    with col1:
        query = st.text_input(label="検索窓", label_visibility="collapsed", key="search", placeholder="いちご、すいか、など...")

    # 3 & 4. 検索処理と表示の制限
    if query:
        # 入力された文字のひらがな版・カタカナ版を用意
        query_hira = kata_to_hira(query)
        query_kata = hira_to_kata(query)
        
        def match_row(row):
            row_str = " ".join([str(x) for x in row])
            return (query_hira in kata_to_hira(row_str)) or (query_kata in hira_to_kata(row_str))

        mask = df.apply(match_row, axis=1)
        result = df[mask]
        
        if not result.empty:
            # 【変更点】大きな緑枠（st.success）をやめ、検索窓のすぐ右側（col2）に、小さく綺麗な緑文字で件数を表示
            with col2:
                st.markdown(f"<p style='color: #2da44e; font-weight: bold; font-size: 15px; margin: 0; white-space: nowrap;'>{len(result)}件見つかりました。</p>", unsafe_allow_index=True)
            
            # スプレッドシートの「左から1番目と2番目の列（呼び出しNo.と品名）」を取得
            display_cols = result.columns[:2].tolist()
            
            # 2列だけに絞り込んだ表を表示
            st.dataframe(
                result[display_cols], 
                use_container_width=False,  # 自動引き伸ばしを無効化
                hide_index=True,           # 行番号を非表示
                column_config={
                    display_cols[0]: st.column_config.Column(width=100),  # 呼出しNo.を「5桁固定」の幅に指定
                    display_cols[1]: st.column_config.Column(width=600)   # 品名を「ゆったり広め」の幅に固定
                }
            )
        else:
            with col2:
                st.markdown("<p style='color: #cf222e; font-weight: bold; font-size:
