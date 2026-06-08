#!/usr/bin/env python3
"""geovis — AI Crawler Visibility Checker for Chinese & Global AI Platforms.

Single-file, zero-dependency tool. Checks if a domain is accessible to the AI
crawlers that power ChatGPT, DeepSeek, Doubao, Kimi, Perplexity, and more.

Usage:
    python geovis.py promptmin.cn
    python geovis.py example.com --json
"""

import json
import re
import sys
import urllib.request
import urllib.error
import ssl
from html.parser import HTMLParser

# ── AI crawler registry ──────────────────────────────────────────
CRAWLERS = {
    "Tier 1 — AI Search (visibility-critical)": [
        ("GPTBot", "OpenAI", "ChatGPT Search + training"),
        ("OAI-SearchBot", "OpenAI", "ChatGPT Search (no training)"),
        ("ChatGPT-User", "OpenAI", "User-initiated browsing"),
        ("ClaudeBot", "Anthropic", "Claude web search"),
        ("PerplexityBot", "Perplexity", "Perplexity search + citations"),
    ],
    "Tier 2 — Chinese AI Platforms": [
        ("Bytespider", "ByteDance", "Doubao / 豆包"),
        ("DeepSeekBot", "DeepSeek", "DeepSeek Chat"),
        ("MoonshotBot", "Moonshot AI", "Kimi"),
        ("YuanbaoBot", "Tencent", "元宝 / Yuanbao"),
        ("Baiduspider", "Baidu", "文心一言 / ERNIE Bot"),
    ],
    "Tier 3 — Broader Ecosystem": [
        ("GoogleOther", "Google", "Gemini + AI Overviews"),
        ("Google-Extended", "Google", "Gemini training (no rank impact)"),
        ("Applebot-Extended", "Apple", "Apple Intelligence"),
        ("Amazonbot", "Amazon", "Alexa + Amazon AI"),
        ("FacebookBot", "Meta", "Meta AI"),
    ],
}

DISCOVERY_FILES = [
    ("/robots.txt", "Robots exclusion"),
    ("/llms.txt", "AI crawler index (llms.txt standard)"),
    ("/sitemap.xml", "Primary sitemap"),
    ("/.well-known/ai.txt", "AI permissions declaration"),
]

JSON_LD_TYPES = [
    "Organization", "WebSite", "FAQPage", "Article",
    "Product", "LocalBusiness", "BreadcrumbList", "Service",
]


def fetch(url, timeout=10):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "geovis/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.read().decode("utf-8", errors="replace"), r.status
    except Exception as e:
        return None, str(e)


def check_robots_txt(domain, base_url):
    """Fetch robots.txt and check access for each crawler."""
    content, status = fetch(f"{base_url}/robots.txt")
    if content is None:
        return {"error": str(status)}, {}

    # Parse: for each User-agent block, collect rules
    blocks = {}
    current_agents = []
    for line in content.split("\n"):
        line = line.split("#")[0].strip()
        if not line:
            continue
        if line.lower().startswith("user-agent:"):
            agent = line.split(":", 1)[1].strip()
            current_agents = [agent]
            for a in current_agents:
                if a not in blocks:
                    blocks[a] = {"allow": [], "disallow": []}
        elif line.lower().startswith("allow:") and current_agents:
            path = line.split(":", 1)[1].strip()
            for a in current_agents:
                blocks.setdefault(a, {"allow": [], "disallow": []})["allow"].append(path)
        elif line.lower().startswith("disallow:") and current_agents:
            path = line.split(":", 1)[1].strip()
            for a in current_agents:
                blocks.setdefault(a, {"allow": [], "disallow": []})["disallow"].append(path)

    # Check Content-Signal
    content_signal = None
    for line in content.split("\n"):
        if line.lower().startswith("content-signal:"):
            content_signal = line.split(":", 1)[1].strip()
            break

    # Evaluate each crawler
    results = {}
    for tier, crawlers in CRAWLERS.items():
        for name, operator, purpose in crawlers:
            access = "not_mentioned"
            if name in blocks:
                rules = blocks[name]
                if "/" in rules["disallow"]:
                    access = "blocked"
                else:
                    access = "allowed"
            elif "*" in blocks:
                rules = blocks["*"]
                if "/" in rules["disallow"]:
                    access = "blocked"
                else:
                    access = "allowed"  # wildcard allows
            else:
                access = "allowed"  # no rules = allowed by default

            results[name] = {"operator": operator, "purpose": purpose,
                           "tier": tier, "access": access}

    robots_info = {"content_signal": content_signal, "sitemaps": []}
    for line in content.split("\n"):
        if line.lower().startswith("sitemap:"):
            robots_info["sitemaps"].append(line.split(":", 1)[1].strip())

    return robots_info, results


class SchemaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.schemas = []
        self.in_script = False
        self.script_type = None
        self.script_data = ""

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            attrs = dict(attrs)
            if attrs.get("type") == "application/ld+json":
                self.in_script = True
                self.script_type = "jsonld"

    def handle_endtag(self, tag):
        if tag == "script" and self.in_script:
            self.in_script = False
            try:
                data = json.loads(self.script_data)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    if isinstance(item, dict) and "@type" in item:
                        self.schemas.append(item)
            except json.JSONDecodeError:
                pass
            self.script_data = ""
            self.script_type = None

    def handle_data(self, data):
        if self.in_script:
            self.script_data += data


def check_page(domain, base_url):
    """Check homepage for JSON-LD, meta tags, content signals."""
    content, status = fetch(base_url)
    if content is None:
        return {"error": str(status)}, [], 0

    # Parse JSON-LD
    parser = SchemaParser()
    parser.feed(content)
    schemas = parser.schemas

    # Extract meta description
    meta_desc = ""
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content, re.I)
    if m:
        meta_desc = m.group(1)

    # Count Chinese text
    text = re.sub(r"<[^>]+>", " ", content)
    text = re.sub(r"\s+", " ", text).strip()
    cn_chars = len(re.findall(r"[一-鿿]", text))

    meta_info = {
        "title": "",
        "description": meta_desc,
        "chinese_chars": cn_chars,
        "has_h1": bool(re.search(r"<h1[>\s]", content, re.I)),
        "has_rss": bool(re.search(r'type="application/rss\+xml"', content, re.I)),
    }
    m = re.search(r"<title>([^<]+)</title>", content, re.I)
    if m:
        meta_info["title"] = m.group(1)

    return meta_info, schemas, cn_chars


def check_discovery_files(domain, base_url):
    """Check which AI discovery files exist."""
    results = {}
    for path, desc in DISCOVERY_FILES:
        _, status = fetch(f"{base_url}{path}", timeout=8)
        if isinstance(status, int) and status == 200:
            results[path] = "found"
        elif isinstance(status, int):
            results[path] = f"HTTP {status}"
        else:
            results[path] = "error"
    return results


def score(robots_results, discovery_info, schemas, meta_info):
    """Compute visibility score 0-100."""
    s = 0

    # Tier 1 crawlers (35 pts): 7 pts each
    tier1 = [n for n, d in robots_results.items()
             if d["tier"].startswith("Tier 1") and d["access"] == "allowed"]
    s += min(35, len(tier1) * 7)

    # Tier 2 Chinese crawlers (25 pts): 5 pts each
    tier2 = [n for n, d in robots_results.items()
             if d["tier"].startswith("Tier 2") and d["access"] == "allowed"]
    s += min(25, len(tier2) * 5)

    # Discovery files (20 pts): 5 pts each
    for path, status in discovery_info.items():
        if status == "found":
            s += 5

    # JSON-LD schemas (15 pts): 5 pts per meaningful type
    schema_types = set()
    for sc in schemas:
        t = sc.get("@type", "")
        if isinstance(t, list):
            schema_types.update(t)
        else:
            schema_types.add(t)
    meaningful = schema_types & set(JSON_LD_TYPES)
    s += min(15, len(meaningful) * 5)

    # Content quality (5 pts)
    if meta_info.get("chinese_chars", 0) >= 500:
        s += 3
    if meta_info.get("has_h1"):
        s += 1
    if meta_info.get("has_rss"):
        s += 1

    return min(100, s)


