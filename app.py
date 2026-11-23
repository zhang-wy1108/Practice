import streamlit as st
import random
import sqlite3
import pandas as pd

# ================= 1. 数据库设置 =================
conn = sqlite3.connect('practice_record.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS records
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              center TEXT, scene TEXT, decision TEXT, score INTEGER, terms TEXT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# ================= 2. 页面与 UI 配置 =================
st.set_page_config(page_title="全能电商运营练习器", page_icon="🛒", layout="wide")
st.sidebar.title("🎮 练习器导航")
page = st.sidebar.radio("选择功能", ["开始练习", "我的复盘"])

# ================= 3. 练习中心逻辑 =================
def practice_center(center_name):
    st.header(f"📚 {center_name}")
    
    # 每次切换模块，重置状态
    if "scene" not in st.session_state or st.session_state.center != center_name:
        st.session_state.center = center_name
        if center_name == "选品定价（国内）":
            st.session_state.scene = {"cost": random.randint(20, 60), "logistics": random.randint(3, 8), "fee_rate": round(random.uniform(0.03, 0.08), 2), "target_margin": 0.30}
        elif center_name == "广告投放（国内）":
            st.session_state.scene = {"price": random.randint(50, 200), "cvr": round(random.uniform(0.01, 0.05), 3), "cpc": round(random.uniform(0.5, 2.0), 2)}
        elif center_name == "客服话术诊断（国内）":
            st.session_state.scene = {"question": "客户收到衣服后说：'实物颜色和图片差太多了，我要退货！'", "options": ["A. 亲，图片都是实拍的哦，可能是显示器色差呢~", "B. 实在抱歉让您失望了！如果不喜欢，我们支持7天无理由退换，运费我们包了。", "C. 退货可以，你自己出运费。"]}
        elif center_name == "数据分析诊断（国内）":
            st.session_state.scene = {"data": "昨日访客数：1000（持平） | 转化率：1.2%（前7天均值3.5%） | 客单价：85元（持平） | 退款率：2%（持平）", "options": ["A. 流量出了问题，需要加大直通车预算", "B. 查一下竞品是不是降价了，或者主图/详情页改了，或者来了差评", "C. 客服回复太慢"]}
        elif center_name == "跨境FBA利润（亚马逊）":
            st.session_state.scene = {"cost": random.randint(20, 50), "first_mile": random.randint(10, 30), "referral_rate": 0.15, "fba_fee": random.randint(20, 40), "acos": round(random.uniform(0.10, 0.30), 2)}
        elif center_name == "跨境合规风险（亚马逊）":
            st.session_state.scene = {"product": "带蓝牙功能的儿童智能手表，准备上架美国站", "options": ["A. 直接上架，先卖再说", "B. 只需要做常规的 CPC 认证", "C. 需要 FCC 认证（含蓝牙）+ CPC 认证（儿童产品）+ 可能面临侵权风险，需严格排查"]}

    s = st.session_state.scene
    st.markdown("### 📦 当前场景")
    
    # ---------- 模块 1：国内定价 ----------
    if center_name == "选品定价（国内）":
        st.info(f"进货成本：**{s['cost']}元** | 物流费：**{s['logistics']}元** | 平台扣点：**{s['fee_rate']*100:.0f}%**")
        with st.form("form1"):
            price = st.number_input("你的定价（元）", min_value=1.0, value=float(s['cost']*2))
            sales = st.number_input("预计日销量", min_value=1, value=30)
            submit = st.form_submit_button("🚀 提交决策")
        if submit:
            unit_profit = price - s['cost'] - s['logistics'] - (price * s['fee_rate'])
            margin = unit_profit / price if price > 0 else 0
            score = 100 if margin >= s['target_margin'] else max(0, int(margin/s['target_margin']*100))
            advice = "✅ 利润达标！" if margin >= s['target_margin'] else "⚠️ 毛利率偏低，抗风险能力差。"
            terms = "毛利率（Gross margin）：(售价-成本)/售价"
            c.execute("INSERT INTO records (center, scene, decision, score, terms) VALUES (?, ?, ?, ?, ?)", (center_name, str(s), f"售价:{price}", score, terms))
            conn.commit()
            st.success(f"得分：{score} 分")
            st.metric("单件净利", f"{unit_profit:.2f} 元")
            st.info(f"📖 术语：{terms}")
            st.session_state.clear()

    # ---------- 模块 2：国内广告 ----------
    elif center_name == "广告投放（国内）":
        st.info(f"客单价：**{s['price']}元** | 当前转化率(CVR)：**{s['cvr']*100:.1f}%** | 行业平均点击花费(CPC)：**{s['cpc']}元**")
        with st.form("form2"):
            budget = st.number_input("日预算（元）", min_value=10, value=100)
            bid = st.number_input("你的出价（CPC，元）", min_value=0.1, value=1.0, step=0.1)
            submit = st.form_submit_button("🚀 提交决策")
        if submit:
            clicks = int(budget / bid) if bid > 0 else 0
            orders = int(clicks * s['cvr'])
            revenue = orders * s['price']
            roi = revenue / budget if budget > 0 else 0
            score = min(100, int(roi * 30))
            advice = "✅ ROI健康！" if roi > 2 else "⚠️ ROI偏低，建议优化转化率或降出价。"
            terms = "ROI（投资回报率）：成交额/花费； CVR（转化率）：订单数/点击量"
            c.execute("INSERT INTO records (center, scene, decision, score, terms) VALUES (?, ?, ?, ?, ?)", (center_name, str(s), f"预算:{budget}", score, terms))
            conn.commit()
            st.success(f"得分：{score} 分")
            st.metric("ROI", f"{roi:.2f}")
            st.info(f"📖 术语：{terms}")
            st.session_state.clear()

    # ---------- 模块 3：客服话术 ----------
    elif center_name == "客服话术诊断（国内）":
        st.info(f"**场景**：{s['question']}")
        choice = st.radio("你选择哪种回复？", s['options'])
        if st.button("🚀 提交决策"):
            if "B" in choice:
                score, advice = 100, "✅ 完美！先安抚情绪，再给出超预期的解决方案。"
            elif "A" in choice:
                score, advice = 30, "⚠️ 推卸责任（色差），容易激怒客户导致差评。"
            else:
                score, advice = 0, "❌ 严重违规，容易引发平台介入。"
            terms = "转化率（CVR）、客诉率、DSR评分"
            c.execute("INSERT INTO records (center, scene, decision, score, terms) VALUES (?, ?, ?, ?, ?)", (center_name, s['question'], choice, score, terms))
            conn.commit()
            st.success(f"得分：{score} 分")
            st.write(advice)
            st.info(f"📖 术语：{terms}")
            st.session_state.clear()

    # ---------- 模块 4：数据分析 ----------
    elif center_name == "数据分析诊断（国内）":
        st.info(f"**昨日数据**：{s['data']}")
        choice = st.radio("你判断主要原因是什么？", s['options'])
        if st.button("🚀 提交决策"):
            if "B" in choice:
                score, advice = 100, "✅ 精准！转化率骤降通常是因为竞品动作、页面改动或突发差评。"
            else:
                score, advice = 20, "⚠️ 诊断错误。访客没降，说明不是流量问题。"
            terms = "转化率漏斗、归因分析"
            c.execute("INSERT INTO records (center, scene, decision, score, terms) VALUES (?, ?, ?, ?, ?)", (center_name, s['data'], choice, score, terms))
            conn.commit()
            st.success(f"得分：{score} 分")
            st.write(advice)
            st.info(f"📖 术语：{terms}")
            st.session_state.clear()

    # ---------- 模块 5：跨境利润 ----------
    elif center_name == "跨境FBA利润（亚马逊）":
        st.info(f"采购成本：**{s['cost']}元** | 头程(First-mile)：**{s['first_mile']}元** | 佣金：**{s['referral_rate']*100:.0f}%** | FBA费：**{s['fba_fee']}元** | ACoS：**{s['acos']*100:.0f}%**")
        with st.form("form5"):
            price_rmb = st.number_input("定价（折合人民币/元）", min_value=10.0, value=150.0)
            submit = st.form_submit_button("🚀 提交决策")
        if submit:
            ad_cost = price_rmb * s['acos']
            total_cost = s['cost'] + s['first_mile'] + (price_rmb * s['referral_rate']) + s['fba_fee'] + ad_cost
            net_profit = price_rmb - total_cost
            margin = net_profit / price_rmb if price_rmb > 0 else 0
            score = 100 if margin >= 0.15 else max(0, int(margin/0.15*100))
            advice = "✅ 跨境利润达标！" if margin >= 0.15 else "⚠️ 利润低于15%，需注意ACoS和FBA费用。"
            terms = "ACoS（广告成本销售比）； FBA（亚马逊物流）"
            c.execute("INSERT INTO records (center, scene, decision, score, terms) VALUES (?, ?, ?, ?, ?)", (center_name, str(s), f"定价:{price_rmb}", score, terms))
            conn.commit()
            st.success(f"得分：{score} 分")
            st.metric("净利率", f"{margin*100:.1f}%")
            st.info(f"📖 术语：{terms}")
            st.session_state.clear()

    # ---------- 模块 6：跨境合规 ----------
    elif center_name == "跨境合规风险（亚马逊）":
        st.info(f"**产品**：{s['product']}")
        choice = st.radio("你的合规策略是？", s['options'])
        if st.button("🚀 提交决策"):
            if "C" in choice:
                score, advice = 100, "✅ 合规意识很强！带蓝牙和儿童属性的电子产品是亚马逊严查对象。"
            else:
                score, advice = 0, "❌ 极易导致产品被下架、扣留甚至封店。"
            terms = "FCC认证、CPC认证、知识产权(IP)"
            c.execute("INSERT INTO records (center, scene, decision, score, terms) VALUES (?, ?, ?, ?, ?)", (center_name, s['product'], choice, score, terms))
            conn.commit()
            st.success(f"得分：{score} 分")
            st.write(advice)
            st.info(f"📖 术语：{terms}")
            st.session_state.clear()


# ================= 4. 页面渲染 =================
if page == "开始练习":
    st.title("🛒 全能电商运营练习器")
    st.write("请选择模块开始训练：")
    center_choice = st.selectbox("请选择要练习的模块", [
        "选品定价（国内）", 
        "广告投放（国内）", 
        "客服话术诊断（国内）",
        "数据分析诊断（国内）",
        "跨境FBA利润（亚马逊）",
        "跨境合规风险（亚马逊）"
    ])
    practice_center(center_choice)

elif page == "我的复盘":
    st.title("📊 我的复盘与数据看板")
    df = pd.read_sql_query("SELECT * FROM records ORDER BY time DESC", conn)
    
    if df.empty:
        st.info("暂无练习记录，快去练一道吧！")
    else:
        # 顶部指标卡
        col1, col2, col3 = st.columns(3)
        col1.metric("累计练习", f"{len(df)} 次")
        col2.metric("平均得分", f"{df['score'].mean():.1f} 分")
        col3.metric("最高得分", f"{df['score'].max()} 分")
        
        # 图表展示
        st.subheader("📈 成绩趋势")
        chart_data = df[['time', 'score']].set_index('time')
        st.line_chart(chart_data)
        
        # 错题本
        st.subheader("⚠️ 错题本（低于60分）")
        bad_df = df[df['score'] < 60]
        if bad_df.empty:
            st.write("太棒了，目前没有低分记录！")
        else:
            for _, row in bad_df.iterrows():
                with st.expander(f"[{row['center']}] 得分: {row['score']} - {row['time']}"):
                    st.write(f"**场景**: {row['scene']}")
                    st.write(f"**你的决策**: {row['decision']}")
                    st.write(f"**复习术语**: {row['terms']}")
                    
        st.subheader("📜 全部历史记录")
        st.dataframe(df[["time", "center", "score"]], use_container_width=True)
