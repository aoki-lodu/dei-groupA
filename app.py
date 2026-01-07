import streamlit as st

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

# --- ✅ 人財データ（全93名） ---
CHARACTERS_DB = [
    # --- 🌈 アイデンティティ ---
    {"name": "佐藤 陽菜", "icons": ["🌈"], "base": 1, "role": "Newbie"},
    {"name": "鈴木 翔太", "icons": ["🌈"], "base": 1, "role": "Newbie"},
    {"name": "高橋 美咲", "icons": ["🌈"], "base": 1, "role": "Newbie"},
    {"name": "中村 さくら", "icons": ["🌈"], "base": 2, "role": "Staff"},
    {"name": "伊藤 葵", "icons": ["🌈"], "base": 1, "role": "Newbie"},
    {"name": "山本 大翔", "icons": ["🌈"], "base": 2, "role": "Staff"},
    {"name": "渡辺 結衣", "icons": ["🌈"], "base": 2, "role": "Staff"},
    {"name": "田中 蓮", "icons": ["🌈"], "base": 1, "role": "Newbie"},
    {"name": "加藤 ひかる", "icons": ["🌈"], "base": 3, "role": "Leader"},
    {"name": "吉田 玲奈", "icons": ["🌈"], "base": 3, "role": "Leader"},
    {"name": "山田 隼人", "icons": ["🌈"], "base": 3, "role": "Leader"},
    {"name": "佐々木 真央", "icons": ["🌈"], "base": 4, "role": "Manager"},
    {"name": "山口 咲良", "icons": ["🌈"], "base": 4, "role": "Manager"},
    {"name": "斎藤 陽介", "icons": ["🌈"], "base": 5, "role": "Director"},
    # --- 💚 くらし ---
    {"name": "井上 菜々", "icons": ["💚"], "base": 1, "role": "Newbie"},
    {"name": "木村 拓海", "icons": ["💚"], "base": 1, "role": "Newbie"},
    {"name": "林 佳奈", "icons": ["💚"], "base": 1, "role": "Newbie"},
    {"name": "清水 友香", "icons": ["💚"], "base": 1, "role": "Newbie"},
    {"name": "池田 悠真", "icons": ["💚"], "base": 1, "role": "Newbie"},
    {"name": "橋本 紗季", "icons": ["💚"], "base": 2, "role": "Staff"},
    {"name": "山崎 優斗", "icons": ["💚"], "base": 2, "role": "Staff"},
    {"name": "阿部 千尋", "icons": ["💚"], "base": 2, "role": "Staff"},
    {"name": "森 真由", "icons": ["💚"], "base": 2, "role": "Staff"},
    {"name": "池上 直樹", "icons": ["💚"], "base": 3, "role": "Leader"},
    {"name": "大野 未来", "icons": ["💚"], "base": 3, "role": "Leader"},
    {"name": "石井 直人", "icons": ["💚"], "base": 3, "role": "Leader"},
    {"name": "原田 怜", "icons": ["💚"], "base": 4, "role": "Manager"},
    {"name": "田村 結菜", "icons": ["💚"], "base": 4, "role": "Manager"},
    {"name": "竹内 智也", "icons": ["💚"], "base": 5, "role": "Director"},
    # --- 🌏 グローバル ---
    {"name": "Ava Chen", "icons": ["🌏"], "base": 1, "role": "Newbie"},
    {"name": "Daniel Kim", "icons": ["🌏"], "base": 1, "role": "Newbie"},
    {"name": "Priya Singh", "icons": ["🌏"], "base": 1, "role": "Newbie"},
    {"name": "An Nguyen", "icons": ["🌏"], "base": 1, "role": "Newbie"},
    {"name": "Juan Martínez", "icons": ["🌏"], "base": 2, "role": "Staff"},
    {"name": "Hyejin Park", "icons": ["🌏"], "base": 2, "role": "Staff"},
    {"name": "Ethan Wang", "icons": ["🌏"], "base": 2, "role": "Staff"},
    {"name": "Olga Petrov", "icons": ["🌏"], "base": 2, "role": "Staff"},
    {"name": "Liam O'Connor", "icons": ["🌏"], "base": 3, "role": "Leader"},
    {"name": "Sofia García", "icons": ["🌏"], "base": 3, "role": "Leader"},
    {"name": "Minh Tran", "icons": ["🌏"], "base": 3, "role": "Leader"},
    {"name": "Amira Hassan", "icons": ["🌏"], "base": 4, "role": "Manager"},
    {"name": "Carlos Souza", "icons": ["🌏"], "base": 4, "role": "Manager"},
    {"name": "Zoe Müller", "icons": ["🌏"], "base": 5, "role": "Director"},
    # --- 📖 キャリア ---
    {"name": "長谷川 凛", "icons": ["📖"], "base": 1, "role": "Newbie"},
    {"name": "近藤 海斗", "icons": ["📖"], "base": 1, "role": "Newbie"},
    {"name": "石田 紅葉", "icons": ["📖"], "base": 1, "role": "Newbie"},
    {"name": "岡本 さとみ", "icons": ["📖"], "base": 1, "role": "Newbie"},
    {"name": "藤田 陽", "icons": ["📖"], "base": 1, "role": "Newbie"},
    {"name": "遠藤 大地", "icons": ["📖"], "base": 2, "role": "Staff"},
    {"name": "青木 里奈", "icons": ["📖"], "base": 2, "role": "Staff"},
    {"name": "宮本 蒼真", "icons": ["📖"], "base": 2, "role": "Staff"},
    {"name": "三浦 真琴", "icons": ["📖"], "base": 2, "role": "Staff"},
    {"name": "松本 直哉", "icons": ["📖"], "base": 3, "role": "Leader"},
    {"name": "川口 由衣", "icons": ["📖"], "base": 3, "role": "Leader"},
    # --- 📖 キャリア（元フェアから修正） ---
    {"name": "内田 隼", "icons": ["📖"], "base": 3, "role": "Leader"},
    {"name": "杉本 麻衣", "icons": ["📖"], "base": 4, "role": "Manager"},
    {"name": "中島 慎也", "icons": ["📖"], "base": 4, "role": "Manager"},
    {"name": "金子 拓真", "icons": ["📖"], "base": 5, "role": "Director"},
    # --- ⚖️ フェア ---
    {"name": "村上 拓人", "icons": ["⚖️"], "base": 1, "role": "Newbie"},
    {"name": "新井 美月", "icons": ["⚖️"], "base": 1, "role": "Newbie"},
    {"name": "大西 悠", "icons": ["⚖️"], "base": 1, "role": "Newbie"},
    {"name": "谷口 実央", "icons": ["⚖️"], "base": 1, "role": "Newbie"},
    {"name": "本田 琴音", "icons": ["⚖️"], "base": 1, "role": "Newbie"},
    {"name": "平野 健太", "icons": ["⚖️"], "base": 2, "role": "Staff"},
    {"name": "工藤 彩花", "icons": ["⚖️"], "base": 2, "role": "Staff"},
    {"name": "上田 翔", "icons": ["⚖️"], "base": 2, "role": "Staff"},
    {"name": "原 真子", "icons": ["⚖️"], "base": 2, "role": "Staff"},
    {"name": "神田 亮", "icons": ["⚖️"], "base": 3, "role": "Leader"},
    {"name": "安藤 望", "icons": ["⚖️"], "base": 3, "role": "Leader"},
    {"name": "野村 智", "icons": ["⚖️"], "base": 3, "role": "Leader"},
    {"name": "浜田 佑香", "icons": ["⚖️"], "base": 4, "role": "Manager"},
    {"name": "片山 駿", "icons": ["⚖️"], "base": 4, "role": "Manager"},
    {"name": "柴田 悠斗", "icons": ["⚖️"], "base": 5, "role": "Director"},
    # --- 複合属性 (2つ) ---
    {"name": "田辺 海斗", "icons": ["💚", "🌈"], "base": 1, "role": "Newbie"},
    {"name": "望月 さや", "icons": ["🌏", "🌈"], "base": 1, "role": "Newbie"},
    {"name": "佐伯 啓", "icons": ["📖", "🌈"], "base": 1, "role": "Newbie"},
    {"name": "磯部 瞳", "icons": ["🌈", "⚖️"], "base": 1, "role": "Newbie"},
    {"name": "花田 里緒", "icons": ["💚", "📖"], "base": 1, "role": "Newbie"},
    {"name": "山根 悠", "icons": ["💚", "⚖️"], "base": 2, "role": "Staff"},
    {"name": "町田 柚希", "icons": ["📖", "🌏"], "base": 2, "role": "Staff"},
    {"name": "中原 玲央", "icons": ["🌏", "⚖️"], "base": 2, "role": "Staff"},
    {"name": "島田 こはる", "icons": ["📖", "⚖️"], "base": 2, "role": "Staff"},
    {"name": "長井 智哉", "icons": ["💚", "🌈"], "base": 3, "role": "Leader"},
    {"name": "白石 凛子", "icons": ["🌏", "🌈"], "base": 3, "role": "Leader"},
    {"name": "宮下 慧", "icons": ["📖", "🌈"], "base": 3, "role": "Leader"},
    {"name": "Julia Novak", "icons": ["💚", "🌏"], "base": 4, "role": "Manager"},
    {"name": "杉浦 颯太", "icons": ["💚", "🌏"], "base": 4, "role": "Manager"},
    {"name": "Alec Tan", "icons": ["🌈", "⚖️"], "base": 5, "role": "Director"},
    # --- 複合属性 (3つ) ---
    {"name": "藤川 佑", "icons": ["💚", "🌏", "🌈"], "base": 1, "role": "Newbie"},
    {"name": "川瀬 美羽", "icons": ["💚", "📖", "🌈"], "base": 1, "role": "Newbie"},
    {"name": "Mei Tanaka", "icons": ["📖", "🌈", "⚖️"], "base": 2, "role": "Staff"},
    {"name": "Lucas Pereira", "icons": ["💚", "📖", "🌏"], "base": 2, "role": "Staff"},
    {"name": "Hanna Schmidt", "icons": ["💚", "🌏", "⚖️"], "base": 2, "role": "Staff"},
    {"name": "Sergey Ivanov", "icons": ["📖", "🌏", "⚖️"], "base": 3, "role": "Leader"},
    {"name": "Noor Rahman", "icons": ["💚", "📖", "⚖️"], "base": 3, "role": "Leader"},
    {"name": "茅野 すみれ", "icons": ["📖", "🌏", "🌈"], "base": 5, "role": "Director"},
]

