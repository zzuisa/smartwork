# 贡献指南

感谢您对 SmartWork 项目的关注！我们欢迎各种形式的贡献，包括但不限于：

- 🐛 Bug 报告
- 💡 功能建议
- 📝 文档改进
- 🔧 代码贡献
- 🧪 测试用例

## 🚀 快速开始

### 1. Fork 项目
点击项目页面右上角的 "Fork" 按钮，将项目复制到你的 GitHub 账户。

### 2. 克隆项目
```bash
git clone https://github.com/你的用户名/smartwork.git
cd smartwork
```

### 3. 创建开发环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装依赖
pip install -r confs/requrements.txt
pip install -e .[dev]  # 安装开发依赖
```

## 🔧 开发流程

### 1. 创建分支
```bash
git checkout -b feature/你的功能名称
# 或者
git checkout -b bugfix/修复的问题描述
```

### 2. 进行开发
- 编写代码
- 添加测试用例
- 更新文档
- 确保代码符合项目规范

### 3. 运行测试
```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=. --cov-report=html

# 代码风格检查
flake8 .
black --check .
isort --check-only .
```

### 4. 提交更改
```bash
git add .
git commit -m "feat: 添加新功能描述"
# 或者
git commit -m "fix: 修复问题描述"
```

### 5. 推送并创建 Pull Request
```bash
git push origin feature/你的功能名称
```

然后在 GitHub 上创建 Pull Request。

## 📝 代码规范

### Python 代码风格
- 遵循 PEP 8 规范
- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 函数和类需要添加文档字符串

### 提交信息规范
使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

类型包括：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat: 添加性能监控功能

- 新增 PerformanceMonitor 类
- 添加性能监控装饰器
- 更新相关文档

Closes #123
```

## 🧪 测试指南

### 测试结构
```
tests/
├── test_file_handler.py
├── test_excel_tools.py
├── test_config_tools.py
└── test_performance_tools.py
```

### 编写测试
```python
import pytest
from handler.file_handler import do_count

def test_do_count():
    """测试文件计数功能"""
    smart_dict = {}
    report_dict = {}
    path = "test_data/sample.txt"
    
    result = do_count(smart_dict, report_dict, path)
    
    assert result is not None
    assert len(smart_dict) > 0
```

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_file_handler.py

# 运行特定测试函数
pytest tests/test_file_handler.py::test_do_count

# 详细输出
pytest -v
```

## 📚 文档规范

### README 更新
- 新功能需要更新 README.md
- 添加使用示例
- 更新安装说明

### 代码文档
- 所有公共函数和类都需要文档字符串
- 使用 Google 风格的文档字符串

```python
def process_file(file_path: str, options: dict = None) -> dict:
    """
    处理工作日志文件
    
    Args:
        file_path: 文件路径
        options: 处理选项，默认为 None
        
    Returns:
        处理结果字典
        
    Raises:
        FileNotFoundError: 当文件不存在时
        ValueError: 当文件格式不正确时
    """
    pass
```

## 🐛 Bug 报告

### 报告模板
```markdown
**Bug 描述**
简要描述遇到的问题

**重现步骤**
1. 执行命令 '...'
2. 点击 '...'
3. 看到错误

**预期行为**
描述你期望发生什么

**实际行为**
描述实际发生了什么

**环境信息**
- 操作系统: [e.g. Windows 10]
- Python 版本: [e.g. 3.8.8]
- SmartWork 版本: [e.g. 1.5.0]

**附加信息**
添加任何其他相关信息
```

## 💡 功能建议

### 建议模板
```markdown
**功能描述**
简要描述你希望添加的功能

**使用场景**
描述这个功能的使用场景

**实现建议**
如果有实现想法，请描述

**附加信息**
添加任何其他相关信息
```

## 🔍 代码审查

### 审查清单
- [ ] 代码符合项目规范
- [ ] 添加了适当的测试
- [ ] 更新了相关文档
- [ ] 提交信息清晰明确
- [ ] 没有破坏现有功能

### 审查流程
1. 自动检查（CI/CD）
2. 维护者审查
3. 代码合并

## 📞 获取帮助

- 创建 [Issue](https://github.com/zzuisa/smartwork/issues) 提问
- 查看 [文档](https://github.com/zzuisa/smartwork#readme)
- 阅读 [性能优化报告](PERFORMANCE_OPTIMIZATION.md)

## 🎉 贡献者

感谢所有为项目做出贡献的开发者！

<!-- 这里会自动生成贡献者列表 -->

## 📄 许可证

通过贡献代码，您同意您的贡献将在 MIT 许可证下发布。

---

再次感谢您的贡献！🎉
