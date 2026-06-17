# Lesson Plan V3 — 双入口教学详案生成器

## 技能说明

本技能是对 `lesson-plan-from-images` 和 `teaching-guide-generator-en` 两个 Skill 的整合升级版。支持**双入口输入**，智能识别输入类型并选择对应的输出模式，一键生成符合公司模板格式的小学数学教学详案。

### 双入口模式

| 输入类型 | 触发条件 | 输出模式 | 核心能力 |
|----------|----------|----------|----------|
| **Path A: 教研案 docx** | 用户提供 .docx 文件，含知识目标、动画串讲、例题文本等 | 中英双语详案 (.xlsx) | docx解析 + openpyxl模板填充 + 双语话术生成 |
| **Path B: 例题图片** | 用户提供 PNG/JPG 例题图片（每环节可1张或多张） | 8列中文教案 (.xlsx)，v4粤语详案格式 | 图片分析 + openpyxl从头重建 + 教学话术编写 |

### 与原始 Skill 的关系

- `lesson-plan-from-images`：保留不变，专注图片→教案路径
- `teaching-guide-generator-en`：保留不变，专注 docx→双语详案路径
- **`lesson-planV3`**：整合两者，自动识别输入类型，选择最优输出模式

---

## 输入类型自动识别规则

AI 收到用户请求后，按以下优先级判断走哪个路径：

1. **用户提供了 .docx 文件** → 自动走 Path A（教研案→双语详案）
2. **用户提供了图片文件（PNG/JPG）+ 参考模板 Excel** → 自动走 Path B（图片→教案）
3. **用户只提供了图片 + 明确说要中英双语** → 走 Path A 的话术生成逻辑，但用 Path B 的图片分析能力
4. **用户没有提供文件，只提供基本信息** → 按用户指定模式（默认 Path A 手动录入模式）

---

## 教学详案标准1.0 — 话术格式规范（全局适用）

本技能产出的话术必须遵循 **教学详案标准1.0.pdf** 的格式要求。

### 话术序号与标注标准

每条话术必须标序号（1. 2. 3. 4.），每序号最多包含2个关键提问。五种标准标注格式：

| 标注 | 格式 | 用途 |
|------|------|------|
| 学生回答 | `（学生：xxx）` | 预设学生回答内容 |
| 板书 | `（板书：xxx）` | 板书内容说明 |
| 动作 | `（动作：xxx）` | 教师/学生肢体动作、课件点击操作 |
| 笔记 | `（笔记：xxx）` | 要求学生做笔记的内容 |
| 说明 | `（说明：xxx）` | 其余补充说明（如规律、公式等） |

**示例**：
```
1. 同学们，大家看课件——这个3×3×3的大正方体，它的表面全部染了红色，然后被切成一块一块的小正方体。我们一起来观察一下，哪些小正方体有三个面染了颜色呢？

2. （板书：任务一：三面染色小正方体）

3. 每个角（顶点）上的小正方体，它有几个面露在外面？
（学生：三个面！）

4.（动作：点击课件，高亮顶点处三面染色的小正方体）

5. 三面染色的小正方体共有几个？
（学生：8个！）

6.（说明：无论大正方体是3×3×3、4×4×4还是5×5×5，顶点永远是8个！所以三面染色的小正方体永远是8个！）
```

### 破冰话术规则

破冰内容采用固定结构，**禁止出现当节例题的任何具体知识点、符号或计算规则**：

```
1. 同学们好！欢迎来到今天的数学思维课堂！
（动作：点击课件，展示今日课题）

2. 之前我们学习了xxx的基本特征，有没有同学还记得呀？
（学生：xxx！）

3. 很好！看来大家都记得很清楚。
（说明：此处为固定模式，禁止出现当节例题的任何具体知识点、符号或计算规则）

4. 今天老师带来了一个超酷的新技能——xxx！准备好了吗？Let's go！
```

### 课堂总结结构（P14 区域）

课堂总结的 P14 区域包含三个子区，**顺序不可更改**：