# --- ✅ 施策データ（全30種） ---
POLICIES_DB = [
    {"name": "構造化面接", "target": ["⚖️"], "power": 0, "type": ["recruit", "promote"]},
    {"name": "インクルーシブJD", "target": ["📖"], "power": 0, "type": ["recruit"]},
    {"name": "給与バンド公開", "target": ["⚖️"], "power": 0, "type": ["recruit", "promote", "shield"]},
    {"name": "フルリモート", "target": ["💚"], "power": 1, "type": ["recruit", "power", "shield"]},
    {"name": "時短・コア短縮", "target": ["💚"], "power": 2, "type": ["recruit", "power", "shield"]},
    {"name": "会議字幕・通訳", "target": ["🌏"], "power": 2, "type": ["power", "recruit"]},
    {"name": "二言語テンプレ＆用語集", "target": ["🌏"], "power": 1, "type": ["power", "recruit"]},
    {"name": "ビザスポンサー", "target": ["🌏"], "power": 0, "type": ["recruit", "shield"]},
    {"name": "リターンシップ", "target": ["📖"], "power": 0, "type": ["recruit", "promote"]},
    {"name": "オンボーディング90日", "target": ["📖"], "power": 3, "type": ["power", "shield"]},
    {"name": "メンタリング＆スポンサー", "target": ["📖"], "power": 0, "type": ["promote", "shield"]},
    {"name": "公正なアサイン管理", "target": ["⚖️"], "power": 1, "type": ["promote", "power"]},
    {"name": "有償ワークサンプル", "target": ["📖"], "power": 1, "type": ["recruit", "power"]},
    {"name": "面接官トレーニング", "target": ["⚖️"], "power": 0, "type": ["recruit", "promote"]},
    {"name": "ケア支援 (保育/介護補助)", "target": ["💚"], "power": 2, "type": ["recruit", "power", "shield"]},
    {"name": "アクセシブルツール支給", "target": ["🌈"], "power": 2, "type": ["power", "shield"]},
    {"name": "心理的安全性ルーチン", "target": ["🌈"], "power": 3, "type": ["power", "promote", "shield"]},
    {"name": "ERG→経営提言ライン", "target": ["🌈"], "power": 1, "type": ["promote", "power"]},
    {"name": "復帰ブリッジ (育休/介護)", "target": ["💚"], "power": 1, "type": ["power", "shield", "promote"]},
    {"name": "配慮申請ガイド＆窓口", "target": ["🌈"], "power": 0, "type": ["recruit", "shield"]},
    {"name": "フェア採用ダッシュボード", "target": ["⚖️"], "power": 0, "type": ["recruit"]},
    {"name": "交通・機材サポート", "target": ["⚖️"], "power": 1, "type": ["recruit", "power"]},
    {"name": "リロケーション支援", "target": ["🌏"], "power": 0, "type": ["recruit", "shield"]},
    {"name": "内部公募マーケット", "target": ["📖"], "power": 1, "type": ["promote", "power", "shield"]},
    {"name": "学習支援 (費用・就業内)", "target": ["📖"], "power": 3, "type": ["power", "promote"]},
    {"name": "サテライト/在宅手当", "target": ["💚"], "power": 1, "type": ["recruit", "power", "shield"]},
    {"name": "透明な評価会 (校正)", "target": ["⚖️"], "power": 0, "type": ["promote", "shield"]},
    {"name": "ATSバイアスアラート運用", "target": ["⚖️"], "power": 0, "type": ["recruit"]}, 
    {"name": "アルムナイ/ブーメラン採用", "target": ["📖", "🌏"], "power": 1, "type": ["recruit", "shield", "promote", "power"]}, 
    {"name": "ペアワーク＆コードレビュー標準", "target": ["📖", "🌈"], "power": 2, "type": ["power", "promote"]},
]

