---
name: github-push
description: 把本地新增或修改的内容提交并推送到 GitHub 远程仓库（origin）的完整工作流。当用户提出「推送到 GitHub / 同步到远程 / 提交并推送 / push 一下 / 把这次改动传上去」，或完成文件生成后需要同步到远程仓库时使用。覆盖提交前敏感信息审查、中文提交信息自动生成、push 被拒与非快进的处理，以及沙箱网络下 git push 报 502 / CONNECT tunnel failed 时改用 GitHub Git Data API 推送的兜底方案。
agent_created: true
---

# github-push — 把本地内容推送到 GitHub 远程仓库

把工作区的新增/修改内容，经安全审查后提交并推送到远程仓库；失败时按错误类型选择修复或 API 兜底路径；最后验证远程状态并向用户汇报。

## 本仓库固定信息

| 项 | 值 |
|------|------|
| 仓库根目录 | `E:/repos/statistics-data-analysis-2026` |
| remote | `origin` → `https://github.com/tuoqi-stats/statistics-data-analysis-2026.git` |
| 默认分支 | `main` |
| 提交信息 | 简体中文，按本次改动内容自动生成（格式见步骤 4） |
| 凭据 | Windows 凭据管理器；`git credential fill` 可取到（username=`tuoqi-stats`）。`gh` CLI **未安装**，不要依赖它 |
| `.workbuddy/` | **已被 git 跟踪**：`memory/*.md`、`skills/**/SKILL.md` 属于项目共享产物，需随代码一起提交 |

## 何时使用

- 用户说「推送到 GitHub」「同步到远程」「提交并推送」「push 一下」「把改动传上去」
- 刚生成/修改了本地文件（学习资料、笔记、代码、项目 skill、memory 等），需要同步到远程仓库
- 用户只要求「提交」不要求推送时，执行步骤 1–4，跳过步骤 5

## 标准流程

### 步骤 1：核对仓库状态

```bash
cd "E:/repos/statistics-data-analysis-2026"
git rev-parse --is-inside-work-tree      # 必须在工作区内
git remote -v                            # 确认 origin 存在
git status --short --branch              # 看改动与领先/落后情况
git log --oneline -3
```

异常分支：未初始化 git、缺 remote、处于 detached HEAD、本地落后远程 —— 见 `references/troubleshooting.md` 对应小节后再继续。

### 步骤 2：提交前安全审查（不可跳过）

先列出本次将要提交的文件：

```bash
git status --short
```

逐条确认，命中任一条即**停止提交**：

- **疑似凭据文件名**：`.env*`、`*credential*`、`*secret*`、`*.pem`、`*token*`、`id_rsa*`、`*.key`
- **凭据内容**：对新增文件用 Grep 抽查，模式 `(api[_-]?key|secret|token|password|passwd)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}`
- **临时产物**：`__pycache__/`、`.ipynb_checkpoints/`、`node_modules/`、`.DS_Store`、`*.log`、`*.tmp`
- **大文件**：单文件 > 50 MB（GitHub 单文件上限 100 MB）
- **隐私信息**：日志或导出文件中的真实姓名、手机号、邮箱、个人目录绝对路径

**发现疑似凭据时**：不要提交。用 Read 打开该文件定位具体行号，向用户指出「文件 + 行号 + 命中的模式」，等用户确认是误报还是需要移出提交。绝不在汇报中回显密钥明文。

`.workbuddy/memory/` 与 `.workbuddy/skills/` 是本仓库的共享产物，正常提交；但要确认其中没有粘贴进对话里的密钥或 token。

### 步骤 3：暂存

```bash
git add -A                    # 默认：提交全部改动
git add <path> [<path>...]    # 只提交部分内容时，用显式路径
git status --short            # 复核：确认暂存区就是预期内容，无多余文件
```

### 步骤 4：生成中文提交信息并提交

按本次改动的实际内容生成，格式固定为「类型：主题」：

| 改动性质 | 格式 | 示例 |
|------|------|------|
| 新增文件/资料 | `新增：<主题> <文件类型>` | `新增：RAG 学习资料` |
| 修改已有内容 | `更新：<主题>（<变更要点>）` | `更新：README 仓库结构说明` |
| 修正错误 | `修复：<问题描述>` | `修复：agent.md 中链接失效` |
| 结构调整 | `重构：<范围>` | `重构：learning-materials 目录归类` |
| 配置/流程 | `配置：<内容>` | `配置：新增 github-push 项目 skill` |

