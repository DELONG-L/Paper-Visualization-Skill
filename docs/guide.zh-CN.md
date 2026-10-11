# 使用指南

[返回首页](../README.zh-CN.md) · [English](guide.md)

以下命令从仓库根目录运行。骨架脚本需要 Python 3；生成的网页使用 HTML、CSS、JavaScript 和 JSON。

## 安装与调用

按照[首页安装步骤](../README.zh-CN.md#开始使用)安装 `skills/paper-visualization`，然后调用 `$paper-visualization`。已有安装时先保留本地修改。

## 从论文开始

```bash
python3 skills/paper-visualization/scripts/bootstrap_paper_visualization.py ./my-paper --pdf ./paper.pdf
```

需要中英文路由和正式网址时：

```bash
python3 skills/paper-visualization/scripts/bootstrap_paper_visualization.py ./my-paper \
  --pdf ./paper.pdf \
  --bilingual \
  --public-url https://example.com/publications/my-paper/ \
  --site-dir docs \
  --release-dir release/site-package
```

默认创建 `docs/`、`docs/paper-visualization.config.json`、发布包目录，以及元数据和打包脚本。`--bilingual` 额外创建 `docs/zh/` 及对应配置。

## 填写内容

配置包含标题、作者、单位、论文链接、页面元数据、概览、各章节和引用。先核对问题、方法和结论的依据，再选择适合原论文的结构。正式作者名保持准确，翻译后的结论保留同样的限定条件。

把公开图表放在 `docs/assets/`。中英文页面可以共享图表。内置 `framework`、`lifecycle`、`showcase`、`stats`、`split` 等布局；配置无法表达所需版式时，直接修改 HTML、CSS、JavaScript。

## 预览与交付

进入生成的项目目录：

```bash
python3 -m http.server 8123 --bind 127.0.0.1
```

打开 `http://127.0.0.1:8123/docs/`，双语项目同时检查 `docs/zh/`。检查正文、图表、手机布局、语言切换和引用。完成编辑后运行：

```bash
./scripts/sync_site_package.sh
```

该脚本更新页面元数据和 `sitemap.xml`，并同步发布目录。可将 `release/site-package/` 放到静态托管服务；没有明确公开要求的论文源码、草稿和私有材料留在写作目录。

## 更多参考

[完整配置格式](../skills/paper-visualization/references/config-schema.md) · [内容工作流](../skills/paper-visualization/references/workflow.md) · [技能入口](../skills/paper-visualization/SKILL.md) · [许可证](../LICENSE)