# ==========================================
# 1. サイドバー (スマート検索版)
# ==========================================
with st.sidebar:
    st.header("🎮 ゲーム操作盤")
    st.info("👇 メンバーや施策を選んでください")

    # --- 🟢 メンバー選択 (検索付きプルダウン) ---
    st.markdown("### 👤 参加メンバー")
    st.caption("※プルダウン内で文字を入力すると、名前・役職・属性で絞り込めます。")
    
    # 検索しやすいラベルを作成する関数
    def create_char_label(c):
        icons = "".join(c['icons'])
        return f"{c['name']} ｜ {c['role']} {icons}"

    # { "表示ラベル": データ本体 } の辞書を作成
    char_map = {create_char_label(c): c for c in CHARACTERS_DB}
    
    # デフォルト選択用のラベルリスト
    default_char_labels = [create_char_label(c) for c in CHARACTERS_DB[:3]]

    # マルチセレクト (表示はラベルで行う)
    selected_char_labels = st.multiselect(
        "メンバーを選択 (検索対応)",
        options=char_map.keys(),
        default=default_char_labels
    )
    
    # ラベルから元のデータを取り出す
    active_chars = [char_map[label] for label in selected_char_labels]

    st.divider()

    # --- 🃏 施策選択 (検索付きプルダウン) ---
    st.markdown("### 🃏 実行した施策")
    st.caption("※「recruit」「shield」や属性アイコンで検索できます。")

    def create_policy_label(p):
        target = "".join(p['target'])
        types = " ".join(p['type'])
        return f"{p['name']} ｜ {target} ({types})"

    policy_map = {create_policy_label(p): p for p in POLICIES_DB}
    
    selected_policy_labels = st.multiselect(
        "施策を選択 (検索対応)",
        options=policy_map.keys(),
        default=[]
    )
    
    active_policies = [policy_map[label] for label in selected_policy_labels]