多类改动时，首行写概括，空行后用 `- ` 列出 2–5 条要点：

```bash
git commit -m "新增：统计学习资料两篇

- 新增 t-test.md、anova.md
- 更新 README 索引"
```

无任何改动可提交时（`git status --short` 为空且无未推送提交）：直接告知用户「工作区无改动，无需提交」，**不要**制造空提交。若本地已有未推送的提交，跳过步骤 3–4，直接进入步骤 5。

### 步骤 5：推送

```bash
git push origin main
```

成功则进入步骤 6。失败时**不要反复重试同一条命令**，按下表分流：

| 报错关键字 | 处理方式 |
|------|------|
| `CONNECT tunnel failed`、`502`、`unable to access`、`Failed to connect to github.com` | 沙箱网络受限但 API 可达 → 改用下方「步骤 5 兜底方案」 |
| `rejected`、`non-fast-forward`、`fetch first` | `git pull --rebase origin main` 后重新 push；出现冲突则停下，向用户说明冲突文件并请其决策 |
| `Authentication failed`、`could not read Username`、`403` | 凭据失效或权限不足 → 请用户在本地重新登录 git 凭据；**不要**向用户索要 token 明文 |
| `refusing to merge unrelated histories` | 首次把本地仓库连到已有远程 → 见 `references/troubleshooting.md` |
| `src refspec main does not match any` | 尚无提交或分支名不是 main → 先确认 `git log` 与 `git branch` |

### 步骤 5 兜底方案：GitHub Git Data API 推送

适用条件：`git push` 因网络受限失败，但 `api.github.com` 可达。命令：

```bash
python ".workbuddy/skills/github-push/scripts/push_via_api.py" \
  --repo "E:/repos/statistics-data-analysis-2026" \
  --branch main \
  -m "<步骤 4 的提交信息>"
```

若当前工作目录不是仓库根目录，把脚本路径换成绝对路径 `E:/repos/statistics-data-analysis-2026/.workbuddy/skills/github-push/scripts/push_via_api.py`。

参数：`--dry-run` 只打印推送计划不写入；`--no-sync` 跳过本地同步；`--max-blob-mb N` 调整大文件阈值（默认 50）；`--remote` 指定 remote（默认 origin）。

脚本执行的等价动作：读取 git 索引 → 取远程 HEAD 与 base tree → 逐文件对比算出新增/修改/删除 → 逐个建 blob → 建 tree（含删除项）→ 基于远程 HEAD 建 commit → 更新分支 ref（`force=false`，保证快进）→ 对齐本地 HEAD 与远程跟踪引用 → 调 API 验证。

- 脚本报「远程分支已前进」：说明远程有新提交，重新运行一次即可（会基于新 HEAD 重建）。
- API 推送生成的 commit SHA 与本地 git commit 不同（对象不同、内容一致），脚本会自动把本地 HEAD 对齐到远程 SHA，属预期行为。
- 脚本打印的 token 来源、文件清单、SHA 需如实转述给用户。

### 步骤 6：验证并汇报

```bash
git status --short --branch                  # 应显示与 origin/main 同步，无 ahead/behind
git log --oneline -1                         # 本地最新提交
git ls-remote origin -h refs/heads/main      # 远程 SHA 应与本地 HEAD 一致
```

汇报用简洁要点，包含：

1. 仓库与分支（`tuoqi-stats/statistics-data-analysis-2026` / `main`）
2. 提交信息
3. 本次提交的文件数，并列出 1–3 个关键文件路径
4. 本地 HEAD 与远程 SHA
5. 使用的方式：`git push` 或「API 兜底推送」
6. 遗留问题（如有：未处理的冲突、待用户确认的疑似凭据等）

## 禁止事项

- 不使用 `git push --force` / `-f`（除非用户明确要求并二次确认）
- 不用 `git reset --hard` / `git checkout -- ` 丢弃用户未提交的改动
- 不把 token、密码、私钥写进任何文件、提交信息或命令输出
- 不修改 `.gitignore` 去放行本该忽略的敏感文件
- 不在用户未明确授权时新建远程仓库、改动或新增 remote 配置
- 不代替用户做冲突决策：遇到无法自动解决的合并冲突，停在报告环节

## 参考文件

- `references/troubleshooting.md`：各类 git 报错的诊断与修复（含 `origin/<branch>` 跟踪引用卡在旧值、CRLF 警告、大文件、凭据失效、误提交回滚、首次推送）
