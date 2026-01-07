import streamlit as st
import pandas as pd
import random
import time

# ==========================================
# 0. 設定 (一番最初に書く必要があります)
# ==========================================
st.set_page_config(page_title="LODU Game", layout="wide", initial_sidebar_state="expanded")

# カスタムCSS
st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ff4b4b; }
    .card-safe { border-left: 5px solid #00c853; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. ゲームデータ定義
# ==========================================
ICONS = {"くらし(💚)": "💚", "キャリア(📖)": "📖", "グローバル(🌏)": "🌏", "アイデンティティ(🌈)": "🌈", "フェア(⚖️)": "⚖️"}
RISK_MAP = {2: "💚", 3: "📖", 4: "🌏", 5: "🌈", 6: "⚖️"}

# 人財データ
CHARACTERS_DB = [
    {"name": "白石 凛子", "base": 3, "icons": ["🌏", "🌈"], "role": "Manager"},
    {"name": "山本 大翔", "base": 2, "icons": ["🌈"], "role": "Staff"},
    {"name": "川瀬 美羽", "base": 1, "icons": ["💚", "📖", "🌈"], "role": "Newbie"},
    {"name": "Hanna Schmidt", "base": 2, "icons": ["💚", "🌏", "⚖️"], "role": "Specialist"},
    {"name": "宮下 慧", "base": 3, "icons": ["📖", "🌈"], "role": "Expert"},
    {"name": "川口 由衣", "base": 3, "icons": ["📖"], "role": "Leader"},
]

# 施策データ
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
# 2. サイドバー（入力エリア）
# ==========================================
with st.sidebar:
    st.header("🎮 ゲーム操作盤")
    
    selected_char_names = st.multiselect(
        "👤 参加メンバー",
        [c["name"] for c in CHARACTERS_DB],
        default=[c["name"] for c in CHARACTERS_DB[:3]]
    )
    
    st.divider()
    
    selected_policy_names = st.multiselect(
        "🃏 実行した施策",
        [p["name"] for p in POLICIES_DB],
        default=[]
    )
    
    st.divider()
    if st.button("🔄 リセット", type="primary"):
        st.rerun()

# データの抽出
active_chars = [c for c in CHARACTERS_DB if c["name"] in selected_char_names]
active_policies = [p for p in POLICIES_DB if p["name"] in selected_policy_names]

# ==========================================
# 3. 計算ロジック
# ==========================================
total_power = 0
active_shields = set()
for pol in active_policies:
    if "shield" in pol["type"]:
        for t in pol["target"]:
            active_shields.add(t)

char_results = []
for char in active_chars:
    current_power = char["base"]
    status_tags = []
    
    # 施策効果
    for pol in active_policies:
        if set(char["icons"]) & set(pol["target"]):
            current_power += pol["power"]
            if "promote" in pol["type"] and "🟢昇進" not in status_tags: status_tags.append("🟢昇進")
            if "recruit" in pol["type"] and "🔵採用" not in status_tags: status_tags.append("🔵採用")
            
    # リスク判定
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
# 4. メイン画面レイアウト
# ==========================================

# タイトルエリア
st.title("🎲 DE&I 組織シミュレーター")

# スコアボード
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("🏆 チーム仕事力", f"{total_power} pt")
with c2:
    # --- ここを変更しました！ ---
    # ガード中のアイコンを並べて表示します
    if active_shields:
        shield_text = " ".join(sorted(list(active_shields))) # アイコンを並べる
    else:
        shield_text = "ー" # なしの場合
    
    st.metric("🛡️ ガード中の属性", shield_text)
    # -----------------------
with c3:
    st.metric("👥 メンバー数", f"{len(active_chars)} 名")

st.divider()

# ダイスロールセクション
st.subheader("🎲 運命のダイスロール")
col_dice_btn, col_dice_result = st.columns([1, 2])

with col_dice_btn:
    roll_btn = st.button("サイコロを振る！", type="primary", use_container_width=True)

with col_dice_result:
    if roll_btn:
        with st.spinner("コロコロ..."):
            time.sleep(1)
            dice = random.randint(1, 6)
        
        st.markdown(f"### 出目: **【 {dice} 】**")
        
        if dice == 1:
            st.balloons()
            st.success("🎉 **セーフ！** トラブルは起きませんでした！")
        else:
            risk_attr = RISK_MAP.get(dice)
            st.warning(f"⚠️ 対象: **{risk_attr}** の属性を持つメンバー")
            
            # 離職判定
            dropouts = [res["data"]["name"] for res in char_results if risk_attr in res["risks"]]
            
            if dropouts:
                st.error(f"😱 **離職発生！**: {', '.join(dropouts)} さんが退職します...")
            elif risk_attr in active_shields:
                st.info(f"🛡️ **ガード成功！** 施策のおかげで {risk_attr} のメンバーは守られました！")
            else:
                st.success("💨 該当するメンバーがいなかったのでセーフ！")

st.divider()

# メンバーカード表示エリア
st.subheader("📊 組織メンバーの状態")

cols = st.columns(3)
for i, res in enumerate(char_results):
    with cols[i % 3]:
        # カードのデザイン
        emoji_status = "🛡️鉄壁" if res["is_safe"] else "⚠️危険"
        
        with st.container():
            st.markdown(f"**{res['data']['name']}**")
            st.caption(f"属性: {''.join(res['data']['icons'])}")
            
            # 仕事力メーター
            st.progress(min(res["power"] / 10, 1.0), text=f"仕事力: {res['power']}")
            
            # ステータスバッジ
            if res["tags"]:
                st.markdown(" ".join([f"`{t}`" for t in res["tags"]]))
            else:
                st.caption("特殊効果なし")
            
            # リスク表示
            if res["is_safe"]:
                st.success(f"{emoji_status}")
            else:
                st.error(f"{emoji_status}: {''.join(res['risks'])}が出たらアウト")