def report_text(domain, robots_info, robots_results, discovery_info,
                schemas, meta_info, final_score):
    """Format results as readable text."""
    out = []
    out.append(f"\n  {domain} AI Crawler Visibility Report")
    out.append(f"  {'─' * 50}")

    # Crawler access
    current_tier = ""
    for name, data in robots_results.items():
        if data["tier"] != current_tier:
            current_tier = data["tier"]
            out.append(f"\n  {current_tier}")
        icon = "✅" if data["access"] == "allowed" else ("❌" if data["access"] == "blocked" else "⬜")
        out.append(f"  {icon} {name:<22s} {data['operator']:<12s} {data['purpose']}")

    # Discovery files
    out.append(f"\n  Discovery Files")
    for path, status in discovery_info.items():
        icon = "✅" if status == "found" else "❌"
        out.append(f"  {icon} {path:<28s} {status}")

    # JSON-LD
    if schemas:
        types = set()
        for sc in schemas:
            t = sc.get("@type", "")
            if isinstance(t, list):
                types.update(t)
            else:
                types.add(t)
        out.append(f"\n  JSON-LD Types: {', '.join(sorted(types))}")
    else:
        out.append(f"\n  JSON-LD: ❌  None found")

    # Content
    out.append(f"\n  Content")
    out.append(f"  Chinese chars: {meta_info.get('chinese_chars', '?')}")
    out.append(f"  H1: {'✅' if meta_info.get('has_h1') else '❌'}")
    out.append(f"  RSS: {'✅' if meta_info.get('has_rss') else '❌'}")

    # Content-Signal
    if robots_info.get("content_signal"):
        out.append(f"\n  Content-Signal: {robots_info['content_signal']}")

    # Sitemaps
    if robots_info.get("sitemaps"):
        out.append(f"\n  Sitemaps in robots.txt: {len(robots_info['sitemaps'])}")

    # Score
    bar_len = 20
    filled = int(final_score / 100 * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)
    rating = "Excellent" if final_score >= 90 else ("Good" if final_score >= 75 else
              ("Fair" if final_score >= 60 else ("Poor" if final_score >= 40 else "Critical")))
    out.append(f"\n  AI Visibility Score: {final_score}/100  {bar}  {rating}")
    out.append("")

    return "\n".join(out)


def main():
    if len(sys.argv) < 2:
        print("Usage: python geovis.py <domain> [--json]")
        print("  python geovis.py promptmin.cn")
        print("  python geovis.py example.com --json")
        sys.exit(1)

    domain = sys.argv[1].rstrip("/")
    use_json = "--json" in sys.argv

    if "://" not in domain:
        base_url = f"https://{domain}"
    else:
        base_url = domain
        domain = domain.split("://")[1].split("/")[0]

    print(f"  Scanning {domain}...", file=sys.stderr)

    # 1. robots.txt
    robots_info, robots_results = check_robots_txt(domain, base_url)

    # 2. Discovery files
    discovery_info = check_discovery_files(domain, base_url)

    # 3. Homepage analysis
    meta_info, schemas, _ = check_page(domain, base_url)

    # 4. Score
    final_score = score(robots_results, discovery_info, schemas, meta_info)

    if use_json:
        output = {
            "domain": domain,
            "score": final_score,
            "crawlers": robots_results,
            "discovery_files": discovery_info,
            "jsonld_types": list(set(
                sc.get("@type", "") for sc in schemas
            )),
            "meta": meta_info,
            "robots_content_signal": robots_info.get("content_signal"),
            "robots_sitemaps": robots_info.get("sitemaps", []),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(report_text(domain, robots_info, robots_results,
                          discovery_info, schemas, meta_info, final_score))


if __name__ == "__main__":
    main()
