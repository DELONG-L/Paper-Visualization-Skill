# Custom reading example / 定制阅读示例

[English home](../README.md) · [中文首页](../README.zh-CN.md)

The bilingual example uses a custom static layout. Its `site` and `citation` config fields retain their documented meaning; the `demo` field contains content for the example's annotations and sections. [render_demo.py](../examples/reading-demo/scripts/render_demo.py) renders both HTML editions. The reusable skill and starter template are separate from this example.

双语示例采用定制的静态版式。配置中的 `site`、`citation` 字段保留原有含义；`demo` 字段提供本示例的标注与章节内容。[render_demo.py](../examples/reading-demo/scripts/render_demo.py) 生成两版 HTML。可复用技能与初始模板独立于这个定制示例。

Edit the English or Chinese `paper-visualization.config.json`, then render:

修改英文或中文 `paper-visualization.config.json` 后，重新生成页面：

```bash
python3 examples/reading-demo/scripts/render_demo.py
```

The two editions share their interaction behavior and visual rules. Keep the two copies of `styles.css` and `script.js` synchronized when changing them.

两版使用相同的交互和视觉规则。修改时，应同步两份 `styles.css` 与 `script.js`。

To materialize metadata, generate the sitemap, and build the portable public site package:

生成静态元数据、站点地图及可迁移的公开站点包：

```bash
bash examples/reading-demo/scripts/sync_site_package.sh
```

Preview the package:

预览打包后的页面：

```bash
python3 -m http.server 8123 --bind 127.0.0.1 --directory examples/reading-demo/package
```

Open `http://127.0.0.1:8123/` or `http://127.0.0.1:8123/zh/`. The site uses local CSS and JavaScript, with no external runtime fonts or libraries. Source links open public GitHub documents.

打开 `http://127.0.0.1:8123/` 或 `http://127.0.0.1:8123/zh/`。页面使用本地 CSS 与 JavaScript，不依赖外部运行时字体或库。来源链接打开 GitHub 上的公开文档。

For GitHub Pages, enable GitHub Actions as the publishing source. The [Pages workflow](../.github/workflows/pages.yml) builds and deploys only `examples/reading-demo/package/`. Before publishing a fork or using another host, update the canonical URLs, alternates, and social preview URLs in both configs. The package contains public site files and the MIT licence; keep manuscripts and private sources outside the site directory.

使用 GitHub Pages 时，将发布源设置为 GitHub Actions。[Pages 工作流](../.github/workflows/pages.yml) 仅构建并部署 `examples/reading-demo/package/`。发布分叉仓库或更换托管地址前，应更新两份配置中的规范链接、语言互链与社交预览地址。打包内容为公开站点文件与 MIT 许可证；稿件和私人来源应保留在站点目录之外。
