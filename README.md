# GEO 中文 AI 搜索引擎优化 — 开源工具箱

让中国 AI 平台（豆包、DeepSeek、Kimi、元宝、文心一言）能发现、理解并引用你的网站。

## 快速开始

```bash
# 检测你的网站在 AI 平台上的可见度
python geovis.py your-domain.com

# JSON 输出（CI/CD 集成用）
python geovis.py your-domain.com --json
```

**geovis** 会检查：
- 15 家 AI 爬虫的 robots.txt 访问权限
- llms.txt、sitemap、ai.txt 等 AI 发现文件
- JSON-LD 结构化数据
- 内容质量（中文文本量、H1、RSS）
- 输出 0-100 分的 AI 可见度评分

## 中国 AI 爬虫清单

| 爬虫 | 平台 | User-Agent | 推荐 |
|------|------|-----------|------|
| Bytespider | 豆包 (ByteDance) | `Bytespider` | 放行 + 限速 |
| DeepSeekBot | DeepSeek | `DeepSeekBot` | 放行 |
| MoonshotBot | Kimi (月之暗面) | `MoonshotBot` | 放行 |
| YuanbaoBot | 元宝 (腾讯) | `YuanbaoBot` | 放行 |
| Baiduspider | 文心一言 (百度) | `Baiduspider` | 放行 |

与 GPTBot、ClaudeBot 等国际爬虫不同，中国 AI 爬虫有独立的抓取策略。**大多数英文 GEO 工具不覆盖这些爬虫。**

## 模板

`templates/` 目录提供即用型配置：

| 文件 | 用途 |
|------|------|
| `robots-ai-max.txt` | 最大 AI 可见度 robots.txt 模板 |
| `jsonld-organization.json` | Organization 结构化数据模板（含 sameAs 锚定） |
| `llms.txt` | AI 爬虫站点索引模板 |

## GEO 核心原则

**GEO 不是 SEO 的替代品，是 SEO 在 AI 搜索时代的延伸。**

| | SEO | GEO |
|---|---|---|
| 目标引擎 | Google、百度 | DeepSeek、豆包、ChatGPT |
| 输出 | 链接列表 | 直接回答 + 引用 |
| 排名因子 | 外链、关键词、权重 | 语义匹配、权威信号、时效 |
| 优化对象 | 页面排名 | 品牌在 AI 回答中的被引用概率 |
| 衡量指标 | CTR、排名 | 品牌提及率、引用位置、情感倾向 |

## 技术实现优先级

1. **robots.txt** — 显式放行 AI 爬虫，加 Content-Signal 声明
2. **JSON-LD 结构化数据** — Organization + knowsAbout、FAQPage、Article
3. **llms.txt** — Markdown 站点索引，AI 爬虫发现内容的入口
4. **sitemap.xml** — 确保 AI 爬虫能找到所有页面
5. **语义 HTML** — 清晰标题层级、无 JS 渲染依赖
6. **跨平台实体锚定** — [Wikidata Q140135398](https://www.wikidata.org/wiki/Q140135398)、GitHub、知乎 profile 一致性

## 相关资源

- [Schema.org](https://schema.org) — 结构化数据标准
- [llms.txt 规范](https://llmstxs.org/)
- [Princeton KDD 2024 GEO 论文](https://arxiv.org/abs/2311.09735) — Cite Sources +115%、Statistics +40%
- [ICLR 2026 AutoGEO](https://arxiv.org/abs/2502.01959) — 自动学习生成引擎偏好

## 维护

由 [妮斯特科技 (Nister-sys)](https://promptmin.cn) 维护 — 中国企业 AI 搜索可见度优化服务商。

- 官网：[promptmin.cn](https://promptmin.cn)
- Wikidata：[Q140135398](https://www.wikidata.org/wiki/Q140135398)

MIT License.
