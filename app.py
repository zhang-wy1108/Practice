import streamlit as st
import pandas as pd
import sqlite3
import altair as alt
from datetime import datetime

# ================= 1. 全局底座与数据库 =================
st.set_page_config(page_title="全域电商仿真实训工作台", page_icon="🌐", layout="wide")
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

conn = sqlite3.connect('practice_record.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS records
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              module TEXT, action TEXT, score INTEGER, report TEXT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# ================= 2. 左侧主导航 =================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/shop.png", width=60)
    st.title("全域仿真实训台")
    st.caption("国内+跨境 · 纯沙盘演练")
    st.divider()
    
    nav = st.radio(
        "系统模块",
        [
            "📊 全局总览驾驶舱", 
            "🇨🇳 国内电商仿真", 
            "🌍 跨境平台仿真", 
            "📚 运营知识库",
            "🎯 实训沙盘与复盘",
            "⚙️ 系统设置"
        ]
    )

# ================= 3. 模块 1：全局驾驶舱 =================
if nav == "📊 全局总览驾驶舱":
    st.title("🌐 模拟多店铺数据看板")
    st.info("💡 提示：此处为模拟沙盘数据，非真实交易。可在右侧【系统设置】中重置或加载新场景。")
    
    # 顶部时间与语言切换模拟
    col_time, col_lang = st.columns([3, 1])
    with col_time:
        st.write(f"🗓️ 当前模拟日期：{datetime.now().strftime('%Y年%m月%d日')}")
    with col_lang:
        st.selectbox("界面/知识库语言", ["中文", "English", "Español", "日本語"])
    
    st.divider()
    
    # 数据分开展示
    tab_dom, tab_cross = st.tabs(["🇨🇳 国内店铺数据", "🌍 跨境店铺数据 (USD)"])
    
    with tab_dom:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("国内总 GMV", "¥ 125,400", "+12%")
        c2.metric("订单量", "3,240 单", "+5%")
        c3.metric("整体转化率", "3.2%", "-0.1%")
        c4.metric("广告 ROI", "2.5", "持平")
        st.warning("⚠️ 预警：国内店铺有 3 笔异常物流，有 1 条恶意差评待处理。")
        
    with tab_cross:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("跨境总 GMV", "$ 18,500", "+22%")
        c2.metric("订单量", "890 单", "+15%")
        c3.metric("综合 ACoS", "18%", "优化中")
        c4.metric("平均净利率", "15.5%", "+1.2%")
        st.error("⚠️ 警告：亚马逊美国站有 2 个 SKU 面临断货风险；欧洲站 VAT 申报单已生成，待审核。")

# ================= 4. 模块 2：国内电商仿真 =================
elif nav == "🇨🇳 国内电商仿真":
    st.title("🐮 国内电商平台后台仿真")
    
    platform = st.selectbox("选择仿真平台", ["淘宝/天猫", "京东", "抖音小店", "拼多多"])
    st.info(f"当前已加载：{platform} 模拟后台")
    
    tab1, tab2, tab3 = st.tabs(["商品发布管理", "订单与售后", "营销推广"])
    with tab1:
        st.subheader("商品上架演练")
        st.text_input("商品标题 (限30字)", "2024新款龙年红绳手链 纯手工编织 闺蜜礼物")
        st.multiselect("选择主图空间", ["主图1", "主图2", "白底图", "详情图A", "详情图B"])
        if st.button("提交上架审核"):
            st.success("✅ 本地仿真：审核通过，商品已加入虚拟店铺货架。")
            c.execute("INSERT INTO records (module, action, score, report) VALUES ('国内淘宝', '商品上架', 90, '标准上架')")
            conn.commit()
            
    with tab2:
        st.subheader("待发货订单池")
        st.table(pd.DataFrame({"订单号": ["TB001", "TB002"], "商品": ["手链A", "手链B"], "状态": ["待发货", "异常"]}))

# ================= 5. 模块 3：跨境平台仿真 =================
elif nav == "🌍 跨境平台仿真":
    st.title("🌍 跨境通用平台仿真")
    
    platform = st.selectbox("选择跨境平台", ["Amazon (亚马逊)", "Shopee (虾皮)", "TikTok Shop", "AliExpress (速卖通)"])
    st.info(f"当前已加载：{platform} 仿真后台（语言：English）")
    
    tabs = st.tabs(["多语言 Listing 编辑", "FBA 库存与物流", "国际广告投放", "税务与合规"])
    
    with tabs[0]:
        st.subheader("Listing 优化演练")
        st.markdown("**1. Product Title (商品标题)**")
        title_en = st.text_input("Title (English)", "Handmade Red String Bracelet for Dragon Year, Lucky Charm")
        st.caption("💡 知识库提示：核心词前置 (Handmade Red String Bracelet)，避免堆砌。")
        
        st.markdown("**2. Bullet Points (五点描述)**")
        st.text_area("Bullet 1", "🐉 DRAGON YEAR SPECIAL: Perfect gift for the Year of the Dragon.")
        st.text_area("Bullet 2", "🧵 HANDMADE QUALITY: Made with durable red string.")
        
        st.markdown("**3. Backend Keywords (后台搜索词)**")
        st.text_input("Search Terms", "lucky bracelet, chinese zodiac, red rope, friendship gift")
        st.caption("💡 注意：后台词不需要逗号，用空格隔开，不要与标题重复。")
        
        if st.button("保存并发布 Listing"):
            st.success("✅ Listing 翻译检查通过，模拟发布至美国站。")

    with tabs[1]:
        st.subheader("FBA 库存模拟")
        st.progress(15, text="当前库存仅剩 15%，面临断货风险！")
        st.number_input("创建补货计划 (件)", value=500)
        st.selectbox("头程物流方式", ["海运 (慢, 约30天)", "空运 (快, 约7天)", "快递 (极快, 约3天)"])
        if st.button("提交补货单"):
            st.warning("📦 补货指令已发往工厂，预计35天后入仓。")

    with tabs[2]:
        st.subheader("广告与 ACoS 测算")
        st.slider("日预算 ($)", 10, 500, 50)
        st.number_input("竞价 (Bid $)", value=0.75)
        st.metric("预估 ACoS", "22%", "-3%")
        
    with tabs[3]:
        st.subheader("合规检查清单")
        st.checkbox("已注册目标国 VAT 税号", value=True)
        st.checkbox("产品已具备 CE 认证", value=False)
        if not st.session_state.get("warned", False):
            st.error("🚨 警告：缺少 CE 认证，在欧洲站发布属违规行为，可能被封店！")

# ================= 6. 模块 4：知识库 =================
elif nav == "📚 运营知识库":
    st.title("📚 全域运营知识库与翻译")
    st.write("结合仿真操作，随时查阅专业术语与规则：")
    
    with st.expander("📖 跨境电商高频术语 (含中英对照)"):
        st.markdown("""
        - **ACoS (Advertising Cost of Sale)**: 广告成本销售比。
        - **ODR (Order Defect Rate)**: 订单缺陷率，亚马逊重要绩效指标，高于1%可能被封店。
        - **Listing**: 商品页面（包含标题、图片、五点描述等）。
        - **FBA (Fulfillment by Amazon)**: 亚马逊代仓储代发货。
        """)
    
    with st.expander("🌍 平台规则深度拆解 (防封号指南)"):
        st.markdown("""
        **1. 知识产权侵权 (IP Infringement)**
        - **现象**：标题写了别人的牌子，或者产品外观类似某大牌。
        - **后果**：直接下架，冻结资金。
        - **演练建议**：上架前用商标查询网查一遍。
        """)
        
    st.markdown("### 🔍 一键专业翻译（仿真工具）")
    trans_text = st.text_area("粘贴英文 Listing 或平台邮件进行翻译", "Your account is at risk of suspension due to high ODR.")
    if st.button("专业电商翻译"):
        st.info("【中文对照】您的账户因订单缺陷率过高，面临被暂停（封号）的风险。")
        st.caption("💡 提示：此处为本地电商词库匹配翻译，而非普通机翻。")

# ================= 7. 模块 5：实训沙盘与复盘 =================
elif nav == "🎯 实训沙盘与复盘":
    st.title("🎯 实训操作记录与数据复盘")
    
    df = pd.read_sql_query("SELECT * FROM records ORDER BY time DESC", conn)
    if df.empty:
        st.info("暂无操作记录，快去各大仿真平台点几下吧！")
    else:
        st.metric("累计操作步数", f"{len(df)} 步")
        st.dataframe(df[["time", "module", "action", "score", "report"]], use_container_width=True, hide_index=True)

# ================= 8. 模块 6：系统设置 =================
elif nav == "⚙️ 系统设置":
    st.title("⚙️ 沙盘控制台")
    st.info("由于是纯本地仿真系统，你可以随时重置练习数据，加载新的实训场景。")
    
    st.subheader("加载预设场景")
    st.selectbox("选择实训事件", ["常规运营", "黑五大促爆单 (库存告急)", "差评危机 (遇到恶意退款)", "广告超支 (ACoS飙升)"])
    
    if st.button("加载场景并重置沙盘数据", type="primary"):
        c.execute("DELETE FROM records")
        conn.commit()
        st.success("✅ 沙盘数据已重置，新场景已加载！")
