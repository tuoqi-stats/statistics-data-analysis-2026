---
name: github-push
agent_created: true
description: 推送本地内容到 GitHub 远程仓库时使用此 skill。触发场景：用户要求 push/上传/提交/同步本地文件到 GitHub、创建远程仓库并推送、git push 失败（502 / CONNECT tunnel failed / non-fast-forward）、远端引用卡住、git clone 静默失败等。本机环境特点：无 gh CLI、沙箱代理下 github.com 的 git 协议可能 502 但 api.github.com 可用、凭据 token 无 delete_repo 权限。
---

# GitHub Push

## Overview

将本地内容推送到 GitHub 远程仓库。覆盖三条路径：常规 git push、沙箱 502 时用 Git Data API 直接推送、以及仓库初始化（本地无 .git 时）。包含本机环境已知的全部坑与修复方法。

## 环境事实（必须先知道）

- GitHub 账号：**tuoqi-stats**，凭据已存 Windows 凭据管理器。获取 token：`printf "protocol=https\nhost=github.com\n" | git credential fill`
- token scopes 仅 `gist/repo/workflow`，**无 delete_repo**——API 删除仓库会 403，需用户网页手动删除
- 本机未安装 gh CLI，不要尝试 `gh` 命令
- 沙箱代理下 `github.com` 的 git push/clone 可能 502，但 `api.github.com` 的 HTTPS 请求可用
- 用户习惯：代码仓库统一放在 `E:\repos\`

## 工作流决策

1. 本地无 `.git` → 先走「仓库初始化」
2. 有 `.git` 且需要推送 → 先试常规 `git push`
3. push 报 502 / CONNECT tunnel failed → 走「Git Data API 推送」（见 references/api-push.md）
4. push 报 non-fast-forward 但历史应为最新 → 检查「行尾符分叉陷阱」
5. push 后远端状态存疑 → 用 API 查询确认：`curl -s -H "Authorization: Bearer <token>" https://api.github.com/repos/tuoqi-stats/<repo>/commits?per_page=1`

## 路径 A：仓库初始化（本地无 .git）

```bash
cd <项目目录>
git init -b main
git add -A
git commit -m "Initial commit"
git remote add origin https://github.com/tuoqi-stats/<repo>.git
git push -u origin main
```

如远程仓库尚未创建，用 API 创建（用户级仓库，POST /user/repos）：

```bash
curl -s -X POST -H "Authorization: Bearer <token>" \
  https://api.github.com/user/repos \
  -d '{"name":"<repo>","private":true}'
```

## 路径 B：常规推送

```bash
git add -A && git commit -m "<message>"
git push
```

首次推送用 `git push -u origin main`。成功后 `git log --oneline -1` 验证。

## 常见陷阱与修复

### 行尾符分叉陷阱（API 推送后网络恢复）

Git Data API 推送时若直接用工作区文件内容（Windows 下 CRLF），而 git 正常提交存储为 LF（core.autocrlf=true），两者 blob SHA 不同。网络恢复后 `git push` 会被 non-fast-forward 拒绝。

**对策（二选一）：**
- API 推送前先把文件统一转为 LF 再 base64 编码（推荐）
- 网络恢复后 `git push --force` 用本地 LF 版本覆盖远程

### origin/main 跟踪引用卡住

若 `.git/refs/remotes/origin/` 目录不存在，git fetch/update-ref 不生效（引用困在 packed-refs 中）。

**修复：**
```bash
mkdir -p .git/refs/remotes/origin
printf <sha> > .git/refs/remotes/origin/main
```
**注意：修复后不要运行 `git pack-refs --all`**，否则 loose ref 被打包回去，下次 push 后引用再次卡住。

### git clone 静默失败

沙箱中 `git clone` 可能退出码 0 但实际未写出任何文件（ls 看不到目录；重试时报 "already exists and is not an empty directory"，文件系统视图不一致）。

**处理：** cd 到目标父目录再 clone 一次即可成功。完成后必须 `ls` + `git log` 验证，不要只看退出码。

## Resources

### references/api-push.md

沙箱 502 环境下的 GitHub Git Data API 推送完整流程：获取 token → 查询 parent commit → 创建 blob（base64，LF 行尾）→ 构建 tree → 创建 commit → 更新 ref。当常规 `git push` 因网络被拒时，按此文档逐步执行。
