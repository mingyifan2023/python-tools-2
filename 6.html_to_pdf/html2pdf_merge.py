# import os
# import re
# from PyPDF2 import PdfReader, PdfMerger
# from datetime import datetime

# # 获取所有pdf文件列表
# pdf_files = [file for file in os.listdir('.') if file.endswith('.pdf')]


# #  自己整理一个顺序即可

# # 将所有pdf文件合并为一个大的pdf文件
# merger = PdfMerger()
# for pdf_file in pdf_files:
#     merger.append(pdf_file)

# merged_pdf_filename = 'merged_output.pdf'
# merger.write(merged_pdf_filename)
# merger.close()

# print(f"All PDF files are merged into {merged_pdf_filename}")

import os
import re
from PyPDF2 import PdfMerger

# 按照文件夹中的pdf文件名 从 0 到最大进行合并

def extract_number_from_filename(filename):
    """从文件名中提取数字并返回作为整数"""
    match = re.search(r'(\d+)', filename)
    return int(match.group(0)) if match else float('inf')  # 如果没有找到数字，则返回无穷大，确保它排到最后

# 获取所有 pdf 文件列表
pdf_folder = '.'  # 替换为您的目标文件夹路径
pdf_files = [file for file in os.listdir(pdf_folder) if file.endswith('.pdf')]

# 按照文件名中的数字进行排序
pdf_files.sort(key=extract_number_from_filename)

# 将所有 pdf 文件合并为一个大的 pdf 文件
merger = PdfMerger()
for pdf_file in pdf_files:
    merger.append(os.path.join(pdf_folder, pdf_file))

merged_pdf_filename = os.path.join(pdf_folder, 'merged_output.pdf')
merger.write(merged_pdf_filename)
merger.close()

print(f"All PDF files are merged into {merged_pdf_filename}")
