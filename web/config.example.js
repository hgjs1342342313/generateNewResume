// 简历生成器配置文件
// 请在部署前修改此文件

// GitHub 仓库信息（格式：owner/repo）
window.GITHUB_REPO = 'your-username/generateNewResume';

// GitHub Personal Access Token
// ⚠️ 警告：请使用具有 repo 权限的 token
// ⚠️ 安全提示：不要将包含真实 token 的文件提交到公开仓库！
// 建议方式：
// 1. 使用 GitHub Actions 自动部署时，通过 secrets 注入
// 2. 使用后端代理服务，不在前端暴露 token
// 3. 仅在本地测试时使用
window.GITHUB_TOKEN = '';

// 如果不配置 GitHub，用户仍可使用"下载 ZIP"功能自行编译