# ==========================================
# 2. 計算ロジック
# ==========================================
total_power = 0
active_shields = set()
active_recruits = set()

# 施策の効果を集計
for pol in active_policies:
    if "shield" in pol["type"]:
        for t in pol["target"]:
            active_shields.add(t)
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

# --- 社長データの作成 ---
president_data = {
    "data": {"name": "社長", "icons": ["👑"]},
    "power": 2,
    "tags": [],
    "risks": [],
    "is_safe": True
}
char_results.insert(0, president_data)
# -----------------------------

# ==========================================
# 3. メイン画面レイアウト
# ==========================================
st.title("🎲 DE&I 組織シミュレーター")

# スコアボード
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("🏆 チーム仕事力", f"{total_power} pt")
with c2:
    shield_text = " ".join(sorted(list(active_shields))) if active_shields else "ー"
    st.metric("🛡️ 離職防止中", shield_text)
with c3:
    recruit_text = " ".join(sorted(list(active_recruits))) if active_recruits else "ー"
    st.metric("🔵 採用強化中", recruit_text)
with c4:
    st.metric("👥 メンバー数", f"{len(active_chars)} 名")

st.divider()

# サイコロ対応表
st.markdown("### 🎲 サイコロの出目対応表")
cols = st.columns(6)
for i, (num, desc) in enumerate(RISK_MAP_DISPLAY.items()):
    with cols[i]:
        st.markdown(f"**{num}**: {desc}")

