import streamlit as st
import pandas as pd

# 【修正2】レイアウトを "centered" に変更し、全体をコンパクトにする
st.set_page_config(page_title="商品検索アプリ", layout="centered")

# 画面全体のデザイン調整（CSS）
st.markdown(
    """
    <style>
    /* 【修正1 & 2】サイト全体の幅を狭く固定（約350px）。これで検索窓が10文字程度の幅になります */
    .block-container { 
        max-width: 350px !important; 
        padding-top: 2rem !important; 
        padding-bottom: 0rem !important; 
        padding-left: 1rem !important; 
        padding-right: 1rem !important; 
    }
    
    div[data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
    div[data-testid="element-container"] { margin-bottom: 0rem !important; }
    
    /* 検索窓と件数の縦のズレを揃える */
    div[data-testid="stHorizontalBlock"] { 
        align-items: center !important; 
    }
    
    h4 { margin-bottom: 10px !important; margin-top: 4px !important; }

    /* 【修正4】表の右上に出るツールバー（ダウンロードや拡大アイコン）を非表示にする */
    [data-testid="stElementToolbar"] { 
        display: none !important; 
    }
    </style>
    """,
    unsafe_allow_html=True
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
    df = get_data()
    st.markdown("#### **ここに「品名」を入力**")
    
    # 検索窓と件数の横幅の割合を設定（3:1の比率）
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input(label="検索窓", label_visibility="collapsed", key="search", placeholder="いちご...")

    if query:
        query_hira = kata_to_hira(query)
        query_kata = hira_to_kata(query)
        
        def match_row(row):
            row_str = " ".join([str(x) for x in row])
            return (query_hira in kata_to_hira(row_str)) or (query_kata in hira_to_kata(row_str))

        mask = df.apply(match_row, axis=1)
        result = df[mask]
        
        if not result.empty:
            with col2:
                st.markdown(f"<p style='color: #2da44e; font-weight: bold; font-size: 15px; margin: 0; white-space: nowrap;'>{len(result)}件</p>", unsafe_allow_html=True)
            
            display_cols = result.columns[:2].tolist()
            
            # 【修正3】use_container_width=True に変更し、表の幅を検索窓（コンテナ）の幅にぴったり合わせる
            st.dataframe(result[display_cols], use_container_width=True, hide_index=True)
        else:
            with col2:
                st.markdown("<p style='color: #cf222e; font-weight: bold; font-size: 15px; margin: 0; white-space: nowrap;'>0件</p>", unsafe_allow_html=True)
    else:
        st.info("上の検索窓に品名を入力すると、ここに結果が表示されます。")

except Exception as e:
    st.error(f"データの読み込みに失敗しました。再読み込みしてください。 (詳細: {e})")
