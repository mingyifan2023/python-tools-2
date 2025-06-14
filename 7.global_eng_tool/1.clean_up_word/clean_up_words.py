#! -*- coding:utf-8 -*-
import re
import os
import openpyxl  # 用于处理Excel文件


def clean_and_extract_words(file_path):
    """
    读取文本文件，清洗并提取所有非数字的唯一英文单词
    :param file_path: 文本文件路径
    :return: 去重后的单词列表
    """
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则表达式分割时间戳和语句
    pattern = r'\n\d+:\d+\n'
    segments = re.split(pattern, content)

    # 提取所有非数字单词
    all_words = []
    for seg in segments:
        # 移除首尾空白
        seg = seg.strip()
        if not seg:
            continue

        # 替换特殊空格和换行符
        seg = seg.replace('\u200b', '')  # 零宽空格
        seg = seg.replace('\n', ' ')  # 换行符替换为空格

        # 合并多余空格
        seg = re.sub(r'\s+', ' ', seg)

        # 移除标点符号
        seg = re.sub(r'[^\w\s]', '', seg)

        # 分割单词
        words = seg.split()

        # 筛选非数字的英文单词
        for word in words:
            # 检查是否是纯数字
            if word.isdigit():
                continue

            # 检查是否包含英文字母
            if re.search(r'[a-zA-Z]', word):
                all_words.append(word)

    # 去重并保持顺序
    unique_words = []
    for word in all_words:
        # 转换为小写进行比较，但保留原始大小写形式
        lower_word = word.lower()
        if lower_word not in [w.lower() for w in unique_words]:
            unique_words.append(word)

    return unique_words


def write_words_to_excel(words, output_file):
    """
    将单词列表写入Excel文件，每行一个单词
    :param words: 单词列表
    :param output_file: 输出Excel文件路径
    """
    # 创建工作簿和工作表
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "单词列表"

    # 设置列宽
    ws.column_dimensions['A'].width = 10  # 序号列
    ws.column_dimensions['B'].width = 30  # 单词列

    # 写入标题行
    ws.append(['序号', '单词'])

    # 设置标题行样式
    header_row = ws[1]
    for cell in header_row:
        cell.font = openpyxl.styles.Font(bold=True)
        cell.alignment = openpyxl.styles.Alignment(horizontal='center')

    # 写入每个单词
    for i, word in enumerate(words, 1):
        ws.append([word])

    # 保存工作簿
    wb.save(output_file)
    print(f"成功写入Excel文件: {output_file}，共 {len(words)} 个单词")


if __name__ == '__main__':
    # 输入和输出文件路径
    input_txt = 'd.txt'  # 替换为你的输入文件路径
    output_excel = 'words.xlsx'  # 输出Excel文件路径

    # 处理文本并写入Excel
    words = clean_and_extract_words(input_txt)

    print(f"处理完成，共提取 {len(words)} 个非数字的唯一英文单词:")
    for i, w in enumerate(words[:10], 1):  # 打印前10个单词作为示例
        print(f"{i}. {w}")
    if len(words) > 10:
        print(f"... 以及 {len(words) - 10} 个更多单词")

    write_words_to_excel(words, output_excel)
