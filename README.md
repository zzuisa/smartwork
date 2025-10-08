# SmartWork - 智能工作日志管理系统

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Performance](https://img.shields.io/badge/performance-optimized-orange.svg)](PERFORMANCE_OPTIMIZATION.md)

## 📋 项目简介

SmartWork 是一个智能工作日志管理系统，专为需要定期统计和汇报工作量的场景设计。系统能够自动处理工作日志文件，生成标准化的交付件报表，并提供每日工作目录自动生成功能。

## ✨ 主要功能

- 🔄 **自动生成每日工作文件夹** - 按日期和星期自动创建工作目录结构
- 📊 **智能工作日志解析** - 自动识别和分类工作内容
- 📈 **月底交付件报表生成** - 基于工作日志导出标准化报表
- 🚀 **高性能处理** - 整体性能提升39%，内存使用减少29%
- 💾 **智能缓存机制** - 配置和计算结果缓存，避免重复计算
- 🛡️ **健壮错误处理** - 完善的异常处理和错误恢复机制

## 🚀 性能优化亮点

- **整体性能提升 39%**：文件处理和Excel生成速度显著提升
- **内存使用减少 29%**：优化内存管理，减少资源占用
- **智能缓存机制**：配置和计算结果缓存，避免重复计算
- **批量处理优化**：支持大数据量的高效处理
- **错误处理增强**：更健壮的异常处理和错误恢复

## 📦 安装要求

### 系统要求
- Python 3.8+
- Windows/Linux/macOS

### 依赖包
```bash
pip install -r confs/requrements.txt
```

主要依赖：
- `openpyxl==3.0.10` - Excel文件处理
- `pandas==1.4.4` - 数据处理
- `chardet==5.0.0` - 文件编码检测
- `tqdm==4.64.1` - 进度条显示

## 🎯 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/zzuisa/smartwork.git
cd smartwork
```

### 2. 安装依赖
```bash
pip install -r confs/requrements.txt
```

### 3. 配置设置
编辑 `confs/conf.ini` 文件，设置你的工作目录路径：
```ini
[smartwork]
base_folder = D:\worklogs\
report_folder = D:\workspace\0交付件
template_folder = D:\workspace\0templates
```

### 4. 运行程序

#### 生成每日工作目录
```bash
python main.py auto
```

#### 统计交付件并生成报表
```bash
python main.py
```

#### 导出指定日期范围的报告
```bash
python main.py 1205  # 导出12月05日之后的报告
python main.py 1201,1215  # 导出12月01日到12月15日的报告
```

#### 使用极简模式（适合在线粘贴）
```bash
python main.py -s
```

## 📁 项目结构

```
smartwork/
├── base/                    # 基础模块
│   └── constants.py        # 常量定义
├── confs/                  # 配置文件
│   ├── conf.ini           # 主配置文件
│   └── requrements.txt    # 依赖包列表
├── crontab/               # 定时任务
│   └── auto.py           # 自动生成工作目录
├── handler/               # 文件处理模块
│   └── file_handler.py   # 核心文件处理逻辑
├── util/                  # 工具模块
│   ├── common_tools.py   # 通用工具
│   ├── config_tools.py   # 配置工具
│   ├── encoding_converter_tools.py  # 编码转换工具
│   ├── excel_tools.py    # Excel处理工具
│   ├── list_tools.py     # 列表工具
│   └── performance_tools.py  # 性能优化工具
├── main.py               # 主程序入口
├── README.md            # 项目说明
├── PERFORMANCE_OPTIMIZATION.md  # 性能优化报告
└── .gitignore          # Git忽略文件
```

## 📊 输出示例

### 统计结果示例
```json
{
    "第三方问题": 0,
    "非问题": 0,
    "系统配置问题": 1,
    "系统问题": 0,
    "业务配置问题": 0,
    "转需求": 0,
    "咨询问题": 1,
    "变更实施": 1,
    "灰度升级部署": 4,
    "告警、监控、巡检": 10,
    "案例输出": 1,
    "变更评审": 1,
    "资源管理": 13,
    "总计": 32
}
```

### 交付件报表示例
| 外部单号 | 业务系统 | 应用模块 | 问题发现时间 | 问题处理时长 | 状态 | 问题分类 | 问题描述 | 根因分析 | 国家 | 责任人 | 备注 | 问题大类 |
|---------|---------|---------|-------------|-------------|------|---------|---------|---------|------|-------|------|---------|
| R01941735 | CBG Myhuawei | 服务化中台 | 2022/09/28 | 4 | Closed | 变更实施 | 服务中台forum | 拉、推镜像，升级cce，刷数据库脚本 | 新加坡 | xx | | 操作类 |

## 🔧 配置说明

### 工作日志格式
系统支持以下格式的工作日志：

```
1. 【案例输出】【DE:vmall[vmall-op]】案例标题
   详细描述内容...

2. 【IT数据查询】【DE:vmall[vmall-op]】查询内容
   查询结果和说明...

3. 【业务咨询问题】【DE:vmall[vmall-cons]】咨询内容
   解答和说明...
```

### 问题分类
系统支持以下问题分类：
- 第三方问题
- 非问题
- 系统配置问题
- 系统问题
- 业务配置问题
- 转需求
- 业务咨询问题
- 变更实施
- 灰度升级部署
- 告警、监控、巡检
- 案例输出
- 变更评审
- 资源管理

## 🚀 性能优化

本项目经过全面性能优化，详细优化报告请查看 [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md)

### 主要优化成果
- 整体性能提升 39%
- 内存使用减少 29%
- 文件处理速度提升 30-50%
- Excel生成速度提升 40-60%
- 配置加载速度提升 88%

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目链接: [https://github.com/zzuisa/smartwork](https://github.com/zzuisa/smartwork)
- 问题反馈: [Issues](https://github.com/zzuisa/smartwork/issues)

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

⭐ 如果这个项目对你有帮助，请给它一个星标！