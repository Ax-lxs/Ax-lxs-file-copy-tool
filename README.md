# Ax-lxs-file-copy-tool
文件批量复制工具

### 命名规则说明
支持以下占位符：
- {n}: 序号
- {name}: 原文件名
- {date}: 日期(YYYYMMDD)
- {time}: 时间(HHMMSS)
- {ext}: 文件扩展名

### 使用示例
1. 基础编号：
   - 格式：`{name}_{n}{ext}`
   - 结果：`文件_1.txt`, `文件_2.txt`

2. 日期命名：
   - 格式：`{date}_{name}{ext}`
   - 结果：`20240301_文件.txt`

3. 自定义前缀：
   - 格式：`Copy_{n}_{name}{ext}`
   - 结果：`Copy_1_文件.txt`, `Copy_2_文件.txt`

4. 序号填充：
   - 设置序号位数为3
   - 格式：`{name}_{n}{ext}`
   - 结果：`文件_001.txt`, `文件_002.txt`

## 打包说明

使用 PyInstaller 打包成可执行文件：



## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

[MIT License](LICENSE)