import streamlit as st
import random
import sqlite3
import pandas as pd
from datetime import datetime

# ================= 1. 数据库设置 =================
conn = sqlite3.connect('practice_record.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS records
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              center TEXT, scene TEXT, decision TEXT, score INTEGER, terms TEXT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# ================= 2. 页面全局配置 (隐藏默认UI，增加高级感) =================
st.set_page_config(page_title="电商运营工作台", page_icon="🛍️", layout="wide")

# 注入 CSS 样式，让按钮变成卡片，隐藏 Streamlit 默认的汉堡菜单
st.markdown("""
<style>
    /* 隐藏顶部的默认菜单和红条 */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 卡片样式 */
    div.stButton > button {
        width: 100%;
        height: 120px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #ff6b6b;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* 侧边栏背景色 */
    [data-testid="stSidebar"] {
        background-color: #2b3952;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ================= 3. 侧边栏 (导航) =================
with st.sidebar:
    st.markdown("### 👤 Zahia")
    st.caption("电商运营训练工作台")
    st.divider()
    st.markdown("**🏠 小窝 (Home)**")
    st.markdown("🏆 学堂 (技能训练)")
    st.markdown("🎮 乐园 (实战模拟)")
    st.markdown("📊 成就图谱")
    st.markdown("⚙️ 设置与重置")

# ================= 4. 主页面 (工作台) =================
# 顶部欢迎语和时间
col_time, col_quote = st.columns([1, 2])
with col_time:
    now = datetime.now()
    st.markdown(f"<h1 style='margin-bottom:0;'>{now.strftime('%H:%M')}</h1>", unsafe_allow_html=True)
    st.caption(now.strftime('%Y年%m月%d日'))
with col_quote:
    st.info("💡 **“慢慢来，比较快。运营是一个需要不断复盘的手艺。”**")

st.write("") # 占位

# 数据看板 (读取数据库统计)
df = pd.read_sql_query("SELECT * FROM records", conn)
total_practice = len(df)
avg_score = df['score'].mean() if total_practice > 0 else 0
best_score = df['score'].max() if total_practice > 0 else 0

st.markdown("### 📈 今日数据")
col1, col2, col3, col4 = st.columns(4)
col1.metric("累计练习", f"{total_practice} 次")
col2.metric("平均得分", f"{avg_score:.1f} 分")
col3.metric("最高得分", f"{best_score} 分")
col4.metric("今日心情", "😎 极佳")

st.divider()

# 快捷录入 (卡片式入口)
st.markdown("### ⚡ 快捷练习")
st.write("点击下方卡片，进入不同的电商实战模块：")

# 这是第一排卡片
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("📦\n\n**选品定价**\n商品利润测算与定价策略"):
        st.session_state.page = "pricing"
with c2:
    if st.button("📈\n\n**广告投放**\nROI模拟与关键词出价"):
        st.session_state.page = "ads"
with c3:
    if st.button("💬\n\n**客服转化**\n话术诊断与催付挽回"):
        st.session_state.page = "service"

# 这是第二排卡片
c4, c5, c6 = st.columns(3)
with c4:
    if st.button("🌍\n\n**跨境FBA**\n亚马逊全成本利润核算"):
        st.session_state.page = "cross_border"
with c5:
    if st.button("🛒\n\n**千牛上架**\n淘宝后台全真模拟"):
        st.session_state.page = "taobao"
with c6:
    if st.button("📊\n\n**数据复盘**\n查看错题本与成绩趋势"):
        st.session_state.page = "review"

st.divider()

# ================= 5. 模拟练习区逻辑 =================
# 这里以弹窗或底部展开的形式展示，不破坏主页面的美观
page = st.session_state.get("page", "")

if page != "":
    st.markdown(f"### 🎯 当前进入模块：{page.upper()}")
    
    # 简单演示一下弹窗逻辑
    if page == "pricing":
        st.info("进货成本 30 元，物流 5 元，扣点 5%。你的定价是：")
        price = st.number_input("输入售价", value=80.0)
        if st.button("提交测算"):
            profit = price - 30 - 5 - (price * 0.05)
            st.success(f"单件利润：{profit:.2f} 元")
            c.execute("INSERT INTO records (center, scene, decision, score, terms) VALUES ('选品定价', '基础测算', '无', 80, '毛利率')", )
            conn.commit()
            st.session_state.page = "" # 清空状态
            st.rerun()
            
    elif page == "review":
        st.dataframe(df[["time", "center", "score"]], use_container_width=True)
        if st.button("返回工作台"):
            st.session_state.page = ""
            st.rerun()
            
    else:
        st.warning("该模块正在开发中... (你可以继续让我帮你补充对应的交互界面)")
        if st.button("返回工作台"):
            st.session_state.page = ""
            st.rerun()
