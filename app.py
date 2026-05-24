import streamlit as st
import pandas as pd

# ページ設定：中央寄せ
st.set_page_config(page_title="商品検索", layout="centered")

# --- デザインカスタマイズ (CSS) ---
st.markdown("""
    <style>
    /* 1. ヘッダーとメニューを完全に非表示 */
    header[data-testid="stHeader"], #MainMenu, footer {display: none !important;}
    
    /* 2. スマホ画面の横揺れ防止 */
    .block-container {
        width: 100% !important;
        max-width: 100% !important;
        padding: 1.5rem 1rem 1rem 1rem !important;
        overflow-x: hidden !important; 
    }

    /* 3. アプリタイトル */
    .app-title {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #1E293B;
        margin-bottom: 0.5rem !important;
    }

    /* 4. ★修正部分★ 検索窓コンテナ全体を「約5文字分（160px）」まで縮める */
    div[data-testid="stHorizontalBlock"] {
        position: relative !important;
        width: 160px !important; /* 全体の幅をガッツリ短く固定 */
        display: flex !important;
        align-items: center !important;
        margin-bottom: 10px !important;
    }
    
    /* カラム1（検索窓本体）：160pxの枠内でいっぱいまで広げる */
    div[data-testid="column"]:nth-of-type(1) { 
        width: 100% !important; 
        flex: 1 1 100% !important; 
        min-width: 0 !important; 
    }
    
    /* ★修正部分★ カラム2（件数）：検索窓の「内側（右端）」に絶対配置で重ねる */
    div[data-testid="column"]:nth-of-type(2) { 
        position: absolute !important;
        right: 12px !important; /* 検索窓の右枠から少し内側に配置 */
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: auto !important; 
        z-index: 10 !important;
        pointer-events: none !important; /* タップの邪魔をしない */
    }

    /* 検索文字が「件数」に被らないよう、入力欄の右側に余白(padding)を設ける */
    div[data-baseweb="input"] input {
        padding-right: 45px !important;
    }

    /* 件数のテキストデザイン（入力欄に馴染むよう少し小さく・グレーに） */
    .hit-count {
        color: #64748b;
        font-size: 14px;
        font-weight: bold;
        margin: 0;
        white-space: nowrap;
    }

    /* 5. 表の余計な機能（拡大アイコン等）を消す */
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
    
    # st.columnsで枠を作り、CSSで重ね合わせる
    col1, col2 = st.columns(2) 
    with col1:
        query = st.text_input("検索", label_visibility="collapsed", placeholder="例: いちご")

    if query:
        qh = kata_to_hira(query); qk = hira_to_kata(query)
        def match(row):
            s = " ".join(map(str, row))
            return (qh in kata_to_hira(s)) or (qk in hira_to_kata(s))
        
        res = df[df.apply(match, axis=1)]
        
        # 内側にめり込ませる「件数」の表示
        with col2:
            st.markdown(f'<p class="hit-count">{len(res)}件</p>', unsafe_allow_html=True)
        
        if not res.empty:
            cols = res.columns[:2].tolist()
            
            # ★修正部分★：呼出しNo.の列幅をさらに半分(50ピクセル)に縮小して固定
            col_config = {
                cols[0]: st.column_config.Column(width=50), 
                cols[1]: st.column_config.Column(width="large")
            }
            
            st.dataframe(res[cols], use_container_width=True, hide_index=True, column_config=col_config)
        else:
            st.error("見つかりませんでした")
    else:
        st.info("入力を待機中...")

except Exception as e:
    st.error("データの読み込みに失敗しました")
