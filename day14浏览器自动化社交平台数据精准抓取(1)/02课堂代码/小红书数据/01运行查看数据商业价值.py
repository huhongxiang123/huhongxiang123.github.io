import pandas as pd
import json
import os
import webbrowser

# ====================== Python后端默认阈值（页面初始化默认值） ======================
DEFAULT_MIN_TOTAL_INTERACT = 100  # 默认最低总互动
DEFAULT_MIN_NOTE_COUNT = 1        # 默认最少笔记

# ====================== 数据处理模块（读取类别、详情页、双重过滤） ======================
def process_blogger_data():
    try:
        df = pd.read_csv("小红书帖子.csv", encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv("小红书帖子.csv", encoding="gbk")
    df.columns = df.columns.str.strip()

    # 聚合字段：id,name,头像,类别,详情页
    author_agg = df.groupby(["id", "name", "头像", "类别", "详情页"]).agg(
        总点赞=("点赞", "sum"),
        总收藏=("收藏", "sum"),
        总评论=("评论", "sum"),
        总分享=("分享", "sum"),
        笔记数量=("标题", "count")
    ).reset_index()

    author_agg["总互动量"] = author_agg["总点赞"] + author_agg["总收藏"] + author_agg["总评论"] + author_agg["总分享"]

    # 门槛校验结果
    def check_threshold(row):
        note_ok = row["笔记数量"] >= DEFAULT_MIN_NOTE_COUNT
        interact_ok = row["总互动量"] >= DEFAULT_MIN_TOTAL_INTERACT
        if note_ok and interact_ok:
            return "双门槛全部达标"
        elif not note_ok:
            return f"笔记不足{DEFAULT_MIN_NOTE_COUNT}"
        else:
            return f"总互动不足{DEFAULT_MIN_TOTAL_INTERACT}"
    author_agg["门槛校验结果"] = author_agg.apply(check_threshold, axis=1)

    # 计算比值
    def calc_ratio(row):
        like = row["总点赞"]
        collect = row["总收藏"]
        comment = row["总评论"]
        cr = collect / like if like > 0 else 0.0
        cm = comment / like if like > 0 else 0.0
        return round(cr, 3), round(cm, 3)
    author_agg[["收藏点赞比", "评论点赞比"]] = author_agg.apply(lambda x: pd.Series(calc_ratio(x)), axis=1)

    # 分层判定（Python导出CSV使用默认阈值）
    def get_blogger_type(row):
        if row["笔记数量"] < DEFAULT_MIN_NOTE_COUNT or row["总互动量"] < DEFAULT_MIN_TOTAL_INTERACT:
            return "普通低价值博主"
        cr = row["收藏点赞比"]
        cmr = row["评论点赞比"]
        if cr > 0.3 and cmr < 0.08:
            return "高收藏带货型"
        elif cmr > 0.15 and cr < 0.15:
            return "高讨论声量型"
        elif 0.15 <= cr <= 0.25 and 0.08 <= cmr <= 0.15:
            return "均衡全能型"
        else:
            return "普通低价值博主"
    author_agg["博主类型"] = author_agg.apply(get_blogger_type, axis=1)

    # 投放建议
    def get_suggest(row):
        t = row["博主类型"]
        if t == "高收藏带货型":
            return "优先复投，适合挂车、引导搜索转化，深度年框/独家合作"
        elif t == "高讨论声量型":
            return "新品造势、品牌话题引爆，不适合直接带货转化"
        elif t == "均衡全能型":
            return "品效合一投放，兼顾曝光与商品转化"
        else:
            if row["笔记数量"] < DEFAULT_MIN_NOTE_COUNT:
                return f"笔记仅{row['笔记数量']}条，无内容基础，不建议投放"
            elif row["总互动量"] < DEFAULT_MIN_TOTAL_INTERACT:
                return f"总互动仅{row['总互动量']}，流量薄弱，不建议投放"
            else:
                return "转化比值一般，性价比偏低"
    author_agg["投放建议"] = author_agg.apply(get_suggest, axis=1)

    # 输出完整CSV
    author_agg.to_csv("博主分层打分结果.csv", index=False, encoding="utf-8-sig")
    print("✅ 已生成：博主分层打分结果.csv（使用默认阈值：笔记≥{}、总互动≥{}）".format(DEFAULT_MIN_NOTE_COUNT, DEFAULT_MIN_TOTAL_INTERACT))

    # 全部博主原始数据传给前端（前端自己动态过滤，不提前裁剪）
    keep_cols = [
        "id", "name", "头像", "类别", "详情页",
        "总点赞", "总收藏", "总评论", "总分享", "笔记数量",
        "收藏点赞比", "评论点赞比", "博主类型", "投放建议", "总互动量"
    ]
    all_bloggers = author_agg[keep_cols].to_dict("records")
    with open("blogger_data.json", "w", encoding="utf-8") as f:
        json.dump(all_bloggers, f, ensure_ascii=False, indent=2)
    print("✅ 已生成：blogger_data.json（包含全部博主，前端可动态修改阈值筛选）")
    return all_bloggers

# ====================== 生成HTML页面（新增阈值修改弹窗、双击编辑阈值） ======================
def generate_html(blogger_json_data):
    json_str = json.dumps(blogger_json_data, ensure_ascii=False)
    html_content = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>小红书博主投放分层决策平台</title>
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css">
<script>
window.tailwind = {{ config: {{ suppressWarnings: true }} }}
tailwind.config = {{
    theme: {{
        extend: {{
            colors: {{
                primary: '#D92550',
                secondary: '#1E293B',
                success: '#10B981',
                discuss: '#6366F1',
                balance: '#0EA5E9',
                dark: '#0F172A',
                category: '#F97316'
            }}
        }}
    }}
}}
</script>
<style>
* {{box-sizing: border-box;}}
body {{margin:0;padding:0;font-family:system-ui,-apple-system,sans-serif;background:#0F172A;color:#e5e7eb;}}
.glass{{background:rgba(30,41,59,0.7);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);}}
.card-shadow{{box-shadow:0 10px 30px rgba(217,37,80,0.15);}}
.text-gradient{{background:linear-gradient(90deg,#D92550,#F59E0B);-webkit-background-clip:text;color:transparent;}}
.avatar-circle{{width:56px;height:56px;border-radius:9999px;object-fit:cover;border:2px solid rgba(255,255,255,0.2);}}
img[loading="lazy"]{{background:#334155;}}
.card-hover{{transition:transform 0.3s ease;}}
.card-hover:hover{{transform:scale(1.02);}}
.blogger-grid{{display:grid;grid-template-columns:repeat(1,1fr);gap:24px;}}
@media(min-width:768px){{.blogger-grid{{grid-template-columns:repeat(2,1fr);}}}}
@media(min-width:1024px){{.blogger-grid{{grid-template-columns:repeat(3,1fr);}}}}
@media(min-width:1280px){{.blogger-grid{{grid-template-columns:repeat(4,1fr);}}}}
.container{{max-width:1400px;margin:0 auto;padding:0 24px;}}
.tab-btn.active{{border-bottom:2px solid #10B981;color:#10B981;}}
.click-tag {{cursor:pointer;}}
.click-tag:hover {{opacity:0.7;}}
/* 双击编辑阈值文字样式 */
.double-click-edit {{cursor:pointer;text-decoration:dashed underline rgba(255,255,255,0.4);}}
.modal-mask{{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:99;display:flex;align-items:center;justify-content:center;}}
.modal-box{{width:420px;background:#1E293B;border-radius:12px;padding:24px;border:1px solid #444;}}
</style>
</head>
<body class="bg-dark text-gray-100 min-h-screen">
<!-- 阈值修改弹窗 -->
<div id="thresholdModal" class="modal-mask hidden">
    <div class="modal-box">
        <h3 class="text-xl font-bold mb-4 text-white">修改优质博主筛选阈值</h3>
        <div class="mb-4">
            <label class="block text-gray-300 mb-2">最低笔记数量：</label>
            <input id="inputMinNote" type="number" min="0" value="{DEFAULT_MIN_NOTE_COUNT}" class="w-full bg-dark border border-gray-600 rounded px-3 py-2 text-white">
        </div>
        <div class="mb-6">
            <label class="block text-gray-300 mb-2">最低总互动量：</label>
            <input id="inputMinInteract" type="number" min="0" value="{DEFAULT_MIN_TOTAL_INTERACT}" class="w-full bg-dark border border-gray-600 rounded px-3 py-2 text-white">
        </div>
        <div class="flex gap-3 justify-end">
            <button id="cancelThreshold" class="px-4 py-2 bg-gray-700 rounded hover:bg-gray-600">取消</button>
            <button id="saveThreshold" class="px-4 py-2 bg-primary rounded hover:opacity-90">保存并刷新</button>
        </div>
    </div>
</div>

<header class="glass sticky top-0 z-50 border-b border-gray-700/50">
    <div class="container px-6 py-4 flex flex-wrap justify-between items-center gap-4">
        <div class="flex items-center gap-3">
            <i class="fa fa-bar-chart text-primary text-2xl"></i>
            <h1 class="text-2xl font-bold text-gradient">小红书博主投放分层决策平台</h1>
        </div>
        <div class="flex gap-4 items-center flex-wrap">
            <!-- 阈值显示区：双击文字打开弹窗 -->
            <div class="bg-secondary rounded-lg px-3 py-2 text-sm">
                优质博主门槛：笔记≥<span id="showMinNote" class="double-click-edit">{DEFAULT_MIN_NOTE_COUNT}</span>
                总互动≥<span id="showMinInteract" class="double-click-edit">{DEFAULT_MIN_TOTAL_INTERACT}</span>
                <span class="text-gray-400 text-xs">(双击数字修改)</span>
            </div>
            <div class="relative">
                <input id="searchInput" placeholder="搜索博主昵称/ID" class="bg-secondary border border-gray-600 rounded-lg px-4 py-2 w-64 focus:outline-none focus:border-primary">
                <i class="fa fa-search absolute right-3 top-3 text-gray-400"></i>
            </div>
            <select id="categorySelect" class="bg-secondary border border-gray-600 rounded-lg px-3 py-2">
                <option value="all_category">全部类别</option>
            </select>
            <select id="sortSelect" class="bg-secondary border border-gray-600 rounded-lg px-3 py-2">
                <option value="collect_rate_desc">按收藏转化比 降序</option>
                <option value="collect_rate_asc">按收藏转化比 升序</option>
                <option value="total_interact_desc">总互动量 降序</option>
                <option value="total_interact_asc">总互动量 升序</option>
            </select>
        </div>
    </div>
</header>

<main class="container px-6 py-8">
    <section class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        <div class="glass rounded-xl p-6 card-shadow border border-primary/20 relative overflow-hidden">
            <p class="text-gray-400 text-sm">当前筛选优质博主总数</p>
            <h2 id="totalCount" class="text-3xl font-bold mt-2 text-primary">0</h2>
            <i class="fa fa-shopping-bag absolute right-6 top-6 text-3xl text-primary/30"></i>
        </div>
        <div class="glass rounded-xl p-6 card-shadow border border-success/20 relative overflow-hidden">
            <p class="text-gray-400 text-sm">高收藏带货池</p>
            <h2 id="sellCount" class="text-3xl font-bold mt-2 text-success">0</h2>
            <i class="fa fa-heart absolute right-6 top-6 text-3xl text-success/30"></i>
        </div>
        <div class="glass rounded-xl p-6 card-shadow border border-discuss/20 relative overflow-hidden">
            <p class="text-gray-400 text-sm">声量话题造势池</p>
            <h2 id="talkCount" class="text-3xl font-bold mt-2 text-discuss">0</h2>
            <i class="fa fa-comments absolute right-6 top-6 text-3xl text-discuss/30"></i>
        </div>
        <div class="glass rounded-xl p-6 card-shadow border border-balance/20 relative overflow-hidden">
            <p class="text-gray-400 text-sm">均衡全能品效池</p>
            <h2 id="balanceCount" class="text-3xl font-bold mt-2 text-balance">0</h2>
            <i class="fa fa-balance-scale absolute right-6 top-6 text-3xl text-balance/30"></i>
        </div>
    </section>

    <div class="flex gap-3 mb-8 border-b border-gray-700 pb-4 flex-wrap">
        <button class="tab-btn active px-6 py-3 rounded-t-lg font-medium text-gray-300" data-type="高收藏带货型">
            <i class="fa fa-cart-plus mr-2"></i>高收藏带货池
        </button>
        <button class="tab-btn px-6 py-3 rounded-t-lg font-medium text-gray-400 hover:text-white" data-type="高讨论声量型">
            <i class="fa fa-bullhorn mr-2"></i>声量话题造势池
        </button>
        <button class="tab-btn px-6 py-3 rounded-t-lg font-medium text-gray-400 hover:text-white" data-type="均衡全能型">
            <i class="fa fa-star-half-o mr-2"></i>均衡全能品效池
        </button>
        <button class="tab-btn px-6 py-3 rounded-t-lg font-medium text-gray-400 hover:text-white" data-type="all">
            <i class="fa fa-th mr-2"></i>全部优质博主
        </button>
    </div>

    <div id="bloggerContainer" class="blogger-grid"></div>
</main>

<footer class="mt-16 py-6 text-center text-gray-500 text-sm border-t border-gray-800">
    <p>操作说明：双击顶部门槛数字修改优质博主判定范围；点击博主类型标签新窗口打开博主详情页</p>
</footer>

<script>
// 全局变量
const rawAllBlogger = {json_str};
let activeType = "高收藏带货型";
let minNote = {DEFAULT_MIN_NOTE_COUNT};
let minInteract = {DEFAULT_MIN_TOTAL_INTERACT};

// DOM缓存
const container = document.getElementById("bloggerContainer");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");
const categorySelect = document.getElementById("categorySelect");
const tabBtns = document.querySelectorAll(".tab-btn");
const modal = document.getElementById("thresholdModal");
const inputMinNote = document.getElementById("inputMinNote");
const inputMinInteract = document.getElementById("inputMinInteract");
const showMinNote = document.getElementById("showMinNote");
const showMinInteract = document.getElementById("showMinInteract");
const cancelBtn = document.getElementById("cancelThreshold");
const saveBtn = document.getElementById("saveThreshold");
const editTextSpans = document.querySelectorAll(".double-click-edit");

// 初始化类别下拉
function initCategoryOption(){{
    const catSet = new Set();
    rawAllBlogger.forEach(i=>catSet.add(i.类别));
    Array.from(catSet).forEach(cat=>{{
        const opt = document.createElement("option");
        opt.value = cat;
        opt.innerText = cat;
        categorySelect.appendChild(opt);
    }})
}}

// 打开弹窗
function openModal(){{
    inputMinNote.value = minNote;
    inputMinInteract.value = minInteract;
    modal.classList.remove("hidden");
}}
// 关闭弹窗
function closeModal(){{
    modal.classList.add("hidden");
}}
// 保存阈值并刷新
function saveNewThreshold(){{
    const newNote = parseInt(inputMinNote.value) || 0;
    const newInteract = parseInt(inputMinInteract.value) || 0;
    minNote = newNote;
    minInteract = newInteract;
    showMinNote.innerText = minNote;
    showMinInteract.innerText = minInteract;
    closeModal();
    renderAll();
}}

// 绑定双击打开弹窗
editTextSpans.forEach(span=>{{
    span.ondblclick = openModal;
}});
cancelBtn.onclick = closeModal;
saveBtn.onclick = saveNewThreshold;
modal.onclick = (e)=>{{if(e.target === modal) closeModal();}}

// 筛选优质博主：动态按当前阈值过滤原始全量数据
function getFilteredQualityBlogger(){{
    return rawAllBlogger.filter(item=>{{
        // 双重门槛
        const passNote = item.笔记数量 >= minNote;
        const passInteract = item.总互动量 >= minInteract;
        if(!passNote || !passInteract) return false;
        // 比值分层
        const cr = item.收藏点赞比;
        const cmr = item.评论点赞比;
        let tagType = "";
        if(cr > 0.3 && cmr < 0.08) tagType = "高收藏带货型";
        else if(cmr > 0.15 && cr < 0.15) tagType = "高讨论声量型";
        else if(cr >=0.15 && cr <=0.25 && cmr >=0.08 && cmr <=0.15) tagType = "均衡全能型";
        else return false;
        item._dynamicTagType = tagType;
        return true;
    }})
}}

// 统计顶部数字
function renderStat(list){{
    let sell=0,talk=0,balance=0;
    list.forEach(item=>{{
        if(item._dynamicTagType === "高收藏带货型") sell++;
        else if(item._dynamicTagType === "高讨论声量型") talk++;
        else balance++;
    }})
    document.getElementById("totalCount").innerText = list.length;
    document.getElementById("sellCount").innerText = sell;
    document.getElementById("talkCount").innerText = talk;
    document.getElementById("balanceCount").innerText = balance;
}}

// 主渲染入口
function renderAll(){{
    let qualityList = getFilteredQualityBlogger();
    const searchKey = searchInput.value.trim().toLowerCase();
    const filterCat = categorySelect.value;
    const sortRule = sortSelect.value;

    // 分类标签筛选
    if(activeType !== "all") qualityList = qualityList.filter(i=>i._dynamicTagType === activeType);
    // 类别筛选
    if(filterCat !== "all_category") qualityList = qualityList.filter(i=>i.类别 === filterCat);
    // 搜索
    if(searchKey) qualityList = qualityList.filter(i=>i.name.toLowerCase().includes(searchKey) || String(i.id).toLowerCase().includes(searchKey));
    // 排序
    qualityList.sort((a,b)=>{{
        switch(sortRule){{
            case "collect_rate_desc": return b.收藏点赞比 - a.收藏点赞比;
            case "collect_rate_asc": return a.收藏点赞比 - b.收藏点赞比;
            case "total_interact_desc": return b.总互动量 - a.总互动量;
            default: return a.总互动量 - b.总互动量;
        }}
    }})

    renderStat(qualityList);
    container.innerHTML = "";
    if(qualityList.length === 0){{
        container.innerHTML = `<div class="col-span-full text-center py-20 text-gray-400 text-lg"><i class="fa fa-folder-open-o text-4xl block mb-4"></i>暂无符合当前门槛的优质博主，可双击顶部数字降低筛选阈值</div>`;
        return;
    }}

    let htmlBuf = "";
    qualityList.forEach(item=>{{
        let borderClass,typeIconHtml,tagColor;
        if(item._dynamicTagType === "高收藏带货型"){{
            borderClass="border-success/40";
            typeIconHtml='<i class="fa fa-cart-plus text-success text-xl"></i>';
            tagColor = "bg-green-600/30 text-success";
        }}else if(item._dynamicTagType === "高讨论声量型"){{
            borderClass="border-discuss/40";
            typeIconHtml='<i class="fa fa-bullhorn text-discuss text-xl"></i>';
            tagColor = "bg-indigo-600/30 text-discuss";
        }}else{{
            borderClass="border-balance/40";
            typeIconHtml='<i class="fa fa-star-half-o text-balance text-xl"></i>';
            tagColor = "bg-sky-600/30 text-balance";
        }}

        let avatarDom = "";
        const avatarUrl = String(item.头像 ?? "");
        if(avatarUrl.startsWith("http")){{
            avatarDom = `<img src="${{avatarUrl}}" loading="lazy" alt="头像" class="avatar-circle" onerror="this.parentElement.innerHTML='<div class=\\'avatar-circle bg-gray-600 flex items-center justify-center text-2xl text-white\\'><i class=\\'fa fa-user\\'></i></div>'">`;
        }}else{{
            avatarDom = `<div class="avatar-circle bg-gray-600 flex items-center justify-center text-2xl text-white"><i class="fa fa-user"></i></div>`;
        }}

        htmlBuf += `
        <div class="glass rounded-xl p-6 card-shadow border ${{borderClass}} card-hover">
            <div class="flex gap-4 items-start mb-4">
                ${{avatarDom}}
                <div class="flex-1">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="text-xl font-bold m-0">${{item.name}}</h3>
                            <p class="text-gray-400 text-sm mt-1 mb-0">博主ID：${{item.id}}</p>
                            <span class="inline-block mt-1 py-1 px-2 rounded bg-orange-600/30 text-category text-xs">
                                <i class="fa fa-tag mr-1"></i>${{item.类别}}
                            </span>
                        </div>
                        ${{typeIconHtml}}
                    </div>
                </div>
            </div>
            <div 
                class="mb-4 py-2 px-3 rounded ${{tagColor}} text-sm inline-block click-tag"
                onclick="window.open('${{item.详情页}}', '_blank')"
                title="点击查看博主完整详情"
            >
                ${{item._dynamicTagType}} <i class="fa fa-external-link ml-1 text-xs"></i>
            </div>
            <div class="space-y-2 text-sm text-gray-300">
                <div class="flex justify-between"><span>总笔记数：</span><span class="font-medium">${{item.笔记数量}} 篇</span></div>
                <div class="flex justify-between"><span>总互动量(赞+藏+评+分)：</span><span class="font-medium text-primary">${{item.总互动量}}</span></div>
                <div class="flex justify-between"><span>收藏/点赞转化比：</span><span class="font-medium text-success">${{item.收藏点赞比}}</span></div>
                <div class="flex justify-between"><span>评论/点赞声量比：</span><span class="font-medium text-discuss">${{item.评论点赞比}}</span></div>
            </div>
            <div class="mt-5 pt-4 border-t border-gray-700/60">
                <p class="text-xs text-gray-400 mb-1">投放建议：</p>
                <p class="text-sm leading-relaxed text-white m-0">${{item.投放建议}}</p>
            </div>
        </div>`;
    }})
    container.innerHTML = htmlBuf;
}}

// 标签切换
tabBtns.forEach(btn=>{{
    btn.onclick = ()=>{{
        tabBtns.forEach(b=>b.classList.remove("active"));
        btn.classList.add("active");
        activeType = btn.dataset.type;
        renderAll();
    }}
}});

// 防抖搜索
let debounceTimer = null;
function debounce(fn,delay=150){{
    return ()=>{{clearTimeout(debounceTimer);debounceTimer=setTimeout(fn,delay);}}
}}
searchInput.oninput = debounce(renderAll);
sortSelect.onchange = renderAll;
categorySelect.onchange = renderAll;

// 初始化
initCategoryOption();
renderAll();
</script>
</body>
</html>'''
    with open("博主投放分析平台.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ 已生成页面：博主投放分析平台.html（支持双击修改优质博主筛选阈值）")

# 自动打开网页
def auto_open_html(file_path):
    absolute_path = os.path.abspath(file_path)
    print(f"\n📂 自动打开网页：{absolute_path}")
    try:
        webbrowser.open("file:///" + absolute_path.replace("\\", "/"))
    except Exception as e:
        print(f"自动打开失败，请手动双击文件：{absolute_path}")

# 程序入口
if __name__ == "__main__":
    print("===== 小红书博主分层分析（支持前端双击修改优质博主阈值） =====")
    print(f"Python默认优质博主判定门槛：笔记≥{DEFAULT_MIN_NOTE_COUNT}、总互动≥{DEFAULT_MIN_TOTAL_INTERACT}")
    print("网页操作：双击顶部门槛数字弹窗修改，实时刷新列表，无需重启程序")
    blogger_full_data = process_blogger_data()
    generate_html(blogger_full_data)
    auto_open_html("博主投放分析平台.html")
    print("\n🎉 输出文件：")
    print("1. 博主分层打分结果.csv 基于Python默认阈值生成固定报表")
    print("2. blogger_data.json 存储全部原始博主数据，前端动态筛选")
    print("3. 博主投放分析平台.html 全部功能集成，双击修改优质博主判断范围")