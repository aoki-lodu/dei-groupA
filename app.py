import streamlit as st
import pandas as pd

# ==========================================
# 0. 設定 & データ定義
# ==========================================
st.set_page_config(page_title="LODU Game", layout="wide", initial_sidebar_state="expanded")

# カスタムCSS
st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    /* 一括削除ボタン隠し */
    [data-testid="stMultiselect"] div[data-baseweb="select"] > div:nth-last-child(1) {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ゲームデータ
ICONS = {"くらし(💚)": "💚", "キャリア(📖)": "📖", "グローバル(🌏)": "🌏", "アイデンティティ(🌈)": "🌈", "フェア(⚖️)": "⚖️"}
RISK_MAP_DISPLAY = {
    "1": "🎉 セーフ",
    "2": "💚 くらし",
    "3": "📖 キャリア",
    "4": "🌏 グローバル",
    "5": "🌈 アイデンティティ",
    "6": "⚖️ フェア"
}

CHARACTERS_DB = [
    {"name": "白石 凛子", "base": 3, "icons": ["🌏", "🌈"], "role": "Manager"},
    {"name": "山本 大翔", "base": 2, "icons": ["🌈"], "role": "Staff"},
    {"name": "川瀬 美羽", "base": 1, "icons": ["💚", "📖", "🌈"], "role": "Newbie"},
    {"name": "Hanna Schmidt", "base": 2, "icons": ["💚", "🌏", "⚖️"], "role": "Specialist"},
    {"name": "宮下 慧", "base": 3, "icons": ["📖", "🌈"], "role": "Expert"},
    {"name": "川口 由衣", "base": 3, "icons": ["📖"], "role": "Leader"},
]

POLICIES_DB = [
    {"name": "ペアワーク＆コードレビュー", "target": ["📖", "🌈"], "power": 2, "type": ["promote"]},
    {"name": "時短・コア短縮", "target": ["💚"], "power": 2, "type": ["shield", "recruit"]},
    {"name": "二言語テンプレ＆用語集", "target": ["🌏"], "power": 1, "type": ["recruit"]},
    {"name": "ERG経営提言", "target": ["⚖️"], "power": 1, "type": ["promote"]},
    {"name": "透明な評価会(校正)", "target": ["🌈", "⚖️"], "power": 0, "type": ["shield", "promote"]},
    {"name": "アクセシブルツール支給", "target": ["💚"], "power": 2, "type": ["shield"]},
    {"name": "リターンシップ", "target": ["📖", "💚"], "power": 0, "type": ["recruit", "promote"]},
    {"name": "ATSバイアスアラート", "target": ["📖", "🌈"], "power": 0, "type": ["recruit"]},
]

# ==========================================
# 1. サイドバー
# ==========================================
with st.sidebar:
    st.header("🎮 ゲーム操作盤")
    st.info("👇 メンバーや施策を選んでください")
    
    # ここでエラーが出ていたので、書き方を修正しました
    character_names = [c["name"] for c in CHARACTERS_DB]
    selected_char_names = st.multiselect(
        "👤 参加メンバー",
        options=character_names,
        default=character_names[:3]
    )
    
    st.divider()
    
    policy_names = [p["name"] for p in POLICIES_DB]
    selected_policy_names = st.multiselect(
        "🃏 実行した施策",
        options=policy_names,
        default=[]
    )

active_chars = [c for c in CHARACTERS_DB if c["name"] in selected_char_names]
active_policies = [p for p in POLICIES_DB if p["name"] in selected_policy_names]

# ==========================================
# 2. 計算ロジック
# ==========================================
total_power = 0
active_shields = set()
active_recruits = set() # 採用ターゲットのセット

# 施策の効果を集計
for pol in active_policies:
    # 離職防止（盾）
    if "shield" in pol["type"]:
        for t in pol["target"]:
            active_shields.add(t)
    # 採用（ターゲット）
    if "recruit" in pol["type"]:
        for t in pol["target"]:
            active_recruits.add(t)

char_results = []
for char in active_chars:
    current_power = char["base"]
    status_tags = []
    
    for pol in active_policies:
        if set(char["icons"]) & set(pol["target"]):
            current_power += pol["power"]
            if "promote" in pol["type"] and "🟢昇進" not in status_tags: status_tags.append("🟢昇進")
            if "recruit" in pol["type"] and "🔵採用" not in status_tags: status_tags.append("🔵採用")
            
    risks = [icon for icon in char["icons"] if icon not in active_shields]
    is_safe = len(risks) == 0 
    
    total_power += current_power
    char_results.append({
        "data": char,
        "power": current_power,
        "tags": status_tags,
        "risks": risks,
        "is_safe": is_safe
    })

# ==========================================
# 3. メイン画面レイアウト
# ==========================================
st.title("🎲 DE&I 組織シミュレーター")

# スコアボード（4列に変更しました）
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("🏆 チーム仕事力", f"{total_power} pt")
with c2:
    # 離職防止（旧ガード）
    shield_text = " ".join(sorted(list(active_shields))) if active_shields else "ー"
    st.metric("🛡️ 離職防止中", shield_text)
with c3:
    # 【追加】採用強化中の属性を表示
    recruit_text = " ".join(sorted(list(active_recruits))) if active_recruits else "ー"
    st.metric("🔵 採用強化中", recruit_text)
with c4:
    st.metric("👥 メンバー数", f"{len(active_chars)} 名")

st.divider()

with st.expander("🎲 サイコロの出目対応表を見る"):
    cols = st.columns(6)
    for i, (num, desc) in enumerate(RISK_MAP_DISPLAY.items()):
        with cols[i]:
            st.markdown(f"**{num}**: {desc}")

st.subheader("📊 組織メンバーの状態")
st.caption("リアルサイコロを振って、🟥 赤い枠 のメンバーの属性が出たら離職です。")

cols = st.columns(3)
if not char_results:
    st.info("👈 サイドバーからメンバーを追加してください")
else:
    for i, res in enumerate(char_results):
        with cols[i % 3]:
            # 配色設定
            if res["is_safe"]:
                border_color = "#00c853"
                bg_color = "#e8f5e9"
                header_text = "🛡️ SAFE (離職防止)" 
                footer_text = "✅ 離職防止 成功中"
                footer_color = "#00c853"
            else:
                border_color = "#ff1744"
                bg_color = "#ffebee"
                header_text = "⚠️ RISK (危険)"
                risk_icons = " ".join(res['risks'])
                # 😱を削除し、テキストをシンプルに
                footer_text = f"{risk_icons} が出たらアウト" 
                footer_color = "#ff1744"

            bar_width = min(res['power'] * 10, 100)
            
            tags_html = ""
            for tag in res["tags"]:
                tags_html += f"<span style='background:#fff; border:1px solid #ccc; border-radius:4px; padding:2px 5px; font-size:0.8em; margin-right:5px;'>{tag}</span>"

            # HTML生成
            html_card = f"""
<div style="border: 4px solid {border_color}; border-radius: 12px; padding: 15px; background-color: {bg_color}; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <div style="font-weight:bold; color:{border_color}; font-size:1.1em; margin-bottom:5px;">{header_text}</div>
    <h3 style="margin:0 0 5px 0;">{res['data']['name']}</h3>
    <div style="color:#555; font-size:0.9em; margin-bottom:10px;">属性: {''.join(res['data']['icons'])}</div>
    
    <div style="font-size:0.8em; margin-bottom:2px;">仕事力: {res['power']}</div>
    <div style="background-color: #ddd; height: 12px; border-radius: 6px; width: 100%; margin-bottom: 10px;">
        <div style="background-color: {border_color}; width: {bar_width}%; height: 100%; border-radius: 6px;"></div>
    </div>
    <div style="margin-bottom: 10px;">{tags_html}</div>
    <hr style="border-top: 2px dashed {border_color}; opacity: 0.3; margin: 10px 0;">
    <div style="font-weight:bold; color:{footer_color}; text-align:center;">{footer_text}</div>
</div>
"""
            st.markdown(html_card, unsafe_allow_html=True)
