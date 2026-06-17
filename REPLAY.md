# REPLAY.md — Lesson Plan V3 复核回放记录

本文件记录本技能的触发方式、输入要求、输出格式和复核步骤，供团队内部复用和审查。

---

## 技能触发方式

在 WorkBuddy 对话中输入以下任一触发语，即可触发本技能：

### Path A（教研案 docx → 中英双语详案）

- "帮我生成第97讲详案，教研案在这里"
- "@s5_v8_97_EN教研案.docx 请生成教学详案"
- "按详案模板生成这道题的教学设计"
- "Generate a bilingual lesson plan from this docx"

### Path B（例题图片 → 8列中文教案）

- "这三张例题图片，帮我生成一个40分钟的教案"
- "参考这个模板，生成教案"
- "帮我把这些题目做成教案Excel"
- "数学例题图片生成教案，三年级"

---

## 输入格式要求

### Path A 输入

| 项目 | 要求 |
|------|------|
| 文件格式 | `.docx` 教研案 Word 文档 |
| 必要内容 | 知识目标、动画串讲脚本、例题文本、小结话术 |
| 可选内容 | 冰壶环节设计、拓展题说明 |
| 提交方式 | 在 WorkBuddy 对话中 @ 上传文件 |

### Path B 输入

| 项目 | 要求 |
|------|------|
| 文件格式 | `.png` / `.jpg` 例题图片（每环节1张或多张） |
| 必要文件 | 参考模板 Excel（含课程信息格式） |
| 提交方式 | 在 WorkBuddy 对话中 @ 上传图片 + 模板 |

---

## 输出格式说明

### Path A 输出（中英双语详案）

- **文件格式**：`.xlsx`（Excel 工作簿）
- **Sheet1**：课程信息（4行标准：课题/年级/时长/知识目标/能力目标/情感目标/课程预告）
- **Sheet2**：课中详案（D-H列中文话术，I列英文话术绿底色，含合并单元格和格式颜色）
- **格式规范**：微软雅黑字体，中文话术黑色，英文话术绿色底色 `#C6EfCe`

### Path B 输出（v4 粤语详案格式）

- **文件格式**：`.xlsx`（Excel 工作簿）
- **Sheet 结构**：8列（A环节/B时间/C角色/D话术/E类型/F图片/G备注/H时间戳）
- **分色格式**：橙绿/浅蓝/粉蓝三色分环节，微软雅黑字体，含合并单元格
- **话术格式**：数字编号无中括号，学生话语放 `（）` 内，不用 `师：` 前缀

---

## 复核回放步骤（Owner Local Replay）

由于本技能为 WorkBuddy Skill，运行依赖于 WorkBuddy 对话环境，无法在本地命令行直接 replay。

### 推荐复核方式

1. 在 WorkBuddy 中触发技能（使用 Path A 或 Path B 触发语）
2. 提供一个最小示例输入（见 `samples/input/`）
3. 检查输出 xlsx 是否符合格式规范（见 `samples/output/` 的说明）
4. 验证话术序号、标注格式、中英并列格式是否正确

### 示例输入

- `samples/input/example_research_doc.md` — 示例教研案结构（Markdown，可转为 docx）
- `samples/input/example_problem_images.md` — 示例例题图片说明

### 示例输出

- `samples/output/format_spec.md` — 输出 xlsx 格式详细说明
- （实际 xlsx 示例因依赖 WorkBuddy 运行环境，暂未放入本仓库；owner 本地可生成后脱敏上传）

---

## 依赖环境

| 依赖 | 用途 | 安装方式 |
|------|------|----------|
| `openpyxl` | Path A/B 的 xlsx 生成和模板填充 | `pip install openpyxl` |
| `python-docx` | Path A 的 docx 教研案解析 | `pip install python-docx` |
| WorkBuddy | 技能运行环境（AI 对话） | 已安装 WorkBuddy 桌面端 |

---

## 已知问题 / 待改进

- `scripts/generate_lesson_plan.py` 当前使用 `xlsxwriter`，但 SKILL.md 要求 Path B 使用 `openpyxl`（v4格式）。下次更新时统一。
- `scripts/parse_docx.py` 尚未创建（Path A 的 docx 解析脚本框架待补充）。
- 示例输出 xlsx 需在 WorkBuddy 环境中运行技能后生成，暂无法在本地直接 replay。

---

## 证据标签

- `owner_local_replay`: pending（需在 WorkBuddy 环境中完成）
- `safe_sample_needed`: 是（需补充 samples/input 和 samples/output）
- `package_readiness_score`: 65（有限 replay，需补 P0 样例）

---

> 最后更新：2026-06-17
