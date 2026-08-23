#!/usr/bin/env python3
"""生成 templates/index.json —— 模板库的机器可读索引（stdlib only，无第三方依赖）。

为什么要这份文件：模板现在只有 markdown，站点靠 generate_pages.py glob 出来，
外部消费方（agency-orchestrator 的创意库、build.html 生成器、任何想接的人）
拿不到结构化数据，只能自己写 markdown parser —— 每接一个就重写一遍。

产出的每条包含：
    id / kind(genre|module) / lang / title / category / description
    variables[]  开拍前要定义的变量（从"先定义变量"表里抽）
    prompt       「完整提示词」小节的原始 markdown（保留分段结构，别压成一行）
    source       对应的公开页地址
    license / author

用法：python3 scripts/gen_index.py
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://prompts.aiolaola.com"
OUT = os.path.join(ROOT, "templates", "index.json")

# 「构件」不是题材模板，是可复用零件（运镜库、氛围骨架、负面词、多镜规划…）。
# 混进题材列表会让人困惑：他想拍猫，列表里冒出来一条"运镜技法库 50 式"。
MODULES = {
    "camera-move-library", "atmosphere-prefabs", "negative-prompts",
    "genre-camera-sop", "multi-shot-narrative", "project-planner",
}

# 分类：按"用户要拍什么"分，不按技法分。
CATEGORY = {
    "animal-vlog": "萌宠", "pet-lifetime-narrative": "萌宠", "elderly-cat-companion": "萌宠",
    "product-commercial": "广告 / 产品", "car-commercial": "广告 / 产品",
    "travel-vlog": "旅行 / 风光", "nature-timelapse": "旅行 / 风光", "drone-fpv": "旅行 / 风光",
    "micro-drama": "剧情 / 短剧", "movie-trailer": "剧情 / 短剧",
    "found-footage-horror": "剧情 / 短剧", "family-recipe-farewell": "剧情 / 短剧",
    "fashion-film": "时尚 / 美妆",
    "sci-fi-space": "科幻 / 动作", "cyberpunk-city": "科幻 / 动作", "anime-to-real": "科幻 / 动作",
    "15s-transformation": "科幻 / 动作", "sports-slowmo": "科幻 / 动作",
    "food-asmr": "美食",
    "music-video": "音乐 / 舞蹈", "dance": "音乐 / 舞蹈",
    "claymation": "风格化",
}

# 小节名有六七种写法：「先定义这些变量」「开拍前要先定义的变量」「先把变量定下来」…
# 所以只认「标题里出现"变量"」，别要求它结尾（travel-vlog 那条就是"先把变量定下来"）
VAR_HEADING = re.compile(r"^##\s+.*(?:变量|variable).*$", re.M | re.I)
# 小节名各文件略有出入：多数写「完整提示词（可直接复制）」，15s-transformation 写的是「模板正文」
# 英文侧写法是 "The complete prompt (copy-paste ready)" / "Template body"，
# 中文侧是「完整提示词（可直接复制）」「模板正文」——只认关键词，别锚死整句
PROMPT_HEADING = re.compile(r"^##\s+(?:.*完整提示词|.*模板正文|.*complete prompt|.*full prompt|.*template body|template)", re.M | re.I)
ANY_H2 = re.compile(r"^##\s+", re.M)


def section(md: str, heading_re: re.Pattern) -> str:
    """取某个 ## 小节的正文（到下一个 ## 为止）。找不到返回空串。"""
    m = heading_re.search(md)
    if not m:
        return ""
    start = md.index("\n", m.end()) + 1 if "\n" in md[m.end():] else len(md)
    nxt = ANY_H2.search(md, start)
    return md[start:nxt.start() if nxt else len(md)].strip()


def parse_variables(block: str) -> list:
    """从变量表里抽 {name, example}。表头形态各文件略有差异，只认第一列是 `{{x}}` 或 `x` 的行。"""
    out = []
    for line in block.split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or set(cells[0]) <= set("-: "):
            continue
        name = re.sub(r"[`{}]", "", cells[0]).strip()
        if not name or name in ("变量", "Variable", "项"):
            continue
        # 变量名应当是标识符样式；表头/说明行会被这一条挡掉
        if not re.fullmatch(r"[A-Za-z0-9_一-龥\- ]{1,40}", name):
            continue
        out.append({"name": name, "example": cells[1]})
    return out


def first_paragraph(md: str) -> str:
    """标题后的第一段引用块（模板都用 > 开头写定位），去掉引用符与换行。"""
    body = md.split("\n", 1)[1] if "\n" in md else ""
    quote = []
    for line in body.split("\n"):
        s = line.strip()
        if s.startswith(">"):
            quote.append(s.lstrip("> ").strip())
        elif quote:
            break
    text = " ".join(quote)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)      # 去链接
    text = re.sub(r"[*_`]", "", text)
    return text[:200].strip()


def build() -> None:
    items = []
    for path in sorted(glob.glob(os.path.join(ROOT, "templates", "*.md"))):
        rel = os.path.relpath(path, ROOT)
        base = os.path.basename(path)
        lang = "zh" if base.endswith(".zh.md") else "en"
        slug = base[:-6] if lang == "zh" else base[:-3]
        md = open(path, encoding="utf-8").read()
        title_m = re.match(r"^#\s+(.+)", md)
        prompt = section(md, PROMPT_HEADING)
        kind = "module" if slug in MODULES else "genre"
        items.append({
            "id": slug,
            "kind": kind,
            "lang": lang,
            "title": (title_m.group(1).strip() if title_m else slug),
            "category": CATEGORY.get(slug, "构件" if kind == "module" else "其他"),
            "description": first_paragraph(md),
            "variables": parse_variables(section(md, VAR_HEADING)),
            "prompt": prompt,
            "hasPrompt": bool(prompt),
            "source": f"{SITE}/p/{slug}.zh.html" if lang == "zh" else f"{SITE}/p/{slug}.html",
            "file": rel,
            "license": "MIT",
            "author": "jnMetaCode",
        })

    data = {
        "version": 1,
        "note": "机器可读索引，由 scripts/gen_index.py 生成，勿手改。"
                "kind=genre 是题材模板，kind=module 是可复用构件（运镜/氛围/负面词/多镜规划）。",
        "count": len(items),
        "templates": items,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    zh = [i for i in items if i["lang"] == "zh"]
    print(f"✅ {OUT}")
    print(f"   共 {len(items)} 条（中文 {len(zh)}；题材 {sum(1 for i in zh if i['kind']=='genre')}、"
          f"构件 {sum(1 for i in zh if i['kind']=='module')}）")
    miss = [i["id"] for i in zh if i["kind"] == "genre" and not i["hasPrompt"]]
    if miss:
        print(f"   ⚠️ 这些题材模板没抽到「完整提示词」小节，消费方拿不到可复制内容：{', '.join(miss)}")
    uncat = [i["id"] for i in zh if i["category"] == "其他"]
    if uncat:
        print(f"   ⚠️ 未归类（会落到「其他」）：{', '.join(uncat)}")


if __name__ == "__main__":
    build()
