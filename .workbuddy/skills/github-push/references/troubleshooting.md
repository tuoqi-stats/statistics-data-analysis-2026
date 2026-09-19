# git push 报错诊断与修复

本文件供 `github-push` skill 在步骤 1 / 步骤 5 遇到异常时按需查阅。仓库：`tuoqi-stats/statistics-data-analysis-2026`，默认分支 `main`，环境为 Windows + Git Bash（git 2.55）。

## 目录

- [A. 网络与传输层](#a-网络与传输层)
- [B. 推送被拒 / 非快进](#b-推送被拒--非快进)
- [C. 凭据与权限](#c-凭据与权限)
- [D. 仓库状态异常](#d-仓库状态异常)
- [E. 内容与换行符](#e-内容与换行符)
- [F. 推送后的引用同步](#f-推送后的引用同步)
- [G. 回滚与撤销](#g-回滚与撤销)

---

## A. 网络与传输层

### A1. `CONNECT tunnel failed, response 502` / `fatal: unable to access ... Failed to connect to github.com port 443`

**症状**：`git push origin main` 在传输层失败，但 `api.github.com` 可达。

**诊断**：
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://api.github.com   # 期望 200
```

**修复**：改用 Git Data API 兜底推送（见 SKILL.md 步骤 5 兜底方案）：
```bash
python ".workbuddy/skills/github-push/scripts/push_via_api.py" \
  --repo "E:/repos/statistics-data-analysis-2026" --branch main -m "<提交信息>"
```

**若 curl 也不通**：网络完全受限，脚本同样不可用。向用户说明「当前环境无法访问 GitHub，改动已在本地提交，请在有网络的环境执行 `git push origin main`」，不要反复重试。

### A2. push 挂起无输出

`git push` 长时间无输出通常是代理/防火墙静默丢包。加超时观察：
```bash
GIT_HTTP_LOW_SPEED_LIMIT=1000 GIT_HTTP_LOW_SPEED_TIME=20 git push origin main
```
仍失败则走 A1 的 API 路径。

---

## B. 推送被拒 / 非快进

### B1. `! [rejected] main -> main (fetch first)` / `non-fast-forward`

**原因**：远程有新提交，本地落后。

**修复**（保持提交历史线性，不产生无谓 merge 提交）：
```bash
git fetch origin
git pull --rebase origin main
git push origin main
```
出现冲突时**停下**：向用户列出冲突文件（`git status --short` 中的 `UU` 项），说明冲突位置，让用户决定保留哪一版。不要自行选择「ours/theirs」，也不要 `git rebase --skip` 丢弃他人提交。

中止 rebase 回到安全状态：`git rebase --abort`

### B2. `refusing to merge unrelated histories`

**原因**：本地仓库与远程仓库各有独立初始提交，被当成两条无关历史。

**修复**（仅用于首次把本地仓库连到已存在的远程，且确认远程内容可被本地覆盖或合并）：
```bash
git pull origin main --allow-unrelated-histories
```
冲突时按 B1 处理。**必须先向用户确认远程仓库是否为空**——如果远程已有他人内容，`--allow-unrelated-histories` 后遇到冲突会很难处理。

### B3. `src refspec main does not match any`

**原因**：本地还没有任何提交，或当前分支名不是 `main`。

**诊断**：`git log --oneline -1`（报 `does not have any commits yet` 说明无提交）、`git branch --show-current`

**修复**：先完成步骤 3–4 的 add/commit；分支名不符时用 `git push origin HEAD:main` 或先 `git branch -M main`。

---

## C. 凭据与权限

### C1. `Authentication failed` / `could not read Username for 'https://github.com'`

**原因**：凭据过期或被清除。

**诊断**：
```bash
printf 'protocol=https\nhost=github.com\n\n' | git credential fill | sed 's/^password=.*/password=***/'
```
返回 `username=tuoqi-stats` 且有 password 说明凭据正常。

**修复**：请用户在本机重新登录（Git Credential Manager 弹窗，或 `git credential-manager github login`）。**绝不向用户索要 token 明文，也绝不把 token 写进文件或提交信息。**

### C2. `remote: Permission to <owner>/<repo>.git denied` / HTTP 403

**原因**：token 有读权限但无写权限（缺 `repo` / `contents:write` scope），或账号对该仓库无写权限。

**处理**：告知用户需要具备写权限的凭据；不要尝试改用其他账号或绕过权限。

---

## D. 仓库状态异常

### D1. detached HEAD

**诊断**：`git status` 显示 `HEAD detached at ...`。

**修复**：有需要保留的改动时 `git switch -c <新分支名>`，否则 `git switch main` 回到分支。创建新分支这类改变仓库结构的操作需先征得用户同意。

### D2. 未初始化 / 无 remote

**诊断**：`git rev-parse --is-inside-work-tree` 失败，或 `git remote -v` 无输出。

**处理**：本仓库固定 remote 为 `origin → https://github.com/tuoqi-stats/statistics-data-analysis-2026.git`。确认后按需执行：
```bash
git init -b main
git remote add origin https://github.com/tuoqi-stats/statistics-data-analysis-2026.git
```
新增或修改 remote 配置属于结构性变更，**必须先取得用户确认**；`gh` CLI 在本机未安装，不要用它创建仓库。

### D3. 索引中有冲突条目（unmerged）

**诊断**：`git status --short` 出现 `UU` / `AA` / `DD`。

**处理**：不自动选边。列出冲突文件与冲突标记位置，请用户决策后再继续。

---

## E. 内容与换行符

### E1. `warning: LF will be replaced by CRLF the next time Git touches it`

**说明**：Windows 下 `core.autocrlf` 正常行为，**不是错误**，无需修复，也不应为此改配置或加 `.gitattributes`。

**与 API 兜底脚本的关系**：脚本用 `git cat-file blob <sha>` 读取索引中的 blob 内容，取到的已是 git 规范化后的内容，因此换行符处理与 `git push` 完全一致，不会引入额外差异。

### E2. 单文件超过 100 MB

**症状**：GitHub 拒绝接收，或 API 返回 `blob is too large`。

**处理**：
- 确认该文件是否真该入库——数据集、模型权重、`.ipynb` 大输出通常应加入 `.gitignore`
- 确需版本管理则改用 Git LFS，或走 Releases 附件
- API 兜底脚本默认在 50 MB 处中止（`--max-blob-mb` 可调），**不要**为了绕过限制而盲目调大阈值

### E3. 误把敏感文件暂存

**处理**：
```bash
git restore --staged <file>          # 仅移出暂存，保留工作区文件
```
若已提交但未推送：
```bash
git rm --cached <file>               # 从版本库移除，保留本地文件
printf '\n<file>\n' >> .gitignore    # 加入忽略规则（用户确认后）
git commit --amend --no-edit
```
**已推送到远程的凭据必须视为泄露**：提示用户立即到对应平台吊销并轮换该凭据，再用 `git filter-repo` 或平台提供的方式清理历史。

---

## F. 推送后的引用同步

### F1. `origin/main` 跟踪引用卡在旧值

**症状**：`git fetch` 输出显示 `old..new main -> origin/main`，但 `git rev-parse origin/main` 仍是旧 SHA，`git status` 显示 `[ahead N]`。

**根因**：`.git/refs/remotes/origin/` 目录不存在（可能被 gc 清理），git 无法写 loose ref，引用困在 `.git/packed-refs`，`git update-ref` 也不生效。

**修复**：
```bash
mkdir -p .git/refs/remotes/origin
printf '<正确SHA>\n' > .git/refs/remotes/origin/main    # 直接写 loose ref
git rev-parse origin/main                               # 验证已是新值
git pack-refs --all                                     # 整理回 packed-refs
git status -sb                                          # 应显示 ## main...origin/main，无 ahead/behind
```
> 原理：loose ref 优先级高于 packed-refs，手动写文件即可让 git 读到正确值。

`push_via_api.py` 的 `sync_local()` 已内置该修复（先 `update-ref`，失败再写 loose ref，最后 `pack-refs --all`），一般无需手动执行。

### F2. API 推送后本地 HEAD 与远程 SHA 不同

**说明**：API 创建的 commit 与本地 `git commit` 是两个不同对象（parent/tree 相同则内容一致，SHA 不同）。这是预期行为，不是错误。脚本会自动 `git reset --hard <远程SHA>` 对齐，使 `git status` 恢复干净。若要跳过对齐使用 `--no-sync`。

---

## G. 回滚与撤销

以下操作会丢弃内容，执行前**必须**向用户说明影响并取得确认。

| 目的 | 命令 | 风险 |
|------|------|------|
| 撤销最近一次提交，保留改动在暂存区 | `git reset --soft HEAD~1` | 低 |
| 撤销最近一次提交，保留改动在工作区 | `git reset --mixed HEAD~1` | 低 |
| 丢弃某个文件的未暂存改动 | `git restore <file>` | 中：改动不可恢复 |
| 丢弃全部未提交改动 | `git reset --hard` | **高：禁止擅自执行** |
| 撤销已推送的提交（留下反向提交） | `git revert <sha>` | 低，且历史安全 |

**优先选择 `git revert`**：它不重写历史，不影响协作者。只有用户明确要求时才考虑 `push --force`，且必须先确认没有他人基于该分支工作。
