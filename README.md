# AI 概念学习技能项目（ai-concept-learning-skill）

> 仓库：[tuoqi-stats/statistics-data-analysis-2026](https://github.com/tuoqi-stats/statistics-data-analysis-2026) ｜ 课程：统计与数据分析 ｜ 更新日期：2026-09-09

## 项目简介

本项目是一个基于 **Agent Skill（智能体技能）** 的 AI 概念学习资料库。核心是一个名为 `concept-material-generator` 的项目级技能——它接收任意 AI / 机器学习 / 统计学习概念名词，按固定的五段式模板自动生成结构化学习文档，统一存放在 `learning-materials/` 目录，逐步沉淀为个人概念知识库。

**核心理念**：把"学一个新概念"从"漫无目的地搜资料"变成"一句指令产出结构化笔记"——每份文档结构一致、来源可核查、便于复习与横向对比。

**关键概念**：本项目本身就是三个 AI 概念的实践样本——

| 概念 | 在本项目中的角色 |
|------|------------------|
| **Agent（智能体）** | WorkBuddy 作为执行引擎，自主完成查重→撰写→核验→自检→落盘的闭环 |
| **大模型上下文（LLM Context）** | 技能通过渐进式披露加载进上下文窗口，控制 token 成本 |
| **Skill（技能）** | `concept-material-generator` 以 SKILL.md 文件形式定义生成流程 |

三者的三角协作关系详见 [concept-relationship.md](learning-materials/concept-relationship.md)。

---

## 目录结构

```
statistics-data-analysis-2026/
├── README.md                          # 本文件——项目总览
├── .gitignore                         # Python 模板 + 密钥/凭据屏蔽规则
│
├── .workbuddy/                        # WorkBuddy 项目配置（随仓库共享）
│   ├── skills/
│   │   └── concept-material-generator/
│   │       └── SKILL.md               # 核心技能：概念学习资料生成器
│   └── memory/
│       ├── MEMORY.md                  # 项目长期记忆
│       └── 2026-09-09.md              # 当日工作日志
│
└── learning-materials/                # AI 概念学习资料库（技能产出）
    ├── README.md                      # 资料库索引与约定
    ├── agent.md                       # Agent（智能体）
    ├── agent-skill.md                 # Agent Skill（智能体技能）
    ├── llm-context.md                 # 大模型上下文（LLM Context）
    ├── skill.md                       # Skill（技能）
    ├── concept-relationship.md        # 概念关系：Agent、上下文与 Skill
    └── concept-material-generator.md  # concept-material-generator（技能自述）
```

---

## Skill 调用方式

### 前置条件

- 已安装 [WorkBuddy](https://www.workbuddy.cn) 智能体平台
- 已克隆本仓库到本地（技能位于 `.workbuddy/skills/`，属项目级技能，随仓库自动加载）

### 触发方法

在 WorkBuddy 对话中直接输入：

```
用 concept-material-generator 生成 <概念名> 的学习资料
```

示例：

```
用 concept-material-generator 生成 Transformer 的学习资料
用 concept-material-generator 生成 假设检验 的学习资料
```

### 生成流程

技能被触发后，WorkBuddy 会自主执行以下七步闭环：

1. **确认概念** — 明确中英文名称与缩写，一词多义时先消歧
2. **查重** — 检查 `learning-materials/` 是否已有同名文档，存在则询问覆盖或归档
3. **撰写内容** — 严格按五段式模板撰写，全文简体中文，术语首现标注英文
4. **落实链接** — 逐条核验第 5 部分链接可达性，宁缺毋假
5. **自检** — 逐项核对自检清单，未通过项修正后再继续
6. **保存输出** — 写入 `learning-materials/<概念名>.md`，文件名小写 kebab-case
7. **汇报结果** — 报告文件路径并用一句话概括每部分要点

### 五段式输出模板

每份文档固定包含以下五个部分（标题一字不差）：

| 序号 | 部分 | 要求 |
|------|------|------|
| 1 | 概念个人解释 | 先类比后定义，禁止术语堆砌 |
| 2 | 核心机制或组成 | 至少拆解 2 个组成要素或关键步骤 |
| 3 | 具体应用场景 | 至少 3 个场景，每个带真实产品/论文实例 |
| 4 | 容易混淆的问题或使用边界 | 至少 1 组 "X vs Y" 对照，写明失效条件 |
| 5 | 可核查资料来源链接 | 2-5 条真实公开链接，逐条附价值说明 |

### 质量约束

- **链接宁缺毋假**：必须本会话核验可达（状态码 200）或高度确信的权威页面，否则改写为"建议检索关键词"，禁止虚构 URL
- **不使用需要登录或付费的链接**
- **写入前必须通过全部自检项**

技能完整定义见 [`.workbuddy/skills/concept-material-generator/SKILL.md`](.workbuddy/skills/concept-material-generator/SKILL.md)。

---

## 已完成文档清单

以下 6 份文档均已生成并通过自检，存放于 `learning-materials/`：

| 文档 | 概念 | 生成日期 |
|------|------|----------|
| [agent.md](learning-materials/agent.md) | Agent（智能体）— 以大模型为大脑、能自主规划与行动完成任务的 AI 系统 | 2026-09-09 |
| [agent-skill.md](learning-materials/agent-skill.md) | Agent Skill（智能体技能）— 以 SKILL.md 为核心的能力包机制 | 2026-09-09 |
| [llm-context.md](learning-materials/llm-context.md) | 大模型上下文（LLM Context）— 信息窗口及其组织管理机制 | 2026-09-09 |
| [skill.md](learning-materials/skill.md) | Skill（技能）— 技能的语义、两层谱系与产品形态 | 2026-09-09 |
| [concept-relationship.md](learning-materials/concept-relationship.md) | 概念关系：Agent、上下文与 Skill 的三角协作 | 2026-09-09 |
| [concept-material-generator.md](learning-materials/concept-material-generator.md) | concept-material-generator — 本技能的自述档案 | 2026-09-09 |

文档间通过 Markdown 相对链接互相引用，形成可检索的概念网络。

---

## 作业完成说明

### 作业目标

围绕 **Agent、大模型上下文、Skill** 三个 AI 核心概念，搭建一个可持续运行的概念学习系统，完成从"理解概念"到"沉淀资料"到"阐明关系"的完整闭环。

### 完成内容

**1. 搭建技能驱动的内容生成系统**

- 编写项目级 Agent Skill `concept-material-generator`（`.workbuddy/skills/concept-material-generator/SKILL.md`），定义了五段式输出模板、七步生成流程与质量约束条款
- 技能采用单文件极简设计（无 scripts/、references/、assets/ 资源包），约 84 行，适用于纯内容生成场景
- 配套 `learning-materials/README.md` 作为资料库索引，每次生成后自动登记

**2. 生成三个核心概念的学习文档**

- `agent.md` — Agent（智能体）：行动闭环五要素（大脑/手脚/记忆/规划/环境）、Agent vs Chatbot vs Workflow 对照
- `llm-context.md` — 大模型上下文：窗口与 token 计量、四类组成、窗口管理三板斧、上下文工程
- `skill.md` — Skill（技能）：内隐 vs 外显两层谱系、Skill vs Tool vs Plugin 对照、使用边界

**3. 生成概念关系文档**

- `concept-relationship.md` — 阐述三者三角协作关系：能力 = 基座模型 × 上下文管理 × 技能注入
- 四条咬合机制：加载链（Skill→Context→Agent）、上下文作唯一交汇面、渐进式披露作节流阀、两类知识张力
- 四种失效模式分析：技能永不加载 / 过度加载 / 上下文失管 / Agent 能力不足

**4. 生成技能自述文档**

- `concept-material-generator.md` — 技能介绍自身的设计要素、生成流程与使用边界，作为"技能长什么样"的实例样本

### 成果总结

| 维度 | 数据 |
|------|------|
| 技能文件 | 1 个（concept-material-generator，84 行 SKILL.md） |
| 概念文档 | 6 份（3 个单概念 + 1 个关系文档 + 1 个技能自述 + 1 个 Agent 概念） |
| 文档结构 | 统一五段式，全部通过自检 |
| 外部链接 | 全部核验可达（状态码 200），无虚构 URL |
| 文档互链 | 通过 Markdown 相对链接形成可检索概念网络 |

### 技术亮点

- **技能即基础设施**：不写一行传统代码，用一份 SKILL.md 定义完整的内容生成流水线，体现"文件系统即接口"的 Agent Skill 设计哲学
- **渐进式披露实践**：技能平时只占几十 token 的名称简介，触发后才加载全文——本项目自身就是 Skill × Context × Agent 三角关系的运行实例
- **质量约束内嵌**：链接核验、自检清单、查重机制均写入技能指令，确保每次产出质量一致
