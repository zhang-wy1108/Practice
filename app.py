import streamlit as st
import pandas as pd
import sqlite3
import altair as alt
from datetime import datetime

# ================= 1. 页面与数据库配置 =================
st.set_page_config(page_title="全域电商高仿真实训台", page_icon="🌐", layout="wide")
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

conn = sqlite3.connect('practice_record.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS records
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              platform TEXT, module TEXT, action TEXT, score INTEGER, report TEXT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# ================= 2. 左侧主导航 =================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/shop.png", width=60)
    st.title("全域仿真实训台")
    st.caption("纯沙盘演练 · 无真实接口")
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
    st.info("💡 提示：此处为沙盘模拟数据。你可在左侧【系统设置】中重置场景。")
    
    tab_dom, tab_cross = st.tabs(["🇨🇳 国内店铺数据", "🌍 跨境店铺数据"])
    
    with tab_dom:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("国内总 GMV", "¥ 125,400", "+12%")
        c2.metric("订单量", "3,240 单", "+5%")
        c3.metric("整体转化率", "3.2%", "-0.1%")
        c4.metric("广告 ROI", "2.5", "持平")
        
    with tab_cross:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("跨境总 GMV", "$ 18,500", "+22%")
        c2.metric("订单量", "890 单", "+15%")
        c3.metric("综合 ACoS", "18%", "优化中")
        c4.metric("平均净利率", "15.5%", "+1.2%")

# ================= 4. 模块 2：国内电商高仿真 =================
elif nav == "🇨🇳 国内电商仿真":
    st.title("🇨🇳 国内电商后台实操")
    
    # 平台选择
    plat_dom = st.selectbox("切换平台后台", ["淘宝/天猫 (千牛)", "京东 (京麦)", "抖音电商 (抖店)", "拼多多 (商家后台)"])
    
    # 顶层 Tabs
    t1, t2, t3, t4 = st.tabs(["📦 商品发布", "📋 订单与售后", "📈 营销与推广", "💬 客户与评价"])
    
    # ---------------- 商品发布 ----------------
    with t1:
        st.subheader(f"【{plat_dom}】商品发布高仿真")
        
        # 差异化设计：淘宝和抖音注重图文，京东注重参数，拼多多注重价格
        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.markdown("**1. 类目与品牌**")
            if "拼多多" in plat_dom:
                st.caption("💡 拼多多提示：类目错放会直接限制流量。")
            st.selectbox("发布类目", ["女装/女士精品 > 毛呢大衣", "饰品/流行首饰 > 手链", "家居日用 > 收纳"])
            st.selectbox("品牌", ["无品牌", "自定义品牌"])
            
            st.markdown("**2. 标题与卖点**")
            title = st.text_input("商品标题 (限60字符)", max_chars=60, placeholder="请输入核心长尾词...")
            if "抖音" in plat_dom:
                st.text_area("抖音短标题 (需有吸引力)", "爆款清仓！纯手工编织龙年红绳，招财转运必备！")
                
            st.markdown("**3. 主图与视频**")
            st.file_uploader("上传 1:1 主图 (限5张)", accept_multiple_files=True, key="dom_img")
            
        with col_right:
            st.markdown("**4. 销售规格 (SKU) 与库存**")
            sku_color = st.text_input("颜色分类", "经典红 / 玫瑰金")
            price = st.number_input("一口价 (元)", value=199.0)
            stock = st.number_input("总库存", value=500)
            
            if "京东" in plat_dom:
                st.markdown("**5. 京东专属：商品参数**")
                st.selectbox("材质", ["纯棉", "聚酯纤维", "真皮"])
                st.text_input("商品编号", "JD-998877")
                
            st.markdown("**6. 物流与服务**")
            st.selectbox("发货时间", ["24小时内", "48小时内"])
            st.checkbox("支持7天无理由退货", value=True)
            
            if "拼多多" in plat_dom:
                st.number_input("拼单返现 (元)", value=10.0)
                
        st.divider()
        if st.button("🚀 提交上架审核", use_container_width=True, type="primary"):
            score = 90
            report = "各项指标正常，成功上架。"
            if len(title) < 10:
                score = 40
                report = "❌ 标题过短，搜索流量极低。"
            elif stock < 10:
                score = 60
                report = "⚠️ 库存预警：库存过低，可能影响活动报名。"
                
            st.success(f"系统判定得分：{score} 分")
            st.write(f"体检报告：{report}")
            c.execute("INSERT INTO records (platform, module, action, score, report) VALUES (?, ?, ?, ?, ?)", 
                      (plat_dom, "商品发布", title, score, report))
            conn.commit()

    # ---------------- 订单与售后 ----------------
    with t2:
        st.subheader("📋 订单处理队列")
        df_orders = pd.DataFrame({
            "订单号": ["TB2024-001", "TB2024-002", "TB2024-003"],
            "商品": ["毛呢大衣", "红绳手链", "桌面收纳"],
            "买家备注": ["发顺丰", "无", "不要放快递柜"],
            "当前状态": ["🟡 待发货", "🔵 发货中", "🔴 异常物流"],
            "操作": ["处理", "查看", "联系物流"]
        })
        st.dataframe(df_orders, use_container_width=True, hide_index=True)
        
        st.markdown("**售后工作台**")
        with st.expander("退款/退货待处理 (2)"):
            st.write("买家申请仅退款：衣服尺码不合适，但吊牌已剪。")
            st.radio("你的操作：", ["同意退款", "拒绝退款并说明规则", "协商换货"])
            if st.button("提交处理意见"):
                st.info("处理结果已记录。查看知识库确认是否属于你责任。")

    # ---------------- 营销推广 ----------------
    with t3:
        st.subheader("📈 国内直通车/千川 投放模拟")
        st.write("模拟场景：新品起盘，日预算 200 元。")
        col_a, col_b = st.columns(2)
        with col_a:
            st.slider("出价 (元/点击)", 0.1, 5.0, 1.5)
        with col_b:
            st.slider("日限额 (元)", 50, 1000, 200)
            
        if st.button("启动推广计划"):
            st.success("计划已建立！系统正在模拟 24 小时点击与转化...")
            st.metric("预估点击率 CTR", "3.5%", "高于同行 1%")
            st.metric("预估转化率 CVR", "2.1%", "持平")
            c.execute("INSERT INTO records (platform, module, action, score, report) VALUES (?, ?, ?, ?, ?)", 
                      (plat_dom, "营销推广", "新建直通车", 85, "ROI待观察"))
            conn.commit()

    # ---------------- 客户评价 ----------------
    with t4:
        st.subheader("💬 评价与 DSR 管理")
        st.warning("⚠️ 发现差评：买家说“实物颜色有色差，再也不买了”。")
        reply = st.text_area("你的客服回复：", "亲，非常抱歉让您失望了！由于显示器不同确实可能存在微小色差。如果您不喜欢，我们支持退货退款，运费我们承担。")
        if st.button("提交回复"):
            if "退货" in reply and "抱歉" in reply:
                st.success("✅ 回复完美！有效安抚情绪，大概率免除投诉。")
                c.execute("INSERT INTO records (platform, module, action, score, report) VALUES (?, ?, ?, ?, ?)", 
                          (plat_dom, "客服售后", "处理差评", 100, "回复标准"))
                conn.commit()
            else:
                st.error("❌ 回复生硬，可能激怒买家引发投诉，扣分。")


# ================= 5. 模块 3：跨境平台高仿真 =================
elif nav == "🌍 跨境平台仿真":
    st.title("🌍 跨境平台后台实操")
    
    plat_cross = st.selectbox("切换平台后台", ["Amazon (亚马逊)", "Shopee (虾皮)", "TikTok Shop", "AliExpress (速卖通)"])
    
    # 因为亚马逊的机制最复杂，这里根据平台动态展示
    st.info(f"当前加载后台语言：English (英文) / 可在右上角切换中文辅助")
    
    tc1, tc2, tc3, tc4 = st.tabs(["📝 Listing 编辑器", "📦 FBA 库存与物流", "📈 站内广告 (Ads)", "⚖️ 税务与合规"])
    
    # ---------------- 1. Listing ----------------
    with tc1:
        st.subheader("多语言 Listing 发布")
        
        if "Amazon" in plat_cross:
            st.caption("💡 亚马逊有严格的字符限制和格式要求。")
            title = st.text_input("Product Title (最多200字符)", "Handmade Lucky Red String Bracelet for Dragon Year")
            st.text_area("Bullet Point 1 (卖点1)", "🐉 PERFECT GIFT: Best wishes for the Dragon year.")
            st.text_area("Bullet Point 2 (卖点2)", "🧵 HANDMADE: Braided by local artisans with premium red rope.")
            st.text_area("Description (A+页面文本)", "This bracelet brings good luck and fortune...")
            st.text_input("Backend Search Terms (后台搜索词, 无需逗号)", "red bracelet lucky charm chinese zodiac")
        elif "Shopee" in plat_cross:
            st.caption("💡 Shopee 更看重 hashtag 标签和促销词。")
            title = st.text_input("Product Name (标题)", "Ready Stock! Dragon Year Red String Bracelet Limited Edition")
            st.text_input("Hashtags (标签)", "#luckybracelet #dragon2024 #freeshipping")
        else:
            title = st.text_input("Product Title", "Dragon Year Lucky Red Rope")
            
        if st.button("保存并提交审核 (Submit)"):
            st.success("✅ 关键词扫描通过，翻译无语法错误，模拟发布成功。")
            c.execute("INSERT INTO records (platform, module, action, score, report) VALUES (?, ?, ?, ?, ?)", 
                      (plat_cross, "Listing编辑", title, 95, "优化良好"))
            conn.commit()

    # ---------------- 2. 物流 ----------------
    with tc2:
        st.subheader("跨境仓储与头程物流模拟")
        st.markdown("**1. 当前库存快照**")
        st.table(pd.DataFrame({
            "SKU": ["红绳-均码", "红绳-大码"],
            "可用库存 (FBA)": [12, 150],
            "在途库存 (海运)": [500, 0],
            "状态": ["🔴 严重断货预警", "🟢 健康"]
        }))
        
        st.markdown("**2. 创建补货计划 (Restock)**")
        st.number_input("发货数量 (件)", value=1000)
        st.selectbox("头程方式", ["海运 (Sea Freight, 30-40天)", "空运 (Air Freight, 7-10天)", "快递 (Express, 3天)"])
        if st.button("生成发货单 (Shipment Plan)"):
            st.info("📦 已生成 FBA 入仓计划，请下载 PDF 标签贴在外箱上。")

    # ---------------- 3. 广告 ----------------
    with tc3:
        st.subheader("站内广告投放 (SP/SB/SD)")
        st.write("当前广告目标：提升新品曝光")
        budget = st.number_input("Daily Budget (日预算 $)", value=50.0)
        bid = st.number_input("Default Bid (默认竞价 $)", value=0.75)
        
        if st.button("启动广告活动 (Launch Campaign)"):
            st.success("🚀 Campaign 已建立，系统正在收集数据...")
            st.metric("预估 ACoS", "25%", "偏高")
            st.metric("预估转化率", "12%")
            st.info("💡 优化建议：ACoS 偏高，建议下调竞价至 $0.60 或优化 Listing 主图。")

    # ---------------- 4. 税务 ----------------
    with tc4:
        st.subheader("跨境合规雷达")
        st.checkbox("已注册美国 EIN 税号")
        st.checkbox("已注册欧洲 VAT (增值税)", value=False)
        st.checkbox("该产品已完成 FDA / CE 认证")
        if st.button("提交合规审查"):
            st.error("🚨 审查未通过：缺少欧洲 VAT 和 CE 认证。如果发往欧洲站，极易被海关扣留并面临高额罚款！")


# ================= 6. 模块 4：知识库 =================
elif nav == "📚 运营知识库":
    st.title("📚 运营知识库与多语言翻译")
    
    tab_dict, tab_rule, tab_trans = st.tabs(["术语词典", "平台规则解读", "一键翻译工具"])
    
    with tab_dict:
        st.markdown("""
        ### 📖 常用术语对照
        | 术语 (缩写) | 英文全称 | 中文解释 |
        |---|---|---|
        | **SPU** | Standard Product Unit | 标准化产品单元（一款商品） |
        | **SKU** | Stock Keeping Unit | 库存量单位（一款商品的不同颜色/尺码） |
        | **ACoS** | Advertising Cost of Sale | 广告成本销售比 (花费/销售额) |
        | **ROI** | Return on Investment | 投资回报率 (利润/花费) |
        | **ODR** | Order Defect Rate | 订单缺陷率（跨境亚马逊核心指标）|
        """)
        
    with tab_rule:
        st.markdown("""
        ### ⚠️ 违规红线速查
        - **极限词违规**：国内《广告法》严禁使用“第一”、“最好”、“国家级”等词汇，一经发现直接扣分下架。
        - **防伪与侵权**：跨境严打知识产权侵权，未获授权不能使用任何大牌图案（如迪士尼、漫威）或外观专利。
        - **类目错放**：淘宝/亚马逊都会对类目进行严格校验，放错类目会导致搜索流量归零。
        """)
        
    with tab_trans:
        st.text_area("粘贴需要翻译的专业内容", "Your account has been suspended due to a high ODR. Please submit a Plan of Action (POA) immediately.")
        if st.button("专业电商翻译"):
            st.success("【中文译文】由于您的订单缺陷率（ODR）过高，您的账户已被暂停。请立即提交行动计划（POA）。")
            st.caption("💡 翻译库已优先匹配：ODR -> 订单缺陷率, POA -> 行动计划")

# ================= 7. 模块 5：实训复盘 =================
elif nav == "🎯 实训沙盘与复盘":
    st.title("🎯 实训复盘中心")
    st.write("系统记录了你所有的仿真操作与系统评分，可反复观摩优化。")
    
    df = pd.read_sql_query("SELECT * FROM records ORDER BY time DESC", conn)
    if df.empty:
        st.info("暂无实操记录，快去国内或跨境平台发布一个商品吧！")
    else:
        st.metric("累计实操步数", f"{len(df)} 步")
        st.metric("平均操作得分", f"{df['score'].mean():.1f} 分")
        
        st.subheader("📋 历史操作日志")
        st.dataframe(df[["time", "platform", "module", "score", "report"]], use_container_width=True, hide_index=True)

# ================= 8. 模块 6：系统设置 =================
elif nav == "⚙️ 系统设置":
    st.title("⚙️ 沙盘重置与设置")
    st.warning("🚨 注意：以下操作会清空历史练习数据！")
    if st.button("重置所有模拟店铺数据与成绩", type="primary"):
        c.execute("DELETE FROM records")
        conn.commit()
        st.success("✅ 所有数据已清零，系统恢复至初始状态。")