| 子区 | D列标签 | E列内容 |
|------|---------|---------|
| 知识点总结 | `知识点总结` | 互动回顾话术 + 公式小结 |
| 个性化点评 | `个性化点评` | 差异化表扬话术（须结合真实情况使用） |
| 习惯提醒 | `习惯提醒` | 作业布置 + 下节课预告 |

### ⚠️ 公式小结位置规则（重要）

**知识点公式小结必须整合在 P14 的 E44（知识点总结）单元格内，禁止独立成行。**

正确做法 — 公式小结作为 E44 话术的末尾部分：
```
1. 同学们，今天我们一起拆解了xxx的规律！
2. （动作：点击课件，展示思维导图/总结页面）
3. 我们一起回顾一下：
· 三面染色 → 顶点处 → 永远8个！
· 两面染色 → 棱上（去顶点）→ (n-2)×12
· 一面染色 → 面中间（去棱）→ (n-2)²×6

【xxx 小结】
· 三面染色：位于顶点处，永远 = 8个
· 两面染色：位于棱上（不含顶点），个数 = (n-2)×12
· 一面染色：位于面中间（不含棱），个数 = (n-2)²×6
```

---

## Path A: 教研案 docx → 中英双语教学详案

### 触发关键词

"教研案"、"docx"、"详案"、"中英双语"、"bilingual"、"teaching guide"、拖入 .docx 文件

### 输入要求

| 输入 | 说明 | 必须 |
|------|------|------|
| 教研案 docx | 含固定字段的教研案文件 | ✅ |
| 参考模板 xlsx | 中英双语详案模板（可选，默认 s5_v8_96_EN） | 推荐 |

### 教研案 docx 结构解析

每份教研案包含以下**固定字段**（纯文本段落，无表格），按顺序出现：

```
校内对应          → 如"人教版 五上 7单元"或"无（实践拓展）"
知识目标          → 1/2/3条，分项列出（如"1.xxx；2.xxx；3.xxx。"）
技能目标          → 一句话
预习              → 一句话
动画串讲1         → 环节一的故事过渡话术
动画串讲2         → 环节二的故事过渡话术
动画串讲3         → 环节三的故事过渡话术
动画串讲4         → 课堂总结的故事收束
环节一P{x}-1例题  → 第一个例题的完整题目文本
环节二P{x}-1例题  → 第二个例题的完整题目文本
环节三P{x}-1例题  → 第三个例题的完整题目文本
```

### 解析方法

使用 `python-docx` 库解析 docx，提取所有非空段落，然后按关键字段匹配：

```python
from docx import Document

def parse_docx(filepath):
    """解析教研案 docx，提取所有字段"""
    doc = Document(filepath)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    
    fields = {}
    for i, para in enumerate(paragraphs):
        for key in ['校内对应', '知识目标', '技能目标', '预习', 
                     '动画串讲1', '动画串讲2', '动画串讲3', '动画串讲4',
                     '环节一', '环节二', '环节三']:
            if para.startswith(key) or key in para:
                # 提取字段值（去除键名后的内容）
                val = para.replace(key, '', 1).strip().lstrip('：:').strip()
                if not val and i + 1 < len(paragraphs):
                    val = paragraphs[i + 1]
                fields[key] = val
                break
    return fields
```

### 详案模板结构（严格遵守）

生成的详案必须包含以下所有板块，**顺序和格式不可更改**。

#### Excel 行号映射（基于96讲模板）

