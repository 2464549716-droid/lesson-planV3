# -*- coding: utf-8 -*-
"""
教研案 docx 解析工具
用法：python parse_docx.py <教研案.docx>
输出：打印所有提取到的字段
"""
import sys
from docx import Document


def parse_docx(filepath):
    """
    解析教研案 docx，提取所有字段
    
    返回 dict，key 为字段名，value 为字段内容
    
    支持的字段：
    - 校内对应
    - 知识目标
    - 技能目标
    - 预习
    - 动画串讲1 / 动画串讲2 / 动画串讲3 / 动画串讲4
    - 环节一P{x}-1例题 / 环节二P{x}-1例题 / 环节三P{x}-1例题
    """
    doc = Document(filepath)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    
    fields = {}
    
    # 定义需要匹配的字段键名
    field_keys = [
        '\u6821\u5185\u5bf9\u5e94',      # 校内对应
        '\u77e5\u8bc6\u76ee\u6807',      # 知识目标
        '\u6280\u80fd\u76ee\u6807',      # 技能目标
        '\u9884\u4e60',                  # 预习
        '\u52a8\u753b\u4e32\u8bb21',     # 动画串讲1
        '\u52a8\u753b\u4e32\u8bb22',     # 动画串讲2
        '\u52a8\u753b\u4e32\u8bb23',     # 动画串讲3
        '\u52a8\u753b\u4e32\u8bb24',     # 动画串讲4
        '\u73af\u8282\u4e00',            # 环节一
        '\u73af\u8282\u4e8c',            # 环节二
        '\u73af\u8282\u4e09',            # 环节三
    ]
    
    for i, para in enumerate(paragraphs):
        for key in field_keys:
            if para.startswith(key):
                # 提取字段值（去除键名和冒号）
                val = para
                # 尝试去除键名
                if key in para:
                    val = para.split(key, 1)[1] if len(para.split(key, 1)) > 1 else ''
                    val = val.lstrip('\uff1a:').strip()
                
                # 如果当前行没有值，尝试取下一行
                if not val and i + 1 < len(paragraphs):
                    val = paragraphs[i + 1]
                
                fields[key] = val
                break
    
    return fields


def print_fields(fields):
    """格式化打印提取的字段"""
    print('=' * 60)
    print('\u6559\u7814\u6848\u5b57\u6bb5\u89e3\u6790\u7ed3\u679c')  # 教研案字段解析结果
    print('=' * 60)
    
    key_labels = {
        '\u6821\u5185\u5bf9\u5e94': '\u6821\u5185\u5bf9\u5e94',
        '\u77e5\u8bc6\u76ee\u6807': '\u77e5\u8bc6\u76ee\u6807',
        '\u6280\u80fd\u76ee\u6807': '\u6280\u80fd\u76ee\u6807',
        '\u9884\u4e60': '\u9884\u4e60',
        '\u52a8\u753b\u4e32\u8bb21': '\u52a8\u753b\u4e32\u8bb21',
        '\u52a8\u753b\u4e32\u8bb22': '\u52a8\u753b\u4e32\u8bb22',
        '\u52a8\u753b\u4e32\u8bb23': '\u52a8\u753b\u4e32\u8bb23',
        '\u52a8\u753b\u4e32\u8bb24': '\u52a8\u753b\u4e32\u8bb24',
        '\u73af\u8282\u4e00': '\u73af\u8282\u4e00',
        '\u73af\u8282\u4e8c': '\u73af\u8282\u4e8c',
        '\u73af\u8282\u4e09': '\u73af\u8282\u4e09',
    }
    
    for key, label in key_labels.items():
        val = fields.get(key, '\uff08\u672a\u627e\u5230\uff09')  # （未找到）
        print(f'\n[{label}]')
        print(val)
    
    print('\n' + '=' * 60)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('\u7528\u6cd5: python parse_docx.py <\u6559\u7814\u6848.docx>')
        sys.exit(1)
    
    filepath = sys.argv[1]
    fields = parse_docx(filepath)
    print_fields(fields)
