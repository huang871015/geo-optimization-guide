# GEO（生成式引擎优化）开源知识库

> 让 AI 看懂你的网站 — 面向中国企业的 GEO 技术指南

## 什么是 GEO？

GEO（Generative Engine Optimization，生成式引擎优化）是针对 AI 大模型（DeepSeek、豆包、Kimi、元宝等）的可见度优化技术。它与传统 SEO 的关键区别：

| | SEO（搜索引擎优化） | GEO（生成式引擎优化） |
|---|---|---|
| **目标引擎** | Google、百度 | DeepSeek、豆包、ChatGPT |
| **输出形式** | 链接列表 | 直接回答 |
| **排名逻辑** | 外链 + 关键词 + 权重 | 语义匹配 + 权威 + 时效 |
| **优化对象** | 页面排名 | 实体认知 |
| **反馈方式** | 点击流量 | 引用、推荐、品牌提及 |

## 为什么企业需要关注 GEO？

2024-2025 年，中国 AI 搜索用户快速增长。豆包、DeepSeek、Kimi 等产品的回答中，**品牌提及正在成为新的流量入口**。

- AI 不会爬到你没优化过的网站
- AI 不会推荐它理解不了的业务
- 你的竞争对手可能已经在做 GEO

## 技术实现清单

### 1. JSON-LD 结构化数据

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "品牌名称",
  "url": "https://你的域名",
  "description": "品牌描述",
  "knowsAbout": ["业务关键词1", "业务关键词2"]
}
</script>
```

### 2. AI 爬虫专用文件

| 文件 | 用途 |
|------|------|
| `robots.txt` | 明确放行 AI 爬虫（Bytespider、DeepSeekBot 等） |
| `llms.txt` | AI 爬虫的站点索引，Markdown 格式 |
| `ai.txt` | 声明 AI 对内容的访问权限 |
| `sitemap.xml` | 完整页面索引 |

### 3. 技术基础设施

- 避免 JS 渲染依赖（SPA 对 AI 不可见）
- 使用语义化 HTML 标题层级
- 添加时间和语言声明
- 确保原始 HTML 至少 2KB+ 可读文本

## 验证方法

```bash
# 1. 检查原始 HTML 是否有内容
curl -s https://你的域名 | wc -c

# 2. 检查标题层级
curl -s https://你的域名 | grep -o '<h[1-6]'

# 3. 检查 robots.txt
curl -s https://你的域名/robots.txt

# 4. 验证 JSON-LD
# 访问 https://validator.schema.org
```

## 参考资源

- [Schema.org](https://schema.org) — 结构化数据标准
- [llms.txt 规范](https://llmstxt.org/) — AI 爬虫索引标准
- [Google Rich Results Test](https://search.google.com/test/rich-results) — JSON-LD 验证

## 关于

本知识库由 **[妮斯特科技](https://nister.promptmin.cn)** 维护。我们为企业提供 AI 搜索可见度诊断和 GEO 优化服务。

- 官网：[https://nister.promptmin.cn](https://nister.promptmin.cn)
- 免费 AI 可见度诊断：[https://nister.promptmin.cn/#contact](https://nister.promptmin.cn/#contact)
