# Git Data API 推送完整流程（502 绕过法）

适用场景：沙箱代理环境下 `git push` 报 502 / CONNECT tunnel failed，但 `api.github.com` 可访问。原理：绕过 git 协议，直接用 REST API 在远端创建 commit 并移动分支引用。

## 前置

- token 获取：`printf "protocol=https\nhost=github.com\n" | git credential fill`，取输出中的 `password=<token>`
- 所有请求头：`Authorization: Bearer <token>`、`Accept: application/vnd.github+json`
- 远端 owner 固定为 `tuoqi-stats`（用户级仓库）

## 步骤

### 1. 获取远端当前分支引用（parent commit）

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/tuoqi-stats/<repo>/git/refs/heads/main
```

记录 `object.sha` 作为 parent。若 409/404（空仓库），无 parent，跳过 parents 字段。

### 2. 为每个文件创建 blob

**行尾符关键点：先统一转为 LF 再 base64**，否则与 git 正常提交（LF）的 blob SHA 不一致，网络恢复后 push 会 non-fast-forward 冲突。

```bash
# 单文件转 LF + base64
CONTENT=$(sed 's/\r$//' <file> | base64 -w 0)
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/tuoqi-stats/<repo>/git/blobs \
  -d "{\"content\":\"$CONTENT\",\"encoding\":\"base64\"}"
```

记录每个文件返回的 `sha`。二进制文件直接 base64，不做 sed。

### 3. 构建 tree

```bash
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/tuoqi-stats/<repo>/git/trees \
  -d '{
    "base_tree": "<parent_commit_tree_sha，可省略>",
    "tree": [
      {"path": "README.md", "mode": "100644", "type": "blob", "sha": "<blob_sha>"},
      {"path": "src/main.py", "mode": "100644", "type": "blob", "sha": "<blob_sha>"}
    ]
  }'
```

记录返回的 tree `sha`。mode：`100644` 普通文件，`100755` 可执行，`040000` 子目录（用 tree sha）。

### 4. 创建 commit

```bash
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/tuoqi-stats/<repo>/git/commits \
  -d '{
    "message": "<commit message>",
    "tree": "<tree_sha>",
    "parents": ["<parent_commit_sha>"]
  }'
```

记录返回的 commit `sha`。

### 5. 移动分支引用（fast-forward 推送）

```bash
curl -s -X PATCH -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/tuoqi-stats/<repo>/git/refs/heads/main \
  -d '{"sha": "<commit_sha>", "force": false}'
```

首次推送空仓库时改用创建引用：

```bash
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/tuoqi-stats/<repo>/git/refs \
  -d '{"ref": "refs/heads/main", "sha": "<commit_sha>"}'
```

### 6. 验证

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/tuoqi-stats/<repo>/commits?per_page=1"
```

## 后续：网络恢复后同步本地

API 推送的历史与本地未推送的提交可能分叉。确认本地历史正确后：

```bash
git push --force
```

用本地 LF 版本统一覆盖远程历史。若 origin/main 跟踪引用卡住，先按 SKILL.md「origin/main 跟踪引用卡住」修复。