| 行号 | 内容 | 列号说明 |
|------|------|----------|
| Row 1 | 标题行 `《课程名》  难度等级：X星` | A 列（跨列合并） |
| Row 2 | `s5_v8_{讲次}_EN` | A 列 |
| Row 3 | 校内对应 / Textbook Reference | C列中文, I列英文 |
| Row 4 | 知识目标 / Knowledge Objectives | C列中文, I列英文 |
| Row 5 | 技能目标 / Skill Objectives | C列中文, I列英文 |
| Row 6 | 预习 / Warm-up | C列中文, I列英文 |
| Row 9 | 破冰：一、学习习惯检查 | C列标题, D列留空, I列英文 |
| Row 10 | 破冰：二、破冰活动 | C列话术, I列英文 |
| Row 13 | 动画串讲1 / Story Recap 1 | C列KO标题, D列内容, I列英文 |
| Row 14 | 环节一 例题讲解 | C列KO, D列教学设计, H列图示(清空), I列英文 |
| Row 17 | 环节一 练习题 | D/E/F各一题信息 |
| Row 21 | 动画串讲2 / Story Recap 2 | 同Row 13结构 |
| Row 22 | 环节二 例题讲解 | 同Row 14结构 |
| Row 25 | 环节二 练习题 | D/E/F各一题信息 |
| Row 29 | 动画串讲3 / Story Recap 3 | 同Row 13结构 |
| Row 30 | 环节三 例题讲解 | 同Row 14结构 |
| Row 33 | **检查点** — 需清空模板残留 | |
| Row 34 | 环节三 练习题 | D/E/F各一题信息 |
| Row 38 | 动画串讲4 / Story Recap 4 | 课堂总结区 |
| Row 39 | 知识点总结 / Knowledge Recap | |
| Row 40 | 个性化点评 / Personalized Feedback | 固定文本 |
| Row 41 | 习惯提醒 / Habit Reminder | 固定文本 |
| Row 43 | 知识点总结框 Key Points | C列中文, I列英文 |

### 生成脚本技术规范

#### 核心原则

1. **以 xlsx 为模板**：用 `openpyxl.load_workbook(TEMPLATE)` 加载模板，填充内容后另存，**不要从头新建**
2. **中文用 chr() 编码**：所有中文文本通过 `chr()` Unicode 码点写入，避免编码问题
3. **合并单元格处理**：`put()` 函数需检测 `MergedCell`，找到合并区左上角单元格写入值
4. **不修改模板格式**：只填充文字内容，保留模板所有原始背景颜色、字体、行高、合并单元格

#### put() 函数标准实现

```python
from openpyxl.utils import column_index_from_string
from openpyxl.cell.cell import MergedCell

def put(ws, row, col, value):
    """Write value to cell, handling merged cells."""
    c = ws.cell(row=row, column=col)
    if isinstance(c, MergedCell):
        for mr in ws.merged_cells.ranges:
            s_ = str(mr)
            parts = s_.split(':')
            c1 = column_index_from_string(''.join(filter(str.isalpha, parts[0])))
            r1 = int(''.join(filter(str.isdigit, parts[0])))
            if ':' in s_:
                c2 = column_index_from_string(''.join(filter(str.isalpha, parts[1])))
                r2 = int(''.join(filter(str.isdigit, parts[1])))
            else:
                c2, r2 = c1, r1
            if r1 <= row <= r2 and c1 <= col <= c2:
                ws.cell(row=r1, column=c1, value=value)
                return
    else:
        c.value = value

def s(*codes):
    """Build string from Unicode codepoints"""
    return ''.join(chr(c) for c in codes)
```

#### 脚本生成流程

1. 解析 docx 提取所有字段
2. 加载 xlsx 模板（openpyxl）
3. 清空模板残留（H14/H22/H30 图示列, Row 33 等）
4. 填充课程信息区（Row 1-6）
5. 填充破冰环节（Row 9-10）
6. 填充环节一：动画串讲(Row 13) + 例题(Row 14-16) + 练习(Row 17)
7. 填充环节二：动画串讲(Row 21) + 例题(Row 22-24) + 练习(Row 25)
8. 填充环节三：动画串讲(Row 29) + 例题(Row 30-32) + 练习(Row 34)
9. 填充课堂总结（Row 38-41）
10. 填充知识点总结框（Row 43）
11. 保存输出

### AI 完全自动生成的内容（Path A）

- 破冰互动话术（中英双语）
- 知识目标/技能目标/预习的英文翻译
- 每个环节的知识目标（中英双语完整版）
- 例题讲解完整话术（读题→互动→小结，中英双语）
- 情绪策略选择与表扬话术
- 练习建议及答案
- 课堂总结（知识点回顾 + 个性化点评 + 习惯提醒）
- 知识点总结框（中英双语完整版）

