# 简历生成器

基于 LaTeX 的专业简历生成器，支持在线填写表单，自动编译生成 PDF。

## ✨ 特性

- 📝 **在线表单填写**：无需手写 LaTeX，通过友好的表单界面填写简历内容
- 🔄 **实时预览**：JSON 数据预览，确保信息正确
- 🚀 **自动编译**：通过 GitHub Actions 自动编译 LaTeX 生成 PDF
- 📦 **离线支持**：可下载 LaTeX 源文件，本地自行编译
- 🎨 **专业模板**：基于 [billryan/resume](https://github.com/billryan/resume) 优雅模板

## 🏗️ 架构

```
用户填写表单（前端）
    ↓
提交 JSON 到 GitHub 仓库
    ↓
触发 GitHub Actions
    ↓
编译 LaTeX 生成 PDF
    ↓
返回下载链接
```

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/generateNewResume.git
cd generateNewResume
```

### 2. 配置 GitHub Token（可选）

如果需要在线编译功能，需要配置 GitHub Personal Access Token：

1. 前往 [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. 创建新 token，勾选 `repo` 权限
3. 复制 `web/config.example.js` 为 `web/config.js`
4. 填入你的仓库信息和 token

```javascript
// web/config.js
window.GITHUB_REPO = 'your-username/generateNewResume';
window.GITHUB_TOKEN = 'ghp_your_token_here';
```

⚠️ **安全警告**：不要将包含真实 token 的 `config.js` 提交到公开仓库！

### 3. 部署前端

#### 方式 A：腾讯 EdgeOne（推荐）

1. 登录 [腾讯云 EdgeOne 控制台](https://console.cloud.tencent.com/edgeone)
2. 创建站点，选择静态网站托管
3. 上传 `web/` 目录内容
4. 绑定自定义域名

#### 方式 B：GitHub Pages

1. 在仓库 Settings > Pages 中启用 GitHub Pages
2. 选择 `web/` 目录作为源
3. 访问 `https://your-username.github.io/generateNewResume/`

#### 方式 C：本地预览

```bash
cd web
python3 -m http.server 8000
# 访问 http://localhost:8000
```

### 4. 启用 GitHub Actions

确保仓库的 Actions 已启用：

1. 前往仓库的 Settings > Actions > General
2. 确保 "Allow all actions and reusable workflows" 被选中

## 📖 使用说明

### 在线生成（需配置 GitHub Token）

1. 打开网站，填写简历表单
2. 点击"下一步"预览数据
3. 点击"提交到 GitHub Actions 编译"
4. 等待 1-3 分钟，下载生成的 PDF

### 离线生成

1. 打开网站，填写简历表单
2. 点击"下载 LaTeX 源文件 ZIP"
3. 解压后，将 `.tex` 文件与 `resume/` 模板目录放在一起
4. 使用 XeLaTeX 编译：

```bash
xelatex resume_你的姓名_时间戳.tex
```

### 在线编译（Overleaf）

1. 下载 LaTeX 源文件
2. 上传到 [Overleaf](https://www.overleaf.com/)
3. 在线编译并下载 PDF

## 📁 项目结构

```
generateNewResume/
├── .github/
│   └── workflows/
│       └── build-resume.yml    # GitHub Actions 编译流程
├── resume/                     # LaTeX 模板文件
│   ├── resume.cls              # 简历类定义
│   ├── resume-zh_CN.tex        # 中文简历示例
│   └── fonts/                  # 字体文件
├── scripts/
│   └── generate_resume.py      # JSON → LaTeX 生成脚本
├── schema/
│   └── resume.schema.json      # 简历数据结构定义
├── web/
│   ├── index.html              # 前端页面
│   ├── config.example.js       # 配置示例
│   └── config.js               # 实际配置（需自行创建）
├── examples/
│   └── sample_resume.json      # 示例简历数据
├── pending/                    # 待处理的简历 JSON（自动创建）
├── processed/                  # 已处理的简历 JSON（自动创建）
└── output/                     # 生成的文件（自动创建）
```

## 🔧 自定义

### 修改简历模板

简历模板位于 `resume/` 目录，你可以：

- 修改 `resume.cls` 调整样式
- 修改字体、颜色、布局等
- 添加自定义宏

### 修改数据结构

简历数据结构定义在 `schema/resume.schema.json`，你可以：

- 添加新的字段
- 修改字段约束
- 扩展支持的内容类型

修改后需要同步更新：
1. `scripts/generate_resume.py` 中的生成逻辑
2. `web/index.html` 中的表单字段

## 🛠️ 技术栈

- **前端**：原生 HTML/CSS/JavaScript，无框架依赖
- **后端**：GitHub Actions（无服务器）
- **编译**：XeLaTeX（TeX Live）
- **模板**：基于 [billryan/resume](https://github.com/billryan/resume)

## 📝 简历数据结构

```json
{
  "personal": {
    "name": "姓名",
    "email": "邮箱",
    "phone": "电话"
  },
  "education": [
    {
      "school": "学校名称",
      "location": "地点",
      "period": "时间段",
      "degree": "学位",
      "major": "专业"
    }
  ],
  "experience": [
    {
      "company": "公司名称",
      "department": "部门",
      "period": "时间段",
      "role": "职位",
      "responsibilities": "核心职责",
      "projects": [
        {
          "title": "项目标题",
          "icon": "faShield",
          "challenge": "挑战/背景",
          "achievements": ["成果1", "成果2"]
        }
      ]
    }
  ],
  "skills": ["技能1", "技能2"]
}
```

## ❓ 常见问题

### Q: 为什么需要 GitHub Token？

A: 前端需要通过 GitHub API 提交文件来触发 Actions。如果你不想在前端暴露 token，可以：
- 使用后端代理服务
- 仅使用"下载 ZIP"功能

### Q: 编译失败怎么办？

A: 检查以下几点：
1. 确保简历数据格式正确
2. 查看 Actions 日志了解具体错误
3. 尝试下载 ZIP 本地编译，查看详细错误信息

### Q: 如何修改字体？

A: 编辑 `resume.cls` 中的字体配置，或修改 `.tex` 文件中的字体包引用。

### Q: 支持英文简历吗？

A: 当前模板主要针对中文简历，英文简历需要修改模板去除中文字体依赖。

## 📄 License

本项目基于 [billryan/resume](https://github.com/billryan/resume) 模板，遵循 MIT License。

## 🙏 致谢

- [billryan/resume](https://github.com/billryan/resume) - 优雅的 LaTeX 简历模板
- [XeLaTeX](https://ctan.org/pkg/xetex) - 强大的排版引擎
- [GitHub Actions](https://github.com/features/actions) - 自动化编译服务