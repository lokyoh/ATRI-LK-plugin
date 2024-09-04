# ATRI-LK项目的插件库

在这提交新插件与插件错误。

## 如何添加新插件
需要安装新依赖需要将依赖写在你的插件目录的`requirements.txt`

### 1. 直接提交

1. 请将新插件放入`plugins`目录下，rss子插件请放入`plugins/rss`下(暂不支持其他子插件)
2. 请在`plugin.json`的末尾添加以下插件信息:

```text
"插件名": {
    "path": "plugins.your_plugin",
    "docs": "插件介绍",
    "version": "版本号",
    "author": "作者",
    "is_dir": true
}
```

### 2. 提交Issue
请填写`新插件审查`