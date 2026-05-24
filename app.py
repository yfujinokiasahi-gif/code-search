import streamlit as st
import pandas as pd

# ページ設定：中央寄せ
st.set_page_config(page_title="商品検索", layout="centered")

# --- デザインカスタマイズ (CSS) ---
st.markdown("""
    <style>
    /* 1. ヘッダーとメニューを完全に非表示 */
    header[data-testid="stHeader"], #MainMenu, footer {display: none !important;}
    
    /* 2. スマホ画面に100%フィット（横揺れ・右の余白を完全に防止） */
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

    /* 4. 検索窓と件数は「縦並び（標準）」に戻すため、横並び強制のCSSは削除 */
    
    /* 件数のテキストデザイン */
    .hit-count {
        color: #2da44e;
        font-size: 16px;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 10px;
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
    
    # 横並びのカラム（st.columns）をやめ、シンプルに上から順に配置
    query = st.text_input("検索", label_visibility="collapsed", placeholder="品名を入力 (例: いちご)")

    if query:
        qh = kata_to_hira(query); qk = hira_to_kata(query)
        def match(row):
            s = " ".join(map(str, row))
            return (qh in kata_to_hira(s)) or (qk in hira_to_kata(s))
        
        res = df[df.apply(match, axis=1)]
        
        # 検索窓の「下」に件数を表示（確実に全文字表示されます）
        st.markdown(f'<p class="hit-count">{len(res)}件</p>', unsafe_allow_html=True)
        
        if not res.empty:
            cols = res.columns[:2].tolist()
            
            # 呼出しNo.の列幅を狭く（50px）固定する設定は継続
            col_config = {
                cols[0]: st.column_config.Column(width=50), 
                cols[1]: st.column_config.Column(width="large")
            }
            
            st.dataframe(res[cols], use_container_width=True, hide_index=True, column_config=col_config)
        else:
            st.error("見つかりませんでした")
    else:
        st.info("文字を入力してEnterを押してください")

except Exception as e:
    st.error("データの読み込みに失敗しました")
