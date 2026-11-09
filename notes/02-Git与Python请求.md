# 02 Git 与 Python 请求

日期：2026-11-09

## 一、本次目标

1. 再完成一次 Git 修改、暂存、提交和推送。
2. 使用 Python `requests` 独立发送 HTTP GET 请求。
3. 查看请求方法、URL、请求头、状态码和响应体。
4. 学习添加查询参数、自定义请求头和超时设置。
5. 理解 Python 请求与浏览器请求的相同点和不同点。

## 二、第二次 Git 提交

在 README.md 中增加了学习记录目录：

```markdown
## 学习记录

1. [01 我的工作台与 HTTP/HTTPS 初步认识](notes/01-我的工作台.md)
```

完成的工作流：

```text
修改 README
    ↓
查看文件差异
    ↓
Stage 暂存
    ↓
Commit 提交到本地仓库
    ↓
Push 推送到 GitHub
    ↓
在 GitHub 页面验证
```

提交前查看差异，可以确认本次到底修改了哪些内容。
Commit 只生成本地版本，Push 才把版本同步到远程仓库。

## 三、第一个 Python HTTP 探针

代码文件：[probe.py](../code/probe.py)

程序访问：

```text
https://www.ctfhub.com/
```

核心请求代码：

```python
response = requests.get(
    url,
    params=params,
    headers=headers,
    timeout=15
)
```

其中：

- `requests.get`：使用 GET 方法。
- `url`：目标地址。
- `params`：URL 查询参数。
- `headers`：自定义请求头。
- `timeout=15`：最多等待 15 秒，避免程序无限等待。
- `response`：服务器返回的响应对象。

## 四、查询参数

代码：

```python
params = {
    "source": "python-learning"
}
```

实际请求 URL：

```text
https://www.ctfhub.com/?source=python-learning
```

说明 `requests` 会把字典形式的参数拼接到 URL 的查询字符串中。

本次请求仍然使用 GET，参数不是 POST 请求体。

服务器返回 200，不代表服务器一定使用了 source 参数。
服务器也可能直接忽略未知参数，因此需要继续观察响应差异才能判断。

## 五、自定义请求头

代码：

```python
headers = {
    "User-Agent": "security-notes-probe/0.1"
}
```

实际请求头：

```text
User-Agent: security-notes-probe/0.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
```

### 1. User-Agent

User-Agent 是客户端自行声明的身份。
本实验中把它改成了学习探针名称。

修改 User-Agent 不会让 Python 真正变成浏览器，
服务器也不能把它当作可靠的身份认证依据。

### 2. Accept-Encoding

表示客户端支持 gzip、deflate 等响应压缩方式。

它说的是数据压缩，不是 UTF-8 等字符编码。

### 3. Accept

`*/*` 表示客户端没有限定响应类型，可以接收任意类型。

### 4. Connection

`keep-alive` 表示希望复用底层网络连接，
不等于保持登录状态。

### 5. 自动补充的请求头

本次只手动设置了 User-Agent，其他请求头由 requests 自动补充。

`response.request.headers` 展示的是 requests 准备好的请求头。
Host 等少数字段可能由更底层网络库补充，
网络中的最终内容可以通过 Burp 进一步观察。

### 6. 敏感请求头

本次没有 Cookie 和 Authorization，
因为脚本没有登录，也没有浏览器中的登录状态。

真实请求中的 Cookie、Authorization 和 Token 可能代表登录状态，
不能直接写入公开笔记或截图。

## 六、响应结果

本次得到：

```text
请求方法：GET
状态码：200
Content-Type：text/html
```

含义：

- GET：本次使用 GET 方法。
- 200：服务器正常返回 HTTP 响应。
- text/html：响应体是网页 HTML，而不是 JSON。

请求 URL 与最终 URL 相同，说明本次没有发生重定向。

## 七、中文乱码与字符编码

第一次输出中，中文出现乱码。

原因是服务器返回的是字节，而 Python 将字节转换为字符串时，
最初没有使用正确的字符编码。

网页 HTML 中存在：

```html
&lt;meta charset=utf-8&gt;
```

说明网页使用 UTF-8。

在读取 response.text 前设置：

```python
response.encoding = "utf-8"
```

中文即可正常显示。

需要区分：

```text
response.content：原始响应字节
response.text：按照字符编码解码后的字符串
```

设置 response.encoding 只影响 Python 的解码方式，
不会修改服务器返回的原始内容。

Accept-Encoding 是压缩方式，response.encoding 是字符编码，
两者不是同一个概念。

## 八、Python 请求与浏览器请求

| 对比项 | Python requests | 浏览器 |
|---|---|---|
| 发送 HTTP 请求 | 可以 | 可以 |
| 设置 URL、方法和请求头 | 可以 | 可以 |
| 接收响应 | 可以 | 可以 |
| 解析并显示 HTML 页面 | 不负责 | 负责 |
| 运行 JavaScript | 不会自动运行 | 会运行 |
| 自动加载页面中的其他资源 | 不会自动完成 | 会自动完成 |

本次 Python 只请求了一个 URL，并打印返回的 HTML 源代码。

浏览器获得 HTML 后，还会继续解析页面、运行 JavaScript，
并加载脚本、样式和图片等资源。

因此，Python 得到 HTML 源代码，不等于得到了浏览器中的完整运行结果。

## 九、五段式复盘

### 1. 现象

第一次 Python 请求成功返回 200 和 HTML，
但响应中的中文出现乱码。

### 2. 假设

请求本身已经成功，乱码可能来自响应字节的解码方式，
而不是服务器请求失败。

### 3. 验证

检查 HTML，发现页面声明 UTF-8。
将 response.encoding 设置为 UTF-8 后重新请求，中文恢复正常。

### 4. 原理

HTTP 响应体在网络中以字节形式传输。
客户端需要采用正确的字符编码，才能把字节转换成正确文本。

请求成功和文本解码正确是两件事：
HTTP 200 不代表客户端一定按照正确方式处理响应。

### 5. 防御与注意事项

- 只请求明确授权的测试目标。
- 请求应设置合理 timeout，避免无限等待。
- 不能仅凭 HTTP 200 判断参数有效或业务成功。
- User-Agent 等客户端请求头可以伪造，服务器不能盲目信任。
- Cookie、Authorization 和 Token 不得写入公开代码或笔记。
- 推送代码前检查是否包含真实密码和内网地址。

## 十、当前形成的核心认识

1. Python 可以不经过浏览器，独立构造并发送 HTTP 请求。
2. URL 查询参数、请求头和请求体是不同位置的数据。
3. requests 会自动补充部分请求头。
4. 响应对象同时包含响应信息以及实际发出的请求信息。
5. HTTP 200 只说明服务器正常响应，不代表业务成功或参数有效。
6. 字符编码处理正确，才能正常显示响应文本。
7. Python requests 不等于完整浏览器，不会自动渲染页面或运行 JavaScript。

## 十一、仍需继续学习的问题

1. 如何让 Python 请求经过 Burp，并与浏览器请求逐项比较？
2. POST 请求体应该如何用 Python 构造？
3. 重定向发生时，response.history 会记录什么？
4. Cookie 和 Session 如何在多次 Python 请求之间保持？

## 十二、下一步

1. 将 probe.py 和本篇笔记一起提交到 GitHub。
2. 学习使用 Python 构造 POST 请求。
3. 进一步比较 GET 查询参数与 POST 请求体。