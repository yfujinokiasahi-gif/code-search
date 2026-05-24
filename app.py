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

    /* 4. 検索窓とヒット件数の横並び設定（隣に配置） */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        width: 100% !important;
        gap: 15px !important; /* 検索窓と件数の間のスペース */
        margin-bottom: 10px !important;
    }
    
    /* カラム1（検索窓）：短めに設定（全体の50%程度） */
    div[data-testid="column"]:nth-of-type(1) { 
        width: 50% !important; 
        flex: 0 0 50% !important; 
        min-width: 0 !important; 
    }
    
    /* カラム2（件数表示）：検索窓のすぐ右隣に配置 */
    div[data-testid="column"]:nth-of-type(2) { 
        width: auto !important; 
        flex: 1 1 auto !important; 
        text-align: left !important; /* 左寄せにして検索窓に近づける */
        white-space: nowrap !important; /* 折り返し防止 */
        min-width: 0 !important; 
    }

    /* 件数のテキストデザイン */
    .hit-count {
        color: #2da44e;
        font-size: 16px;
        font-weight: bold;
        margin: 0;
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
    
    # st.columnsで枠を作成
    col1, col2 = st.columns([1, 1]) # Python側の比率設定（CSSが優先）
    with col1:
        # Enterキーで検索が実行されるのは Streamlit の標準仕様
        query = st.text_input("検索", label_visibility="collapsed", placeholder="例: いちご")

    if query:
        qh = kata_to_hira(query); qk = hira_to_kata(query)
        def match(row):
            s = " ".join(map(str, row))
            return (qh in kata_to_hira(s)) or (qk in hira_to_kata(s))
        
        res = df[df.apply(match, axis=1)]
        
        # 検索窓の右隣に件数を表示
        with col2:
            st.markdown(f'<p class="hit-count">{len(res)}件</p>', unsafe_allow_html=True)
        
        if not res.empty:
            cols = res.columns[:2].tolist()
            
            # 呼出しNo.の列幅を固定（前回のご要望通り 50px）
            col_config = {
                cols[0]: st.column_config.Column(width=50), 
                cols[1]: st.column_config.Column(width="large")
            }
            
            st.dataframe(res[cols], use_container_width=True, hide_index=True, column_config=col_config)
        else:
            with col2:
                # 0件の場合も表示を揃える
                st.markdown('<p class="hit-count" style="color: #cf222e;">0件</p>', unsafe_allow_html=True)
            st.error("見つかりませんでした")
    else:
        st.info("文字を入力してEnterを押してください")

except Exception as e:
    st.error("データの読み込みに失敗しました")
