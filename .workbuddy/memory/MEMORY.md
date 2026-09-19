# 项目长期记忆 — statistics-data-analysis-2026

## 项目定位
- 统计与数据分析课程学习笔记与代码仓库（GitHub: tuoqi-stats/statistics-data-analysis-2026）

## 约定
- `learning-materials/`：AI 概念学习资料目录，由项目 skill `concept-material-generator`（.workbuddy/skills/concept-material-generator/）生成；文档固定五部分结构；文件名小写 kebab-case（英文/缩写优先，无通用英文用拼音）
- `.gitignore` 已含密钥 / API key 屏蔽规则（追加于 Python 模板之后），新增涉及凭据的文件时注意命名匹配
- `.workbuddy/` 下的 `memory/*.md` 与 `skills/**/SKILL.md` **是 git 跟踪的**项目共享产物，需随代码提交，不要当作本地缓存忽略
- 提交与推送统一走项目 skill `github-push`（`.workbuddy/skills/github-push/`）：中文提交信息、提交前敏感信息审查、push 失败按报错分流
- 环境事实：`gh` CLI 未安装（勿依赖）；git 凭据存于 Windows 凭据管理器，`git credential fill` 可取出（username=tuoqi-stats）

