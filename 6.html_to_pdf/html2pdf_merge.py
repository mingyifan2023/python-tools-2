import os
import re
from PyPDF2 import PdfReader, PdfMerger
from datetime import datetime

# 获取所有pdf文件列表
pdf_files = [file for file in os.listdir('.') if file.endswith('.pdf')]


#  自己整理一个顺序即可

# 将所有pdf文件合并为一个大的pdf文件
merger = PdfMerger()
for pdf_file in pdf_files:
    merger.append(pdf_file)

merged_pdf_filename = 'merged_output.pdf'
merger.write(merged_pdf_filename)
merger.close()

print(f"All PDF files are merged into {merged_pdf_filename}")
