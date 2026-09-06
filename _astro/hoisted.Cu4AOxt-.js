const f=new Set("的 了 和 与 或 是 在 把 被 也 还 但 而 及 对 为 就 这 那 我 你 他 她 它 我们 他们 之 于 以 来 到 没 有 但 因 与 其 所 各 由".split(/\s+/));function A(a){if(!a)return[];const s=String(a).toLowerCase(),t=[],c=s.match(/[a-z0-9]+/g)||[];t.push(...c.filter(n=>n.length>=2&&!f.has(n)));const e=s.split(/[\s,，。.、；;：:！!？?\(\)\[\]\{\}【】《》·\/\\\n\t\r"'`~@#$%^&*+=|]/g).filter(Boolean);for(const n of e){const i=n.match(/[\u4e00-\u9fff]+/g);if(i)for(const l of i){if(l.length>=2)for(let o=0;o<l.length-1;o++)t.push(l.substr(o,2));if(l.length>=3)for(let o=0;o<l.length-2;o++)t.push(l.substr(o,3))}}return t.filter(n=>!f.has(n))}function k(a){const s=new Map;for(const t of a)s.set(t,(s.get(t)||0)+1);return s}function h(a,s=20){return[...k(A(a)).entries()].sort((c,e)=>e[1]-c[1]).slice(0,s).map(([c,e])=>({w:c,c:e}))}function y(a,s){const t=h(a,25),c=h(s,60),e=new Set(t.map(r=>r.w)),n=new Set(c.map(r=>r.w)),i=[],l=[];t.forEach(({w:r,c:d})=>{n.has(r)?i.push({w:r,c:d}):l.push({w:r,c:d})});let o=0,B=0;return t.forEach(({c:r})=>{const d=r>=3?1.5:1;o+=d}),i.forEach(({c:r})=>{B+=r>=3?1.5:1}),{pct:o?Math.round(B/o*100):0,hit:i,miss:l,jdKw:t,reKw:c,coverage:e.size?Math.round(i.length/e.size*100):0}}const p=document.getElementById("termBody");function w(){p.innerHTML=""}function m(a,s="info",t=60){return new Promise(c=>{setTimeout(()=>{const e=document.createElement("div");e.className="term-line "+s,e.textContent=a,p.appendChild(e),p.scrollTop=p.scrollHeight,c()},t)})}async function v(){const a=document.getElementById("jdText").value.trim(),s=document.getElementById("resumeA").value.trim(),t=document.getElementById("resumeB").value.trim();if(!a||!s||!t){await m("⚠ 输入不完整，需要 JD + 简历 A + 简历 B 三段文本。","warn",0);return}w(),document.getElementById("vsStage").style.display="none",document.getElementById("kwCompare").style.display="none",await m("▶ START 简历×JD 匹配实验 …","info",0),await m(`  JD 字符: ${a.length}  简历A 字符: ${s.length}  简历B 字符: ${t.length}`,"dim",120),await m("  [1/4] 提取 JD 关键词 …","info",200);const c=h(a,25);await m(`  ✓ 提取到 ${c.length} 个关键词（前 10）：${c.slice(0,10).map(o=>o.w+"×"+o.c).join(" / ")}`,"pass",180),await m("  [2/4] 计算 RESUME A …","info",200);const e=y(a,s);await m(`  ✓ A 命中 ${e.hit.length}/${c.length}，覆盖率 ${e.coverage}% 加权得分 ${e.pct}`,"pass",220),await m("  [3/4] 计算 RESUME B …","info",200);const n=y(a,t);await m(`  ✓ B 命中 ${n.hit.length}/${c.length}，覆盖率 ${n.coverage}% 加权得分 ${n.pct}`,"pass",220),await m("  [4/4] 双份差值 …","info",200);const i=e.pct-n.pct;await m(`  ✓ Δ = ${i>0?"+":""}${i} pts（${i>0?"A 更贴合 JD":i<0?"B 更贴合 JD":"两份相同"})`,"pass",180),await m("▶ DONE","info",220),document.getElementById("vsStage").style.display="",E("scoreA",e.pct),E("scoreB",n.pct),document.getElementById("hitA").textContent=e.hit.length,document.getElementById("hitB").textContent=n.hit.length,document.getElementById("covA").textContent=e.coverage,document.getElementById("covB").textContent=n.coverage;const l=document.getElementById("deltaLabel");l.textContent=(i>0?"+":"")+i+" pts",l.style.color=i>0?"var(--pink)":i<0?"var(--purple)":"var(--ink-soft)",document.getElementById("kwCompare").style.display="",u("kwA",e.hit.map(o=>o.w),"pink"),u("kwMissA",e.miss.map(o=>o.w),"miss"),u("kwB",n.hit.map(o=>o.w),"cyan"),u("kwMissB",n.miss.map(o=>o.w),"miss")}function E(a,s){const t=document.getElementById(a),c=performance.now(),e=1100,n=i=>{const l=Math.min(1,(i-c)/e),o=1-Math.pow(1-l,3);t.textContent=Math.round(s*o),l<1?requestAnimationFrame(n):t.textContent=s};requestAnimationFrame(n)}function u(a,s,t){const c=document.getElementById(a);if(c.innerHTML="",s.forEach(e=>{const n=document.createElement("span");n.className="kw-tag "+(t==="miss"?"kw-miss":t==="pink"?"kw-pink":"kw-cyan"),n.textContent=e,c.appendChild(n)}),!s.length){const e=document.createElement("span");e.className="kw-empty",e.textContent="— 无 —",c.appendChild(e)}}const g={jd:`岗位：内容运营实习生

岗位职责：
1. 负责公众号/小红书日常内容运营，包括选题策划、文案撰写、排版与发布；
2. 跟进用户增长指标（DAU、留存、转化），配合活动策划提升用户活跃；
3. 收集整理用户反馈与运营数据，输出周报月报，用数据驱动内容优化；
4. 跨部门协作，与产品、设计、市场协同推进内容项目落地。

任职要求：
- 文案能力强，文字有感染力；
- 熟悉主流社交平台（小红书/抖音/B站）运营玩法；
- 数据敏感，能用数据驱动决策；
- 加分：英语流利、有个人公众号/自媒体运营经验。`,a:`张甜湉 · 内容运营向简历

教育：财务管理硕士在读

经历：
- 校园公众号主笔，年度阅读量 10w+，策划"考研故事"系列内容，单篇最高 1.2w 阅读；
- 小红书账号运营 6 个月，定位"审计实习日记"，粉丝从 0 到 2400，多篇笔记进入同城榜；
- 参与品牌活动策划组，负责文案与现场执行，活动期间用户活跃提升 18%；
- 跨部门协作：与产品/设计/市场联动完成 3 个内容项目，平均周更 4 篇；
- 数据驱动：用 Excel + VBA 自动化处理 3000+ 条用户数据，输出周报。

技能：文案 / 排版 / 公众号 / 小红书 / Excel / 数据分析 / 跨部门协作。`,b:`张甜湉 · 财务审计向简历

教育：中南财经政法大学 · 财务管理硕士在读

经历：
- 安永华明会计师事务所（深圳分所 · IPO 项目）：独立核对全量银行账户流水与《已开立银行结算账户清单》，逐户验证账户完整性并执行大额资金收付双向测试；通过企业征信系统查询企业及关联方信用报告，交叉比对未披露的对外担保与质押；赴多地仓库执行存货监盘与抽盘程序。
- 中审众环会计师事务所（珠海 · 格力电器总部年审）：独立负责 500 余份供应商及客户函证的制作、寄发与追踪，利用企查查复核回函地址修正 20 余处异常；赴格力电器多地仓库独立执行抽盘核对 1000+ 项；完成 10 余册审计工作底稿索引编制。
- 北京大学深圳医院财务部：独立开发 VBA 自动化模型处理 3000+ 条月度绩效数据，将处理时长由 1 周压缩至 20 分钟，效率提升 90%，获科室采纳并演示汇报。
- 武汉光至科技财务部：金蝶系统独立处理 100+ 笔应收应付账款，完成两期月度财务报表编制；500+ 条银行交易逐笔核对。

技能：函证 / 监盘 / 抽盘 / 资金流水核查 / 信用报告与关联方核查 / 金蝶 / VBA / Excel / 财务分析。`};function I(){document.getElementById("jdText").value=g.jd,document.getElementById("resumeA").value=g.a,document.getElementById("resumeB").value=g.b}function C(){document.getElementById("jdText").value="",document.getElementById("resumeA").value="",document.getElementById("resumeB").value="",w(),document.getElementById("termBody").innerHTML='<div class="term-line dim"># 已清空 · 等待 RUN …</div>',document.getElementById("vsStage").style.display="none",document.getElementById("kwCompare").style.display="none"}document.getElementById("runBtn").addEventListener("click",v);document.getElementById("fillSampleBtn").addEventListener("click",I);document.getElementById("clearBtn").addEventListener("click",C);window.addEventListener("DOMContentLoaded",()=>{I(),setTimeout(v,500)});