### 英文术语对照

- "小喇叭读题" → "Click the Speaker"
- "板书" → "Board:"
- "情绪策略" → "Engagement Strategy:"
- "教师小结" → "Teacher Summary"
- "表扬话术" → "Praise Script:"

---

## Path B: 例题图片 → 8列中文教案（v4粤语详案格式）

### 触发关键词

"例题图片"、"图片"、"PNG"、"JPG"、"教案"、"lesson plan"、"生成教案"、拖入图片文件

### 输入要求

| 输入 | 说明 | 必须 |
|------|------|------|
| 例题图片（PNG/JPG） | 每个教学环节的例题图片，每环节可为1张或多张 | ✅ |
| 年级 | 如：小学四—五年级 | ✅ |
| 课程时长 | 如：40分钟 | ✅ |

### 核心输出

Excel 教案文件，8列结构（A~H），使用 **openpyxl 从头重建工作簿**（禁止使用 `insert_rows()`）：

| 列 | 内容 | 说明 |
|----|------|------|
| A列 | 页面/区段标签 | 如 P1-P2、P3、课上破冰、环节一、课堂总结 |
| B列 | 时间 | 如 课前3-5min、5-7min、30s |
| C列 | 教学目标/标签 | 知识/能力/情感三维目标；课程信息区段的字段标签 |
| D-G列 | 教学设计与话术演绎（合并单元格） | 核心教学互动内容 |
| H列 | 图示 | 图示备注列 |

### 标准行结构（v4格式，必须严格遵守）

**⚠️ 关键技术规范：openpyxl 从头重建，先写值再 merge_cells，不用 insert_rows()**

| 行号 | 内容 | 合并方式 | 填充色 | 字体 | 行高 |
|------|------|----------|--------|------|------|
| Row 1 | `《课程名》适用年级：XX  课程时长：XX分钟` | A:H 全合并 | `#92D04F`（橙绿） | 微软雅黑 14pt bold | 40 |
| Row 2 | `课程信息` | A:H 全合并 | `#D9E1F4`（浅蓝） | 微软雅黑 14pt bold | 30 |
| Row 3 | 标签`校内对应`(A:B) + 内容(C:H) | A:B / C:H 分别合并 | 无 | 标签12pt bold / 内容14pt left | 120 |
| Row 4 | 标签`知识目标`(A:B) + 内容(C:H) | A:B / C:H 分别合并 | 无 | 同上 | 120 |
| Row 5 | 标签`技能目标`(A:B) + 内容(C:H) | A:B / C:H 分别合并 | 无 | 同上 | 130 |
| Row 6 | 标签`预习`(A:B) + 灰色占位(C:H) | A:B / C:H 分别合并 | 无 | 占位文字14pt 灰色`#808080` | 40 |
| Row 7 | `课上破冰` | A:H 全合并 | `#DFEBF6`（粉蓝） | 微软雅黑 14pt bold | 30 |
| Row 8 | 表头：`页面` / `时间` / `教学设计与话术演绎` / `图示` | A / B / C:G / H | 无 | 微软雅黑 12pt bold | 30 |
| Row 9 | P1-P2 / 课前3-5min / 一、学习习惯检查 | A / B / C:G | 无 | 内容14pt left | 95 |
| Row 10 | （空）/ （空）/ 二、破冰互动话术 | A / B / C:G | 无 | 内容14pt left | 240 |
| Row 11 | `环节一` | A:H 全合并 | `#D9E1F4`（浅蓝） | 微软雅黑 14pt bold | 30 |
| Row 12 | 表头：`页面` / `时间` / `教学目标` / `教学设计与话术演绎` / `图示` | A / B / C / D:G / H | 无 | 微软雅黑 12pt bold | 30 |
| Row 13 | 过渡页 P_/30s / 动画串讲(D:G) | A / B / D:G | 无 | 内容14pt left | 80 |
| Row 14-15 | 环节一例题讲解正文（A:A跨行/B:B跨行/C:C跨行/D:G） | A跨行 / B跨行 / C跨行 / D:G | 无 | 标签12pt / 话术14pt left | 400/155 |
| Row 16-17 | 练习题（D/E/F/G 各列标题+内容） | D/E/F/G 各列独立 | 无 | 标题14pt bold / 内容11pt 宋体 | 20/82 |
| Row 18 | `环节二` | A:H 全合并 | `#D9E1F4`（浅蓝） | 微软雅黑 14pt bold | 30 |
| … | 环节二结构同环节一 | — | — | — | — |
| Row 25 | `环节三` | A:H 全合并 | `#D9E1F4`（浅蓝） | 微软雅黑 14pt bold | 30 |
| … | 环节三结构同环节一 | — | — | — | — |
| 课堂总结 | `课堂总结` | **A:G 合并**（非A:H） | `#DFEBF6`（粉蓝） | 微软雅黑 14pt bold | 30 |
| 总结内容 | 动画串讲/知识回顾/点评/习惯提醒 | C / D:G | 无 | 标签12pt / 话术14pt left | 自适应 |
| 末尾行 | `知识点总结 Key Points Summary` | A:H 全合并 | `#DFEBF6`（粉蓝） | 微软雅黑 14pt bold | 20 |

