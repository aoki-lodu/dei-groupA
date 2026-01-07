import streamlit as st
import pandas as pd

# ==========================================
# 0. 設定 & データ定義
# ==========================================
st.set_page_config(page_title="LODU Game", layout="wide", initial_sidebar_state="expanded")

# カスタムCSS（見やすくする ＆ 誤操作防止）
st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ff4b4b; }
    .card-safe { border-left: 5px solid #00c853; }
    
    /* ↓↓↓ 【修正】一括削除ボタン（×）を「場所」指定で消す最強の魔法 ↓↓↓ */
    /* マルチセレクトの右端にあるアイコンエリア（×や▼がある場所）を丸ごと隠します */
    [data-testid="stMultiselect"] div[data-baseweb="select"] > div:nth-last-child(1) {
        display: none !important;
    }
    /* ↑↑↑ これでどんな環境でも強制的に消えます ↑↑↑ */
    
</style>
""", unsafe_allow_html=True)

# ゲームデータ
ICONS = {"くらし(💚)": "💚", "キャリア(📖)": "📖", "グローバル(🌏)": "🌏", "アイデンティティ(🌈)": "🌈", "フェア(⚖️)": "⚖️"}

# 出目とリスクの対応表（画面表示用）
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
# 1. サイドバー（入力）
# ==========================================
with st.sidebar:
    st.header("🎮 ゲーム操作盤")
    
    st.info("👇 メンバーや施策を選んでください")
    
    # シンプルな選択機能
    selected_char_names = st.multiselect(
        "👤 参加メンバー",
        [c["name"] for c in CHARACTERS_DB],
        default=[c["name"] for c in CHARACTERS_DB[:3]] # 初期値
    )
    
    st.divider()
    
    selected_policy_names = st.multiselect(
        "🃏 実行した施策",
        [p["name"] for p in POLICIES_DB],
        default=[]
    )

# データの抽出
active_chars = [c for c in CHARACTERS_DB if c["name"] in selected_char_names]
active_policies = [p for p in POLICIES_DB if p["name"] in selected_policy_names]

# ==========================================
# 2. 計算ロジック
# ==========================================
total_power = 0
active_shields = set()

# 盾の判定
for pol in active_policies:
    if "shield" in pol["type"]:
        for t in pol["target"]:
            active_shields.add(t)

# メンバーごとの計算
char_results = []
for char in active_chars:
    current_power = char["base"]
    status_tags = []
    
    # 施策効果（パワーアップ・昇進・採用）
    for pol in active_policies:
        if set(char["icons"]) & set(pol["target"]):
            current_power += pol["power"]
            if "promote" in pol["type"] and "🟢昇進" not in status_tags: status_tags.append("🟢昇進")
            if "recruit" in pol["type"] and "🔵採用" not in status_tags: status_tags.append("🔵採用")
            
    # リスク判定（盾がない属性を抽出）
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

# スコアボード
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("🏆 チーム仕事力", f"{total_power} pt")
with c2:
    if active_shields:
        shield_text = " ".join(sorted(list(active_shields)))
    else:
        shield_text = "ー"
    st.metric("🛡️ ガード中の属性", shield_text)
with c3:
    st.metric("👥 メンバー数", f"{len(active_chars)} 名")

st.divider()

# サイコロ対応表（アナログプレイ用）
with st.expander("🎲 サイコロの出目対応表を見る（クリックで開閉）"):
    cols = st.columns(6)
    for i, (num, desc) in enumerate(RISK_MAP_DISPLAY.items()):
        with cols[i]:
            st.markdown(f"**{num}**: {desc}")

st.subheader("📊 組織メンバーの状態")
st.caption("リアルサイコロを振って、危険マーク（⚠️）がついている属性が出たら、そのメンバーは離職です。サイドバーの名前横の「×」で削除してください。")

# メンバーカード表示
cols = st.columns(3)
if not char_results:
    st.info("👈 サイドバーからメンバーを追加してください")
else:
    for i, res in enumerate(char_results):
        with cols[i % 3]:
            # カード枠のデザイン
            border_style = "card-safe" if res["is_safe"] else "card"
            emoji_status = "🛡️鉄壁" if res["is_safe"] else "⚠️危険"
            
            with st.container():
                st.markdown(f"**{res['data']['name']}**")
                st.caption(f"属性: {''.join(res['data']['icons'])}")
                
                # 仕事力バー
                st.progress(min(res["power"] / 10, 1.0), text=f"仕事力: {res['power']}")
                
                # タグ（昇進など）
                if res["tags"]:
                    st.markdown(" ".join([f"`{t}`" for t in res["tags"]]))
                
                st.divider()
                
                # リスク表示
                if res["is_safe"]:
                    st.success(f"{emoji_status}: ガード成功中")
                else:
                    risk_str = " ".join(res['risks'])
                    st.error(f"{emoji_status}: **{risk_str}** が出たらアウト")
