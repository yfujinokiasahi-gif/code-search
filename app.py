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

    /* 4. ヒット件数のデザイン */
    .hit-count {
        color: #2da44e;
        font-size: 15px;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 10px;
    }

    /* 5. タブ（シート切り替えボタン）のデザイン微調整 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 38px;
        white-space: nowrap;
        background-color: #f8fafc;
        border-radius: 4px 4px 0px 0px;
        padding: 0px 16px;
        font-size: 14px;
    }

    /* 6. 表の余計な機能（拡大アイコン等）を消す */
    [data-testid="stElementToolbar"] { display: none !important; }
    
    /* 7. 表の幅を画面に合わせる */
    [data-testid="stDataFrame"] { width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# アプリタイトル
st.markdown('<p class="app-title">🔍 商品検索アプリ</p>', unsafe_allow_html=True)

url = "https://docs.google.com/spreadsheets/d/17zsMWCLzo-xUFg_16WGKSEqpFWCLsRCb82EBiml4BiM/export?format=xlsx"

@st.cache_data(ttl="1m")
def get_all_sheets():
    # 全シートを辞書形式（シート名: データフレーム）で一括読み込み
    return pd.read_excel(url, sheet_name=None)

# ひらがな・カタカナ変換ロジック
def hira_to_kata(text): return "".join([chr(ord(c) + 96) if "ぁ" <= c <= "ん" else c for c in text])
def kata_to_hira(text): return "".join([chr(ord(c) - 96) if "ァ" <= c <= "ン" else c for c in text])

try:
    # データの取得
    sheets_dict = get_all_sheets()
    sheet_names = list(sheets_dict.keys())
    
    # 検索窓をタブの上に「1つだけ」配置（これで全シートが同時に検索されます）
    query = st.text_input("検索", label_visibility="collapsed", placeholder="品名を入力 (例: いちご)")

    # シート名のタブボタンを作成
    tabs = st.tabs(sheet_names)
    
    # 各タブの中身をループで作成
    for i, tab in enumerate(tabs):
        sheet_name = sheet_names[i]
        df = sheets_dict[sheet_name]
        
        with tab:
            if query:
                qh = kata_to_hira(query)
                qk = hira_to_kata(query)
                
                # 検索ロジック
                def match(row):
                    s = " ".join(map(str, row))
                    return (qh in kata_to_hira(s)) or (qk in hira_to_kata(s))
                
                res = df[df.apply(match, axis=1)]
                
                # 件数表示
                st.markdown(f'<p class="hit-count">{len(res)}件 ヒット</p>', unsafe_allow_html=True)
                
                if not res.empty:
                    cols = res.columns[:2].tolist()
                    
                    # 1列目の width を None に指定することで、中身と見出し（呼出No.）に合わせて自動サイズ調整（Autosize）されます。
                    # 2列目は引き続き width=1000 とすることで、大画面でも残りのスペースがすべて品名に割り当てられます。
                    col_config = {
                        cols[0]: st.column_config.Column(label="呼出No.", width=None), 
                        cols[1]: st.column_config.Column(label="品名", width=1000)
                    }
                    
                    # height=550 を指定することで、PCやタブレット表示時にも表が長くスクロールしやすくなります
                    st.dataframe(
                        res[cols], 
                        use_container_width=True, 
                        hide_index=True, 
                        column_config=col_config,
                        height=550
                    )
                else:
                    st.error("見つかりませんでした")
            else:
                st.info("文字を入力してEnterを押してください")

except Exception as e:
    st.error("データの読み込みに失敗しました")
