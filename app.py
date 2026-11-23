import streamlit as st
import random
import sqlite3
import pandas as pd

# ================= 1. 页面设置 =================
st.set_page_config(page_title="电商店铺运营工作台", page_icon="🛍️", layout="wide")

# 隐藏默认的菜单，让它更像一个独立软件
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

# ================= 2. 左侧导航栏 =================
with st.sidebar:
    st.title("🛒 运营工作台")
    st.caption("高保真全流程演练")
    st.divider()
    
    # 顶层导航菜单 (已加入跨境模块)
    menu = st.radio(
        "导航菜单",
        [
            "🏠 经营总览", 
            "🛒 淘宝模拟平台", 
            "🌍 跨境平台模拟 (亚马逊)",
            "🛒 拼多多模拟平台 (待建)",
            "📊 经营复盘", 
            "📚 资料库"
        ]
    )

# ================= 3. 各个页面的内容 =================

# ---------------- 页面 1：经营总览 ----------------
if menu == "🏠 经营总览":
    st.title("📈 经营总览")
    
    # 顶部四个状态卡片
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(label="📦 待发货", value="12", delta="需尽快处理", delta_color="normal")
    c2.metric(label="🚚 发货中", value="34", delta="物流更新中", delta_color="off")
    c3.metric(label="⚠️ 异常物流", value="2", delta="需人工介入", delta_color="inverse")
    c4.metric(label="🎧 售后待处理", value="3", delta="退款/换货", delta_color="off")
    
    st.divider()
    
    # 订单处理队列
    st.subheader("📋 订单处理队列")
    df_orders = pd.DataFrame({
        "商品": ["收纳盒", "便携水杯", "桌面置物架"],
        "当前状态": ["🟡 待发货", "🔵 发货中", "🔴 异常物流"],
        "处理提醒": ["核对地址", "物流更新", "联系承运方"],
        "操作": ["查看", "查看", "跟进"]
    })
    st.dataframe(df_orders, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # 履约进度
    st.subheader("🚀 履约进度")
    st.write("待发货 (12)  ➡️  发货中 (34)  ➡️  已签收 (89)")
    st.progress(70)
    st.error("⚠️ 异常物流 2 笔，请及时处理以免影响 DSR 评分。")


# ---------------- 页面 2：淘宝模拟平台 ----------------
elif menu == "🛒 淘宝模拟平台":
    st.title("🐮 千牛 · 商品发布模拟")
    st.info("请按照真实后台流程完成商品上架，提交后系统将模拟审核。")
    
    tab1, tab2, tab3 = st.tabs(["1. 选类目与品牌", "2. 填标题与属性", "3. 设价格与库存"])
    
    with tab1:
        st.text_input("搜索类目（如：手链）", value="手链")
        st.radio("选择类目：", ["饰品/流行首饰/时尚饰品新 > 手链", "珠宝/钻石/翡翠 > 手链"])
        st.selectbox("品牌选择", ["无品牌", "其他品牌", "卡地亚(侵权风险)"])
        
    with tab2:
        st.text_input("宝贝标题（限60字符，核心词：龙年 手链）", max_chars=60)
        st.multiselect("商品属性", ["材质:红绳", "风格:国潮", "适用性别:女"])
        
    with tab3:
        st.number_input("一口价 (元)", min_value=1.0, value=99.0)
        st.number_input("库存数量", min_value=0, value=50)
        
    st.divider()
    if st.button("🚀 提交宝贝信息（触发审核）", type="primary"):
        st.success("✅ 审核通过！已成功上架。")
        st.info("📖 **术语提示**：SPU（标准化产品单元，即这款手链） / SKU（红绳款、黑绳款）")


# ---------------- 页面 3：跨境平台模拟 (新增) ----------------
elif menu == "🌍 跨境平台模拟 (亚马逊)":
    st.title("🌍 亚马逊 · FBA 全成本利润核算")
    st.info("跨境电商与国内最大的不同在于成本结构（头程、FBA费、汇率、佣金）。请计算真实的单件净利。")
    
    # 分成两列：左侧输入，右侧算账
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("📦 成本参数")
        cost_rmb = st.number_input("采购成本 (RMB)", value=30)
        first_mile = st.number_input("头程物流费 (First-mile) /单件 (RMB)", value=15)
        referral_rate = st.slider("平台佣金比例 (Referral Fee %)", 0, 30, 15)
        fba_fee_rmb = st.number_input("FBA 配送费 (RMB)", value=30)
        acos = st.slider("广告花费占比 (ACoS %)", 0, 50, 20)
        
    with col_right:
        st.subheader("💵 定价与利润")
        price_usd = st.number_input("前台售价 (USD)", value=19.99)
        exchange_rate = st.number_input("美元汇率 (USD/RMB)", value=7.20)
        
        # 计算逻辑
        price_rmb = price_usd * exchange_rate
        commission = price_rmb * (referral_rate / 100)
        ad_cost = price_rmb * (acos / 100)
        
        total_cost = cost_rmb + first_mile + commission + fba_fee_rmb + ad_cost
        net_profit = price_rmb - total_cost
        margin = (net_profit / price_rmb) * 100
        
        st.write("---")
        st.metric(label="折合人民币总售价", value=f"¥ {price_rmb:.2f}")
        st.metric(label="单件总成本", value=f"¥ {total_cost:.2f}")
        
        if net_profit > 0:
            st.success(f"✅ 单件净利润：¥ {net_profit:.2f} (净利率 {margin:.1f}%)")
        else:
            st.error(f"❌ 严重亏损！单件亏损：¥ {abs(net_profit):.2f}")

        if st.button("提交核算报告", type="primary"):
            st.info("📖 **术语提示**：FBA（Fulfillment by Amazon，亚马逊代发货）、ACoS（广告花费/广告销售额）、Referral Fee（平台佣金）。")


# ---------------- 页面 4：经营复盘 ----------------
elif menu == "📊 经营复盘":
    st.title("📊 我的复盘与错题本")
    st.write("这里会记录你做错的操作，比如：标题堆砌关键词、运费模板设错、库存填0等。")
    st.info("暂无复盘数据，快去模拟平台发布一个商品或核算一次利润吧！")


# ---------------- 页面 5：资料库 ----------------
elif menu == "📚 资料库":
    st.title("📚 运营资料库")
    st.write("随时查阅专业术语与避坑指南：")
    
    with st.expander("📖 国内电商术语库 (点击展开)"):
        st.markdown("""
        - **SPU (Standard Product Unit)**: 标准化产品单元。例如“某款龙年手链”就是一个 SPU。
        - **SKU (Stock Keeping Unit)**: 库存量单位。例如“红绳款”、“黑绳款”就是两个不同的 SKU。
        - **DSR**: 卖家服务评级系统（描述相符、服务态度、发货速度）。
        """)
        
    with st.expander("🌍 跨境电商术语库 (点击展开)"):
        st.markdown("""
        - **FBA (Fulfillment by Amazon)**: 亚马逊物流，卖家把货发到亚马逊仓库，由亚马逊负责打包发货。
        - **ACoS (Advertising Cost of Sale)**: 广告成本销售比。公式：广告花费 / 广告带来的销售额。
        - **TACoS**: 总广告成本销售比。公式：广告花费 / 总销售额。用来衡量广告对整体业务的拉动。
        - **First-mile (头程)**: 把货物从中国工厂运到海外亚马逊仓库的过程。
        """)
        
    with st.expander("⚠️ 违规知识库 (点击展开)"):
        st.markdown("""
        - **极限词**：标题或详情页绝对不能出现“第一”、“最好”、“国家级”等词汇，直接扣分。
        - **类目错放**：把手链放在“首饰”类目下流量大，如果乱放在“礼品”类目，会被降权。
        - **知识产权侵权**：国内千万别乱标品牌，跨境千万别卖带“迪士尼”、“漫威”图案的产品，直接封店。
        """)

# 未开放模块提示
elif "待建" in menu:
    st.warning("该平台模块正在搭建中，目前请先在淘宝或亚马逊模拟平台进行练习！")
