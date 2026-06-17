# Lesson Plan V3 — 双入口教学详案生成器

## 一句话说明

整合 `lesson-plan-from-images` 和 `teaching-guide-generator-en` 双入口输入，自动生成符合公司模板的小学数学中英双语教学详案。

## 适用场景

- **Path A**：提供教研案 docx → 生成中英双语详案 (.xlsx)
- **Path B**：提供例题图片 → 生成 8 列中文教案 (.xlsx, v4 粤语详案格式)

## 使用方法

### Path A (教研案)
```
@skill:lesson-planV3 请根据这份教研案生成教学详案
（提供 .docx 教研案文件 + 参考模板 xlsx）
```

### Path B (例题图片)
```
@skill:lesson-planV3 这些例题图片，请生成40分钟教案
（提供 PNG/JPG 例题图片 + 年级信息 + 课程时长）
```

## 核心能力

- 智能识别输入类型（docx / 图片）
- 严格遵循教学详案标准 1.0 话术格式
- 支持破冰、分步教学、做题回收、课堂总结完整流程
- 中英双语自动翻译（Path A）
- openpyxl 标准模板填充 / 从头重建

## 依赖

- Python 3.10+
- openpyxl
- python-docx

## 作者

杨童 — 豌豆思维海外教研团队

## 版本

1.0.0 (2026-06-17)
