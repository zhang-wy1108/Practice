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

# ================= 2. 页面配置 =================
st.set_page_config(page_title="高保真电商上架模拟", page_icon="🛍️", layout="wide")
st.sidebar.title("🎮 系统导航")
page = st.sidebar.radio("选择功能", ["高保真上架模拟", "我的复盘数据"])

# ================= 3. 上架模拟核心逻辑 =================
def publish_simulation():
    st.title("🛒 千牛商品发布模拟")
    st.write("请严格按照流程填写，系统将模拟淘宝的发布审核机制。")

    # 使用 tabs 实现千牛后台的界面感
    tab1, tab2, tab3, tab4 = st.tabs(["1. 类目与品牌", "2. 基础信息(标题/属性)", "3. 销售信息(SKU/价格)", "4. 物流与服务"])

    with tab1:
        st.subheader("商品类目选择")
        search_cat = st.text_input("搜索类目（例如输入：手链）")
        if search_cat:
            st.radio("选择系统匹配的类目：", [
                "饰品/流行首饰/时尚饰品新 > 手链",
                "珠宝/钻石/翡翠 > 翡翠 > 手链/手串",
                "特色手工艺 > 佛教工艺品"
            ])
        st.subheader("品牌选择")
        brand = st.selectbox("选择品牌（无品牌请选无品牌）", ["请选择", "无品牌", "卡地亚", "周大福", "自建品牌"])
        
    with tab2:
        st.subheader("宝贝标题（60个字符限制）")
        st.caption("系统提供的词库：龙年、红绳、本命年、招财、原创、925银、手链、闺蜜礼物、国潮")
        title = st.text_input("请输入标题", max_chars=60)
        st.subheader("商品属性（填得越全流量越高）")
        col1, col2 = st.columns(2)
        with col1:
            material = st.selectbox("材质", ["请选择", "925银", "红绳", "黄金"])
            style = st.selectbox("风格", ["请选择", "国潮", "复古", "简约"])
        with col2:
            gender = st.selectbox("适用性别", ["请选择", "女", "男", "情侣"])
            is_custom = st.radio("是否定制", ["是", "否"], index=1)

    with tab3:
        st.subheader("SKU设置（颜色/规格）")
        sku_name = st.text_input("颜色分类（如：龙年红绳款）", value="")
        price = st.number_input("一口价（元）", min_value=1.0, value=99.0)
        stock = st.number_input("库存数量", min_value=0, value=50)
        
        st.subheader("上传图片空间")
        st.info("这里模拟主图上传。当前已自动匹配 1:1 主图3张，详情图1张。")
        st.file_uploader("（演示）拖拽真实图片上传", accept_multiple_files=True)

    with tab4:
        st.subheader("物流与服务")
        delivery_time = st.selectbox("发货时间", ["4小时内发货", "24小时内发货", "48小时内发货"])
        freight = st.selectbox("运费模板", ["卖家默认运费模板（包邮）", "偏远地区加邮费"])
        st.radio("退换货承诺", ["支持7天无理由退货（必选）", "不支持"])

    st.divider()
    
    # 提交审核
    if st.button("🚀 提交宝贝信息（模拟审核）", type="primary", use_container_width=True):
        score = 100
        report = []
        
        # 模拟审核逻辑
        if brand == "请选择":
            score -= 30
            report.append("❌ 品牌未选择，严重影响转化。")
        elif brand in ["卡地亚", "周大福"]:
            score = 0
            report.append("❌ 严重违规！涉嫌售卖假冒品牌，直接封店。")
            
        if len(title) < 20:
            score -= 10
            report.append("⚠️ 标题过短，无法覆盖足够的搜索词。")
        if "龙年" not in title and "手链" not in title:
            score -= 15
            report.append("⚠️ 标题缺少核心词（龙年/手链），曝光量低。")
            
        if material == "请选择" or style == "请选择":
            score -= 15
            report.append("⚠️ 属性未填写完整，系统无法精准打标签。")
            
        if price < 30:
            report.append("⚠️ 售价过低，注意算上运费和扣点是否亏本。")
            
        if stock == 0:
            score -= 20
            report.append("❌ 库存为0，商品发布后将会直接下架。")

        if score >= 80:
            st.success(f"✅ 审核通过！本次模拟得分：{score} 分")
        elif score > 0:
            st.warning(f"⚠️ 勉强过审，但存在隐患。得分：{score} 分")
        else:
            st.error(f"❌ 审核失败！得分：{score} 分")

        st.write("**🩺 系统体检报告：**")
        for r in report:
            st.write(r)
            
        st.info("📖 **本次术语**：SPU（标准化产品单元，指整个手链） / SKU（库存量单位，指红绳款、黑绳款等具体选项） / 流量漏斗。")

        # 记录成绩
        c.execute("INSERT INTO records (center, scene, decision, score, terms) VALUES (?, ?, ?, ?, ?)",
                  ("淘宝发布模拟", "手链上架", f"品牌:{brand}, 标题:{title}, 价格:{price}", score, "SPU/SKU/流量漏斗"))
        conn.commit()
        st.toast("✅ 成绩已保存至复盘看板！")

# ================= 4. 页面路由 =================
if page == "高保真上架模拟":
    publish_simulation()
elif page == "我的复盘数据":
    st.title("📊 我的复盘与数据看板")
    df = pd.read_sql_query("SELECT * FROM records ORDER BY time DESC", conn)
    if df.empty:
        st.info("暂无记录，快去模拟一次上架吧！")
    else:
        st.dataframe(df[["time", "center", "score", "decision"]], use_container_width=True)
