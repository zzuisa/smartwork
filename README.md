# SmartWork - 智能工作日志管理系统

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)]
[![Performance](https://img.shields.io/badge/performance-optimized-orange.svg)]

## 📋 项目简介

SmartWork 是一个智能工作日志管理系统，专为需要定期统计和汇报工作量的场景设计。系统能够自动处理工作日志文件，生成标准化的交付件报表，并提供每日工作目录自动生成功能。

**当前版本**: V 1.6.0 - 配置优化版本

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

- Python 3.8+
- 依赖包：见 `confs/requirements.txt`

## 🛠️ 安装步骤

1. 克隆项目到本地
2. 安装依赖包：
```bash
pip install -r confs/requirements.txt
```

## ⚙️ 配置设置

编辑配置文件 `confs/conf.ini`，根据你的需求调整参数

### 主要配置项

- **路径配置**：设置工作日志目录、报告输出目录、模板目录
- **问题分类**：配置工作日志中的问题分类标签
- **时间配置**：设置不同类型工作的标准时长
- **性能配置**：调整缓存大小、批处理参数等

## 🚀 使用方法

### 基本用法

```bash
# 处理指定日期的工作日志
python main.py --date 2024-01-15

# 处理指定日期范围的工作日志
python main.py --date 2024-01-01 --end-date 2024-01-31

# 简单模式（只生成统计报表）
python main.py --simple

# 自动模式（创建每日工作文件夹）
python main.py --auto
```

### 参数说明

- `--date`: 指定处理日期（格式：YYYY-MM-DD）
- `--end-date`: 指定结束日期（格式：YYYY-MM-DD）
- `--simple`: 简单模式，只生成统计报表
- `--auto`: 自动模式，创建每日工作文件夹

## 📁 项目结构

```
smartwork/
├── main.py                 # 主程序入口
├── base/                   # 基础模块
│   └── constants.py        # 常量定义
├── confs/                  # 配置文件
│   ├── conf.ini           # 主配置文件
│   └── requirements.txt   # 依赖包列表
├── handler/               # 处理模块
│   └── file_handler.py    # 文件处理逻辑
├── crontab/               # 定时任务
│   └── auto.py           # 自动任务
└── util/                  # 工具模块
    ├── common_tools.py    # 通用工具
    ├── config_tools.py    # 配置工具
    ├── encoding_converter_tools.py  # 编码转换工具
    ├── excel_tools.py     # Excel工具
    └── list_tools.py      # 列表工具
```

## 📊 输出说明

### 统计报表
- 按问题分类统计工作量
- 按时间维度统计工作分布
- 按责任人统计工作分配

### 交付件报表
- 详细的工作记录列表
- 包含问题描述、处理时长、责任人等信息
- 支持Excel格式导出

## 🔧 配置说明

### 核心配置节

- `[smartwork]`: 核心配置，包含路径、表头等
- `[issue-types]`: 问题类型配置
- `[country-mapping]`: 国家映射配置
- `[time-config]`: 时间配置
- `[performance]`: 性能配置
- `[file-config]`: 文件处理配置

### 配置示例

```ini
[smartwork]
# 工作日志基础目录
base_folder = /path/to/worklogs/
# 报告输出目录
report_folder = /path/to/reports/
# 模板目录
template_folder = /path/to/templates/

[time-config]
# 案例输出工作时长
case_output_hours = 3
# 默认工作时长
default_hours = 2
```

## 🚀 性能特性

- **智能缓存**：配置和计算结果自动缓存
- **批量处理**：支持大量文件的高效处理
- **内存优化**：减少内存占用，提高处理效率
- **进度显示**：实时显示处理进度
- **错误恢复**：自动处理异常情况

## 📝 使用示例

### 处理单日工作日志
```bash
python main.py --date 2024-01-15
```

### 处理月度工作日志
```bash
python main.py --date 2024-01-01 --end-date 2024-01-31
```

### 创建每日工作文件夹
```bash
python main.py --auto
```

## 🔍 故障排除

### 常见问题

1. **配置文件错误**
   - 检查 `confs/conf.ini` 文件格式
   - 确认路径配置正确

2. **文件编码问题**
   - 系统会自动检测和转换文件编码
   - 支持的文件类型：.txt

3. **权限问题**
   - 确保对工作目录有读写权限
   - 检查输出目录的访问权限

## 📈 版本历史

- **V 1.6.0** - 配置优化版本
  - 全面配置化，支持灵活参数调整
  - 增强错误处理和日志记录
  - 优化性能和内存使用

- **V 1.5.0** - 性能优化版本
  - 整体性能提升39%
  - 内存使用减少29%
  - 智能缓存机制

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 📄 许可证

本项目采用MIT许可证。

## 📞 联系方式

如有问题或建议，请通过Issue联系。

---

**注意**: 使用前请根据实际环境修改配置文件中的路径和参数设置。