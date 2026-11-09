import requests

url = "https://www.ctfhub.com/"

params = {
    "source": "python-learning"
}

headers = {
    "User-Agent": "security-notes-probe/0.1"
}

response = requests.get(
    url,
    params=params,
    headers=headers,
    timeout=15
)

# 网页使用 UTF-8，避免中文乱码
response.encoding = "utf-8"

print("请求方法：", response.request.method)
print("请求 URL：", response.request.url)
print("最终 URL：", response.url)
print("请求头 User-Agent：", response.request.headers.get("User-Agent"))
print("状态码：", response.status_code)
print("Content-Type：", response.headers.get("Content-Type"))

print("\n响应体前 300 个字符：")
print(response.text[:300])
print("\n实际发送的全部请求头：")
for name, value in response.request.headers.items():
    print(f"{name}: {value}")