**精确格式参数（从 v4.xlsx 实测提取）**：

```
字体：微软雅黑（Microsoft YaHei）全局统一
列宽：A=13 / B=15 / C=18 / D=27 / E=27 / F=27 / G=27 / H≈40
边框：thin 四边框（所有有内容的单元格）
话术内容字号：14pt，左对齐，垂直居中，自动换行
标签/表头字号：12pt bold，水平居中，垂直居中
标题行（Row1）：橙绿 #92D04F，14pt bold，行高40
课程信息标题（Row2）：浅蓝 #D9E1F4，14pt bold，行高30
环节标题（环节一/二/三）：浅蓝 #D9E1F4，14pt bold，行高30
破冰/总结/知识点总结标题：粉蓝 #DFEBF6，14pt bold，行高30
普通内容行：无填充
```

### 完整工作流

#### Step 1 — 分析例题图片

**⚠️ 关键规则：每个环节的例题图片数量不固定，可能为1张、2张或多张。同一环节的所有图片须合并理解为一个完整例题，不得拆分成多个环节。**

1. 用 Read 工具读取所有例题图片（逐张读取）
2. 分析每张图片中的数学知识点：
   - 题目的具体要求（是什么类型的题？）
   - 给出了哪些信息（数字、图形、符号、条件）
   - 需要学生完成什么操作
   - 涉及哪些数学概念或规律
3. 将属于同一环节的多张图片合并理解，归纳该环节对应的教学定位（引入/进阶/挑战）

#### Step 2 — 生成课程信息区段内容

在设计教案结构前，先基于例题内容生成以下4项信息：

**校内对应**（必须参考以下三大体系，格式固定）：
```
• 美国（CCSS）：Grade X — [具体标准领域，如 Operations & Algebraic Thinking]
• 新加坡：Primary X — [具体标准]
• 中国香港：小X — [具体标准]
```

**知识目标**：根据例题内容，分点总结学生应掌握的知识（1-3条，以数字编号）

**技能目标**：根据例题内容，分点总结学生应具备的解题能力（1-3条，以数字编号）

**预习**：固定写占位文字（灰色）：`自行补充（简要说明设计意图，如铺垫xx的知识背景、调用学生的xx前经验、激发学习兴趣等）`

#### Step 3 — 设计教案结构

根据例题数量确定模块数量，标准结构为：

