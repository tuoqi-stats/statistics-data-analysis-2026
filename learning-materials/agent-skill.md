# Agent Skill（智能体技能）

> 生成日期：2026-09-09 ｜ 类别：AI 概念学习资料

（注：本文指 2025 年 10 月 Anthropic 正式发布、此后被多个智能体产品采用的 "Agent Skills" 机制——以 SKILL.md 文件为核心的能力包，而非泛指智能体拥有的任何能力。）

## 1. 概念个人解释

先打个比方：AI 智能体（Agent）像一个智商很高但啥流程都不知道的新员工——会思考、会写代码、会用工具，但不知道你们公司的 PPT 模板长什么样、不知道部署要走哪几步审批。Agent Skill 就是给这位新员工准备的"岗位操作手册 + 随取随用的工具箱"：每个技能是一份说明文档，旁边可以放脚本、模板、参考资料，任务来了翻开对应的册子照着做。

正式一点说：Agent Skill 是一种以文件夹形式打包的智能体能力模块——核心是一个用 Markdown 编写的 SKILL.md（技能清单文件，开头是名称与简介等元数据，正文是详细指令），可附带脚本、模板、参考文档等资源。智能体平时只记住每个技能的名字和一句话简介，遇到匹配的任务时才加载完整内容，从而在不重新训练模型、不修改系统提示词的前提下获得新能力。一个就在眼前的例子：你正在读的这份学习资料，就是由一个叫 concept-material-generator 的 Agent Skill 生成的——它的 SKILL.md 里写着"如何生成五段式概念学习文档"的完整流程。

## 2. 核心机制或组成

Agent Skill 的设计可以拆成四个关键要素：

1. **SKILL.md 清单文件**：每个技能的必备核心，分两层——YAML frontmatter（name、description 等元数据）与 Markdown 正文（操作指令、流程、规范）。其中 description 是"触发器"：智能体依据这段简介判断当前任务是否需要加载该技能，所以它必须写清"这个技能是干什么的、什么时候用"。
2. **可选资源包**（三类，按需取用）：
   - `scripts/`：可执行脚本（Python、Bash 等），把精确、确定性的操作交给传统代码而不是让模型逐字生成
   - `references/`：详细参考文档，正文装不下的细节放这里
   - `assets/`：模板文件、样式表等静态素材
3. **渐进式披露（progressive disclosure）**：控制上下文成本的分层加载机制——启动时只加载所有技能的名称与简介（每个几十 token）→ 任务匹配时才读取 SKILL.md 全文（几千 token）→ 执行中遇到需要时才读 references/（可上万 token）。类比：扫一眼书脊 → 翻开某本书 → 查附录。
4. **文件系统即接口**：没有注册中心、没有专用运行时、没有 API——把文件夹拷进 skills 目录就完成了"安装"，改动即时生效，天然可用 git 做版本管理。Anthropic 工程团队的比喻：与其建一个数据库驱动的应用商店，不如用"20 美元的文件存储"。

## 3. 具体应用场景

1. **Anthropic Claude 全家桶**：claude.ai、Claude Code、Agent SDK 于 2025 年 10 月正式内置 Agent Skills，官方预装了 PPT 生成、Word 处理、Excel 分析、PDF 处理等技能，同时开放自定义——把品牌规范、业务流程写成 SKILL.md 即可全平台复用。
2. **WorkBuddy 智能体平台**：分为用户级（`~/.workbuddy/skills/`，全局可用）与项目级（`.workbuddy/skills/`，团队共享）两层，内置办公套件技能并提供推荐市场。本仓库正在使用的 concept-material-generator 就是一个项目级 skill——在对话里说一句"生成 XX 概念的学习资料"即可触发。
3. **Claude Code 编程智能体**：开发者将团队代码规范、提交流程、部署手册写成技能，让编程智能体按约定执行（官方文档见 code.claude.com/docs/en/skills），配合 slash command 机制沉淀为可复用的工作流。
4. **社区共享生态**：GitHub 上出现了官方技能仓库与各类社区合集，沉淀数据处理、文档写作、设计等数百个现成技能，形成"写一次、处处可用"的分发模式。

## 4. 容易混淆的问题或使用边界

1. **Agent Skill vs 工具调用（Tool Use / Function Calling）**：tool 是一个可被调用的 API/函数——结构化的机器接口，参数由 schema 严格定义；skill 是"何时以及如何（组合多个工具）完成任务"的知识——自然语言说明书。类比：tool 是发一把锤子，skill 是教一套装修流程。一个 skill 的正文常常指导智能体去调用若干 tools，二者是配套而非互斥。
2. **Agent Skill vs MCP（Model Context Protocol）**：MCP 是连接外部系统的标准协议，需要运行一个 server（客户端-服务器架构），解决的是"连接"（connectivity）；skill 是纯静态文件，解决的是"知识与方法"（knowledge）。互补关系：MCP 把数据库、网盘接进来，skill 教智能体拿到数据后怎么分析。
3. **Agent Skill vs RAG（检索增强生成）**：RAG 在运行时按语义或关键词检索外部文档片段、拼进上下文，管"找资料"；skill 是预先组织好的指令，由智能体主动判断、按需完整读取，管"照说明书办事"。前者像图书馆检索员，后者像标准作业程序（SOP）手册。
4. **使用边界与失效条件**：需要实时状态或双向交互的系统集成（消息通知、数据库连接）应选 MCP/工具调用；需要严格类型保证的参数传递应选结构化工具；上下文窗口紧张时，技能设计必须遵循渐进披露——否则一份几千行的说明文档就能吃掉大半上下文；琐碎的一次性问题也不值得加载技能，直接问更快。

## 5. 可核查资料来源链接

- https://www.anthropic.com/news/skills — Anthropic 官方发布页：Agent Skills 的正式定义、功能演示与产品级介绍（实测可达 200）
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills — Anthropic 工程博客：设计哲学的完整论述，含渐进式披露与"文件系统即接口"的取舍分析（实测可达 200）
- https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview — 官方文档：SKILL.md 的结构规范、目录约定与编写指南（实测可达 200）
- https://code.claude.com/docs/en/skills — Claude Code 官方文档：编程智能体中技能的开发、调试与使用说明（实测可达 200）
