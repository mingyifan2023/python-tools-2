你可以修改 Python 脚本，以便通过命令行传入 HTML 文件名。以下是更新后的 server.py，可以接受 HTML 文件名作为参数。
更新的 server.py

python

import http.server
import socketserver
import os
import sys

# 检查是否提供了文件名作为参数
if len(sys.argv) != 2:
    print("用法: python server.py <html文件名>")
    sys.exit(1)

html_file = sys.argv[1]

# 确保文件存在
if not os.path.isfile(html_file):
    print(f"错误: 文件 '{html_file}' 不存在.")
    sys.exit(1)

PORT = 8000

# 设置请求处理程序
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 如果请求的是根目录，则返回指定的 HTML 文件
        if self.path == '/':
            self.path = html_file
        return super().do_GET()

with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
    print(f"Serving at port {PORT}, 访问: http://localhost:{PORT}/")
    print(f"默认HTML文件: {html_file}")
    # 启动服务器
    httpd.serve_forever()

使用方式

    确保你的 server.py 和想要访问的 HTML 文件（例如 index.html）在同一目录下。

    在终端或命令提示符中，导航到该目录。

    运行以下命令，并提供 HTML 文件名作为参数：

    bash

python server.py index.html

打开浏览器，输入 http://localhost:8000/，就能访问你提供的 HTML 文件了。