```
Row 1：大标题行（课程名称 + 年级 + 时长）          ← 橙绿底
Row 2：课程信息（小标题）                           ← 浅蓝底
Row 3：校内对应（三大体系）
Row 4：知识目标
Row 5：技能目标
Row 6：预习（灰色占位）

课上破冰                                            ← 粉蓝底
├─ 一、学习习惯检查（点名表扬）
└─ 二、破冰互动（固定模式，见下方规则）

环节一（例题1 或 多张图合并理解的例题1）           ← 浅蓝底
├─ 过渡页（30s）
├─ 知识/能力/情感目标（C列）
├─ 分步教学话术（D:G，学生自主读题→教师分步引导→追问→小结）
└─ 练习题（D/E/F/G 各一题）

环节二（例题2）                                     ← 浅蓝底
└─ 同上结构

环节三（例题3）                                     ← 浅蓝底
└─ 同上结构

课堂总结                                            ← 粉蓝底
├─ 动画过渡
├─ P14 知识点总结（含互动回顾 + 公式小结，整合在同一单元格内）
├─ P14 个性化点评（差异化表扬话术）
└─ P14 习惯提醒/作业提醒
```

#### Step 4 — 编写破冰互动话术（固定模式）

**⚠️ 重要：破冰内容统一采用以下固定结构，禁止出现当节例题的任何具体知识点、符号或计算规则。**

```
二、破冰互动：

1. 同学们，上节课我们学习了什么内容呀？有没有同学还记得？
   （鼓励2-3位同学回答，简单互动即可）

2. 很好！看来大家都记得很清楚。那今天老师带来了一节新课，
   课前有没有同学做了预习呢？
   （询问学生是否完成课前预习）

3. 没有预习的同学也不用担心，跟着老师一起探索就好啦！准备好了吗？我们开始！
   （鼓励没有预习的同学）
```

#### Step 5 — 编写分步教学话术（每个环节）

每道例题的讲解遵循以下结构：

每道例题的讲解遵循以下结构：

**一、学生自主读题，教师就题目关键信息进行提问**

- 提问1：题目让我们做什么？有什么特别的要求？
- 提问2：题目给了我们什么信息/条件？
- 提问3-5：针对具体数学规律/逻辑的引导问题（引导学生回答：xxx）

**二、教师引导学生逐步完成解题**

- 逐步追问，引导学生说出判断依据和计算过程
- 最后一问：谁能告诉老师，为什么……？

**三、教师小结（3条核心规律）**

- 总结本环节的核心规律/方法
- 强调学生容易出错的地方

**四、做题回收（4种差异化场景）**

```
表现突出（全对）：XX做题后主动检查了两遍，所以两题都对啦，奖励五颗小星星！
有明显进步：也要表扬XX！还记得上次我们学分数时还有点迷糊，今天你全部自己分对了，每一步都特别清晰！
努力但结果有误：今天最让老师感动的是XX，虽然有的题目没有完成，但是XX一直没有放弃！
做题习惯不好的：我刚才看到有同学因为粗心反复订正了几次，提交之前要记得检查哦！
```

#### Step 6 — 生成 Excel（openpyxl 从头重建）

**⚠️ 技术要求：使用 openpyxl 从头创建工作簿，绝对禁止使用 `insert_rows()` 或 `xlsxwriter`。**

关键代码规范：

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
ws = wb.active

FONT = "Microsoft YaHei"
THIN = Side(style='thin')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

def make_fill(hex_color):
    return PatternFill(fill_type='solid', fgColor=hex_color)

def set_cell(ws, row, col, value, font_size=12, bold=False, h_align='center',
             v_align='center', wrap=True, fill_color=None, font_color=None):
    cell = ws.cell(row=row, column=col)
    cell.value = value
    kw = {'name': FONT, 'size': font_size, 'bold': bold}
    if font_color:
        from openpyxl.styles.colors import Color
        kw['color'] = Color(rgb=font_color)
    cell.font = Font(**kw)
    cell.alignment = Alignment(horizontal=h_align, vertical=v_align, wrap_text=wrap)
    cell.border = BORDER
    if fill_color:
        cell.fill = make_fill(fill_color)

