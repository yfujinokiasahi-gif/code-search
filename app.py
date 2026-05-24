import streamlit as st
import pandas as pd

# ページ設定：中央寄せ
st.set_page_config(page_title="商品検索", layout="centered")

# --- デザインカスタマイズ (CSS) ---
st.markdown("""
    <style>
    /* 1. ヘッダーとメニューを完全に非表示 */
    header[data-testid="stHeader"], #MainMenu, footer {display: none !important;}
    
    /* 2. スマホ画面に100%フィットさせ、右側の謎の余白（横揺れ）を完全に防止 */
    .block-container {
        width: 100% !important;
        max-width: 100% !important;
        padding: 2rem 1rem 1rem 1rem !important; /* 上 右 下 左 の余白 */
        overflow-x: hidden !important; /* ★右側の余白を消す特効薬★ */
    }

    /* 3. アプリタイトル */
    .app-title {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #1E293B;
        margin-bottom: 0.5rem !important;
    }

    /* 4. 検索窓とヒット件数を絶対に横並びにしつつ、画面内に収める */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    /* 検索窓（左側） */
    div[data-testid="column"]:nth-of-type(1) { 
        width: 75% !important; 
        flex: 1 1 auto !important; 
        min-width: 0 !important; /* ★中身が画面外に押し出されるのを防ぐ★ */
    }
    
    /* 件数表示（右側） */
    div[data-testid="column"]:nth-of-type(2) { 
        width: 25% !important; 
        flex: 0 0 auto !important; 
        text-align: right !important;
        padding-left: 10px !important;
        min-width: 0 !important; /* ★中身が画面外に押し出されるのを防ぐ★ */
    }

    /* 5. 表の余計な機能（拡大・ダウンロードアイコン）を消す */
    [data-testid="stElementToolbar"] { display: none !important; }

    /* 6. 表の幅を画面に合わせる */
    [data-testid="stDataFrame"] { width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# アプリタイトル
st.markdown('<p class="app-title">🔍 商品検索アプリ</p>', unsafe_allow_html=True)

url = "https://docs.google.com/spreadsheets/d/17zsMWCLzo-xUFg_16WGKSEqpFWCLsRCb82EBiml4BiM/export?format=xlsx"

@st.cache_data(ttl="1m")
def get_data():
    return pd.read_excel(url)

# ひらがな・カタカナ変換ロジック
def hira_to_kata(text): return "".join([chr(ord(c) + 96) if "ぁ" <= c <= "ん" else c for c in text])
def kata_to_hira(text): return "".join([chr(ord(c) - 96) if "ァ" <= c <= "ン" else c for c in text])

try:
    df = get_data()
    
    # 検索窓と件数の表示エリア
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("検索", label_visibility="collapsed", placeholder="品名を入力 (例：いちご)")

    if query:
        qh = kata_to_hira(query); qk = hira_to_kata(query)
        def match(row):
            s = " ".join(map(str, row))
            return (qh in kata_to_hira(s)) or (qk in hira_to_kata(s))
        
        res = df[df.apply(match, axis=1)]
        
        # 件数の表示
        with col2:
            st.markdown(f"**{len(res)}** 件", unsafe_allow_html=True)
        
        if not res.empty:
            # 呼び出しNo.と品名の2列だけを表示
            cols = res.columns[:2].tolist()
            st.dataframe(res[cols], use_container_width=True, hide_index=True)
        else:
            st.error("見つかりませんでした")
    else:
        st.info("入力を待機中...")

except Exception as e:
    st.error("データの読み込みに失敗しました")
