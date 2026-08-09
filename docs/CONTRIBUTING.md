# 🤝 参与贡献 / Contributing

感谢你愿意让这个项目变得更好！不管你是提 Issue、修文档还是加功能，都非常欢迎。

## 环境要求

- Python 3.10+
- 本项目依赖：见 `requirements.txt`
- （可选）本地视觉模型：`python download_models.py`

## 开发约定

### 代码

- **语言**：Python，遵循 [PEP 8](https://peps.python.org/pep-0008/)。
- **注释**：中文注释为主（项目面向中英双语用户），关键逻辑加注释。
- **保持简单**：`img2text.py` 是单一职责的核心工具，尽量不引入额外依赖。
- **不提交敏感信息**：任何情况下不得把 API Key、密码、个人邮箱、token 提交进仓库。

### 文档

- README 面向用户，讲"怎么用"。
- `docs/` 面向开发者和排错，讲"为什么"。
- 中英双语优先，至少要有中文。

## 提 PR 流程

1. Fork 本仓库并克隆到本地。
2. 新建分支：`git checkout -b feat/my-improvement`。
3. 做改动并本地验证（例如跑 `python img2text.py 测试图.jpg vision`）。
4. 提交，写清改动内容。
5. 推送到你的 Fork，向 `master` 分支发起 Pull Request。
6. 在 PR 描述里说明：改了什么、为什么改、如何验证。

## 提交信息规范

- 使用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)：
  - `feat:` 新功能
  - `fix:` 修复
  - `docs:` 文档
  - `style:` 格式
  - `refactor:` 重构
  - `test:` 测试
  - 例如：`fix: 修复中文路径下 OCR 失败的问题`

## 行为准则

请阅读并遵守 [CODE_OF_CONDUCT](../CODE_OF_CONDUCT.md)。我们希望大家互相尊重、共同进步。

## 安全相关

如果发现安全问题，请**不要**直接开 Issue，按 [SECURITY](SECURITY.md) 的流程报告。