# 设置列宽
ws.column_dimensions['A'].width = 13
ws.column_dimensions['B'].width = 15
ws.column_dimensions['C'].width = 18
ws.column_dimensions['D'].width = 27
ws.column_dimensions['E'].width = 27
ws.column_dimensions['F'].width = 27
ws.column_dimensions['G'].width = 27
ws.column_dimensions['H'].width = 40

# 写值之后再 merge（先写值再合并）
set_cell(ws, 1, 1, "《课程名》...", font_size=14, bold=True, fill_color='FF92D04F')
ws.merge_cells('A1:H1')
ws.row_dimensions[1].height = 40

# 课程信息标题
set_cell(ws, 2, 1, "课程信息", font_size=14, bold=True, fill_color='FFD9E1F4')
ws.merge_cells('A2:H2')
ws.row_dimensions[2].height = 30

# 校内对应（Row3）：A:B 标签，C:H 内容
set_cell(ws, 3, 1, "校内对应", font_size=12, bold=True)
ws.merge_cells('A3:B3')
set_cell(ws, 3, 3, "• 美国（CCSS）：...\n• 新加坡：...\n• 中国香港：...",
         font_size=14, bold=False, h_align='left')
ws.merge_cells('C3:H3')
ws.row_dimensions[3].height = 120

# 预习（Row6）：灰色占位
set_cell(ws, 6, 1, "预习", font_size=12, bold=True)
ws.merge_cells('A6:B6')
set_cell(ws, 6, 3,
         "自行补充（简要说明设计意图，如铺垫xx的知识背景、调用学生的xx前经验、激发学习兴趣等）",
         font_size=14, bold=False, h_align='left', font_color='FF808080')
ws.merge_cells('C6:H6')
ws.row_dimensions[6].height = 40

# 环节标题（课上破冰）
set_cell(ws, 7, 1, "课上破冰", font_size=14, bold=True, fill_color='FFDFEBF6')
ws.merge_cells('A7:H7')
ws.row_dimensions[7].height = 30

# 保存
wb.save(output_path)
```

#### Step 7 — 执行脚本并验证

1. 使用 managed Python 路径运行脚本：
   `C:\Users\Administrator\.workbuddy\binaries\python\envs\default\Scripts\python.exe script.py`
2. 检查生成的 Excel 文件是否存在且大小合理（通常 > 15KB）
3. 确认行数、合并单元格数量与预期一致

---

## 环境与工具

| 项目 | 路径/说明 |
|------|----------|
| Managed Python | `C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe` |
| Venv | `C:\Users\Administrator\.workbuddy\binaries\python\envs\default\` |
| 已安装包 | python-docx, openpyxl, xlsxwriter |
| 模板目录（Path A） | `C:\Users\PC\Desktop\教学详案&教研案\中英双语详案\` |
| 输出目录（默认） | `C:\Users\Administrator\Desktop\教研写作` 或用户指定 |

### 模板文件（Path A，选择最合适的作为基础）

| 文件 | 适用场景 |
|------|----------|
| `s5_v8_96_EN《枝枝的烦恼》教学详案.xlsx` | **推荐**，结构最完整，三环节均有内容 |
| `s5_v8_81_EN《一击即中》教学详案.xlsx` | 备选 |
| `s5_v8_83_EN《没有硝烟的战争》教学详案.xlsx` | 备选 |

---

## ⛔ 常见错误及禁止事项（生成前必读）

以下错误在之前的生成中反复出现，**每次生成时必须逐项检查**：

### Path A 专属

1. **禁止 AI 编造预习内容**：直接从教研案 docx 中提取"预习"字段原文，一字不改
2. **禁止 AI 编造动画串讲故事线**：直接从教研案 docx 中提取动画串讲1~4原文，一字不改
3. **禁止 AI 编造知识目标/技能目标**：直接从教研案 docx 中提取对应字段原文，一字不改
4. **学习习惯检查保持模板原文**：Row 9 col 3 只保留标题，不要改写为一长段文字
5. **C14/C22/C30 知识目标必须拆分 C4 的知识目标**：不能自写新目标
6. **清理模板残留内容**：Row 33 等行必须清空
7. **H 列（图示）先清空**：H14/H22/H30 等图示列全部设为 None
8. **D/E/F 练习题列：一格子一个信息**：拆分为 D/E/F 各一个
9. **禁止修改模板背景颜色**：只填充文字内容

### Path B 专属

1. **禁止使用 xlsxwriter 或 insert_rows()**：必须用 openpyxl 从头重建工作簿，避免合并单元格错位
2. **先写值再 merge_cells**：openpyxl 中必须先调用 `set_cell()` 写入值，再调用 `ws.merge_cells()`，顺序不可颠倒
3. **格式严格按 v4 标准**：使用 v4粤语详案格式，禁止使用旧蓝底白字格式（`#4472C4`）
4. **破冰禁止涉及例题内容**：破冰话术只能用固定模式（回顾+预习询问+鼓励），绝对不得出现当节例题的任何知识点或符号
5. **多图同环节不拆分**：同一环节有2张或以上图片时，合并理解为一个完整例题，不要拆成多个环节
6. **中文编码安全**：Python 脚本用 UTF-8 编码写文件，所有中文字符串直接写（不需要 chr() 编码）
7. **输出路径**：保存到桌面或用户指定目录

