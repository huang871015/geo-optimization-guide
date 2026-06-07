# GEO Optimization Guide

生成式引擎优化（Generative Engine Optimization）实战指南——让品牌被AI搜索引擎推荐。

## 什么是GEO

GEO是AI搜索时代的品牌可见度优化方法论。不同于传统SEO追求搜索排名，GEO追求的是：当用户向豆包、DeepSeek、Kimi、ChatGPT等AI助手提问时，你的品牌能否出现在AI的推荐结果中。

**核心理念**：不是"让用户在搜索栏找到你"，而是"让AI在回答问题时推荐你"。

## 方法论

基于Princeton KDD 2024和ICLR 2026学术研究，GEO三大核心策略：

| 策略 | AI引用概率提升 | 说明 |
|------|---------------|------|
| Cite Sources | +115% | 清晰标注信息来源 |
| Statistics | +40% | 用具体数据替代模糊描述 |
| Fluency | +29% | 清晰的结构化表达 |

技术栈：JSON-LD结构化数据 · AI爬虫友好化 · 语义HTML · 时间信号 · Schema.org词汇表

## 自案例（Self-Case）

我们在自有站点实践GEO方法论，公开追踪效果：

- **网站**：[nister.promptmin.cn](https://nister.promptmin.cn)
- **AI优化页面**：[nister.promptmin.cn/ai/](https://nister.promptmin.cn/ai/)
- **方法论文档**：[nister.promptmin.cn/methodology/](https://nister.promptmin.cn/methodology/)
- **博客更新**：[nister.promptmin.cn/blog/](https://nister.promptmin.cn/blog/)

### 当前状态（2026-06-07）

- [x] 网站V3编辑风格上线
- [x] JSON-LD结构化数据部署（Organization + WebSite + FAQPage + Article + BreadcrumbList）
- [x] AI爬虫友好化（robots.txt放行7家AI爬虫、llms.txt、ai.txt）
- [x] Bing Webmaster验证 + sitemap提交
- [x] 百度站长平台验证 + sitemap提交
- [x] 头条搜索站长平台验证 + sitemap提交
- [x] IndexNow主动推送
- [x] ICP/公安备案完成
- [ ] 中国AI爬虫（DeepSeekBot/ByteSpider/MoonshotBot）首次访问（监控中）
- [ ] 建立20个关键词追踪基线

### AI爬虫访问追踪

```bash
ssh root@111.231.24.138
grep -i 'ByteSpider\|DeepSeekBot\|MoonshotBot\|GPTBot\|ClaudeBot' /var/log/nginx/access.log | awk '{print $4,$7}' | sort | uniq -c | sort -rn
```

## 文件结构

```
.
├── README.md                    # 本文件
├── llms.txt                     # LLM爬虫友好文件
├── ai.txt                       # AI平台声明文件
├── robots.txt                   # 爬虫规则 + 多sitemap引用
├── sitemap.xml                  # Hugo自动生成
└── sitemap-ai.xml               # AI诱捕页面sitemap
```

## 相关资源

- Schema.org 词汇表：https://schema.org/docs/full.html
- Google Rich Results Test：https://search.google.com/test/rich-results
- Bing Webmaster Tools：https://www.bing.com/webmasters
- IndexNow Protocol：https://www.indexnow.org

## 许可

MIT — 欢迎参考、修改和使用。如果这个仓库对你有帮助，给个star让更多人看到。我们也会持续更新自案例的实测数据。