# --- メンバー表示エリア ---
st.subheader("📊 組織メンバーの状態")
st.caption("リアルサイコロを振って、🟥 赤い枠 のメンバーの属性が出たら離職です。")

cols = st.columns(3)

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
            footer_text = f"{risk_icons} が出たらアウト" 
            footer_color = "#ff1744"

        # 社長の場合
        if res['data']['name'] == "社長":
            header_text = "🏢 社長 (固定)"
            footer_text = "✅ 絶対安泰"

        bar_width = min(res['power'] * 10, 100)
        
        tags_html = ""
        for tag in res["tags"]:
            tags_html += f"<span style='background:#fff; border:1px solid #ccc; border-radius:4px; padding:2px 5px; font-size:0.8em; margin-right:5px;'>{tag}</span>"

        icons_str = "".join(res['data']['icons'])
        
        # 高さ固定
        html_card = (
            f'<div style="border: 4px solid {border_color}; border-radius: 12px; padding: 15px; background-color: {bg_color}; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 320px; display: flex; flex-direction: column; justify-content: space-between;">'
            f'<div>'
            f'<div style="font-weight:bold; color:{border_color}; font-size:1.1em; margin-bottom:5px;">{header_text}</div>'
            f'<h3 style="margin:0 0 5px 0;">{res["data"]["name"]}</h3>'
            f'<div style="color:#555; font-size:0.9em; margin-bottom:10px;">属性: {icons_str}</div>'
            f'<div style="font-size:0.8em; margin-bottom:2px;">仕事力: {res["power"]}</div>'
            f'<div style="background-color: #ddd; height: 12px; border-radius: 6px; width: 100%; margin-bottom: 10px;">'
            f'<div style="background-color: {border_color}; width: {bar_width}%; height: 100%; border-radius: 6px;"></div>'
            f'</div>'
            f'<div style="margin-bottom: 10px; min-height: 25px;">{tags_html}</div>'
            f'</div>'
            f'<div>'
            f'<hr style="border-top: 2px dashed {border_color}; opacity: 0.3; margin: 10px 0;">'
            f'<div style="font-weight:bold; color:{footer_color}; text-align:center;">{footer_text}</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(html_card, unsafe_allow_html=True)

# --- 施策表示エリア ---
st.divider()
st.subheader("🛠️ 実行中の施策")

if not active_policies:
    st.info("👈 サイドバーから施策を実行すると、ここに表示されます")
else:
    cols_pol = st.columns(3)
    for i, pol in enumerate(active_policies):
        with cols_pol[i % 3]:
            type_tags = []
            if pol["power"] > 0:
                type_tags.append(f"🟢 仕事力+{pol['power']}")
                
            if "shield" in pol["type"]: type_tags.append("🛡️ 離職防止")
            if "recruit" in pol["type"]: type_tags.append("🔵 採用強化")
            
            pol_tags_html = ""
            for tag in type_tags:
                pol_tags_html += f"<span style='background:#fff; border:1px solid #ccc; border-radius:4px; padding:2px 5px; font-size:0.8em; margin-right:5px; color:#333;'>{tag}</span>"

            target_icons = "".join(pol["target"])
            html_pol_card = (
                f'<div style="border: 2px solid #5c6bc0; border-radius: 10px; padding: 15px; background-color: #e8eaf6; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
                f'<div style="font-weight:bold; color:#3949ab; font-size:1.0em; margin-bottom:5px;">{pol["name"]}</div>'
                f'<div style="font-size:0.9em; color:#555; margin-bottom:8px;">対象: {target_icons}</div>'
                f'<div>{pol_tags_html}</div>'
                f'</div>'
            )
            st.markdown(html_pol_card, unsafe_allow_html=True)