### 共同要求

1. **话术要按教学详案标准1.0 标注**：使用 `（学生：）` `（板书：）` `（动作：）` `（笔记：）` `（说明：）` 五种标注，每条标序号
2. **话术要自然、符合课堂节奏**：口语化，适合线上直播课堂
3. **课堂总结的公式小结整合在 P14 E44 内**：知识点公式小结不独立成行，须作为 P14 知识点总结的一部分
4. **英文版要地道**（Path A）：英文版不是中文直译，要符合英语教学表达习惯
5. **情绪策略要与题目匹配**：根据题目特点选择合适的互动策略
6. **时间分配要合理**：全课40分钟，各环节时间之和严格控制在40分钟内
7. **每个环节题目步骤要完整**：必须包含"读题引导→互动操作→教师小结"三步

---

## 文件命名规律

### Path A (教研案输入)
- 输入：`s5_v8_{讲次}_EN教研案.docx`
- 输出：`s5_v8_{讲次}_EN《{课程名}》教学详案.xlsx`

### Path B (图片输入)
- 输出：`{课题名}-{年级}-{时长}-v1.xlsx`

---

## 输出格式

- **Path A**：Excel (.xlsx)，中英双语并列（D-H列中文，I列英文绿底色），含合并单元格、背景颜色、Microsoft YaHei 字体
- **Path B**：Excel (.xlsx)，8列中文教案，v4粤语详案格式（橙绿/浅蓝/粉蓝分色，微软雅黑字体，含合并单元格、课程信息区段）
- 生成后直接可用，无需二次排版
- 生成完毕后询问教师是否需要调整任何环节

---

## 示例触发语

以下说法都会触发本技能：

### Path A
- "帮我生成第97讲详案，教研案在这里"
- "@s5_v8_97_EN教研案.docx 请生成教学详案"
- "按详案模板生成这道题的教学设计"
- "Generate a bilingual lesson plan from this docx"

### Path B
- "这三张例题图片，帮我生成一个40分钟的教案"
- "参考这个模板，生成教案"
- "帮我把这些题目做成教案Excel"
- "数学例题图片生成教案，三年级"

---

## Resources

本 Skill 包含以下可复用资源：

### scripts/
- `generate_lesson_plan.py` — Path B 的 openpyxl 教案生成器脚本框架（v4格式，8列，从头重建）
- `parse_docx.py` — Path A 的 docx 教研案解析脚本（需创建）

### references/
- `template_format.md` — Path B 的 7列教案 Excel 模板格式规范
- `dialogue_templates.md` — 教学话术模板参考（破冰/分步引导/小结/做题回收）

### 外部依赖
- 需要安装 `openpyxl` 和 `python-docx` 用于 Path A 和 Path B
- `xlsxwriter` 不再用于 Path B（已替换为 openpyxl）
