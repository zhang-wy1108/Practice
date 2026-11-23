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

# ================= 2. 页面配置 =================
st.set_page_config(page_title="电商运营工作台", layout="wide")

# ================= 3. 左侧导航栏 =================
with st.sidebar:
    st.title("🛍️ 运营工作台")
    st.caption("我的个人练习空间")
    st.divider()
    nav = st.radio("导航", ["🏠 首页 (工作台)", "📊 成绩与复盘"])

# ================= 4. 主页面逻辑 =================
if nav == "🏠 首页 (工作台)":
    # --- 顶部欢迎区域 ---
    col1, col2 = st.columns([1, 2])
    with col1:
        now = datetime.now()
        st.title(f"👋 晚上好")
        st.write(f"今天是 {now.strftime('%Y年%m月%d日')}")
    with col2:
        st.info("💡 **运营心得**：慢慢来，比较快。数据不会骗人，每一个细节的优化都在积累势能。")
    
    st.divider()

    # --- 核心数据面板 ---
    st.subheader("📈 数据看板")
    df = pd.read_sql_query("SELECT * FROM records", conn)
    total_practice = len(df)
    avg_score = df['score'].mean() if total_practice > 0 else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("累计练习次数", f"{total_practice} 次")
    m2.metric("平均得分", f"{avg_score:.1f} 分")
    m3.metric("今日学习时长", "未统计")
    m4.metric("连续打卡", "1 天")

    st.divider()

    # --- 快捷练习入口 (卡片模式) ---
    st.subheader("⚡ 快捷练习入口")
    st.write("选择下方模块开始训练：")
    
    # 第一排
    r1_c1, r1_c2, r1_c3 = st.columns(3)
    with r1_c1:
        with st.container(border=True):
            st.subheader("📦 选品与定价")
            st.caption("国内电商单品利润测算")
            btn_pricing = st.button("进入模块", use_container_width=True, key="btn1")
            
    with r1_c2:
        with st.container(border=True):
            st.subheader("📈 广告投放")
            st.caption("国内电商ROI与出价模拟")
            btn_ads = st.button("进入模块", use_container_width=True, key="btn2")
            
    with r1_c3:
        with st.container(border=True):
            st.subheader("🛒 千牛上架")
            st.caption("淘宝后台全流程高保真模拟")
            btn_taobao = st.button("进入模块", use_container_width=True, key="btn3")

    # 第二排
    r2_c1, r2_c2, r2_c3 = st.columns(3)
    with r2_c1:
        with st.container(border=True):
            st.subheader("🌍 跨境FBA")
            st.caption("亚马逊全成本利润核算")
            btn_cross = st.button("进入模块", use_container_width=True, key="btn4")
            
    with r2_c2:
        with st.container(border=True):
            st.subheader("💬 客服话术")
            st.caption("客诉处理与话术转化")
            btn_service = st.button("进入模块", use_container_width=True, key="btn5")
            
    with r2_c3:
        with st.container(border=True):
            st.subheader("📊 数据分析")
            st.caption("转化率漏斗与异常排查")
            btn_data = st.button("进入模块", use_container_width=True, key="btn6")

    # --- 练习区加载 ---
    st.divider()
    
    # 使用 session_state 记录当前点击了哪个模块
    if "active_module" not in st.session_state:
        st.session_state.active_module = None

    if btn_pricing: st.session_state.active_module = "pricing"
    if btn_ads: st.session_state.active_module = "ads"
    if btn_taobao: st.session_state.active_module = "taobao"
    if btn_cross: st.session_state.active_module = "cross"
    if btn_service: st.session_state.active_module = "service"
    if btn_data: st.session_state.active_module = "data"

    # 根据点击展示具体练习
    if st.session_state.active_module:
        with st.expander(f"🎯 当前正在练习：{st.session_state.active_module.upper()}", expanded=True):
            
            # 1. 选品定价
            if st.session_state.active_module == "pricing":
                st.write("场景：进货成本 30 元，物流 5 元，平台扣点 5%。")
                price = st.number_input("你的定价 (元)", value=80.0)
                if st.button("提交测算"):
                    profit = price - 30 - 5 - (price * 0.05)
                    st.success(f"单件净利：{profit:.2f} 元")
                    c.execute("INSERT INTO records (center, scene, decision, score, terms) VALUES ('选品定价', '基础', '无', 80, '毛利率')")
                    conn.commit()
            
            # 2. 千牛上架 (这里放之前的 Tabs 高保真简化版)
            elif st.session_state.active_module == "taobao":
                t1, t2 = st.tabs(["基础信息", "销售信息"])
                with t1:
                    st.text_input("商品标题（核心词如：龙年手链）")
                    st.selectbox("品牌", ["无品牌", "其他"])
                with t2:
                    st.number_input("一口价", value=99.0)
                    st.number_input("库存", value=50)
                if st.button("提交宝贝信息"):
                    st.success("✅ 审核通过！体检得分：90")
                    c.execute("INSERT INTO records (center, scene, decision, score, terms) VALUES ('千牛上架', '基础', '无', 90, 'SPU')")
                    conn.commit()

            # 其他模块占位
            else:
                st.info("该模块正在配置中，后续可加入对应的表单。")
            
            if st.button("关闭当前模块"):
                st.session_state.active_module = None
                st.rerun()

# ================= 5. 复盘页面 =================
elif nav == "📊 成绩与复盘":
    st.title("📊 成绩与复盘")
    df = pd.read_sql_query("SELECT * FROM records ORDER BY time DESC", conn)
    if df.empty:
        st.info("暂无数据，快去练习吧！")
    else:
        st.dataframe(df[["time", "center", "score"]], use_container_width=True)
