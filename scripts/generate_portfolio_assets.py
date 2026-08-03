from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ASSET_DIR = ROOT / "assets" / "portfolio"
SOURCE_ENV_VAR = "PORTFOLIO_ASSET_SOURCE_DIR"


def split_lines(text: str, width: int) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        chunks = wrap(raw, width=width, break_long_words=True, break_on_hyphens=False)
        lines.extend(chunks or [""])
    return lines


def svg_document(
    *,
    title: str,
    subtitle: str,
    panels: list[dict[str, object]],
    footer: str,
) -> str:
    width = 1200
    height = 900
    panel_width = 540 if len(panels) == 2 else 1100
    panel_positions = [(60, 210), (600, 210)] if len(panels) == 2 else [(50, 210)]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0%" stop-color="#f5fbfa"/>',
        '<stop offset="100%" stop-color="#eef5fb"/>',
        "</linearGradient>",
        "</defs>",
        '<rect width="1200" height="900" fill="url(#bg)"/>',
        '<rect x="36" y="32" width="1128" height="836" rx="30" fill="#ffffff" stroke="#d7e5eb" stroke-width="2"/>',
        '<text x="72" y="94" font-size="18" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#3f7f88">制作実績・サンプル</text>',
        f'<text x="72" y="148" font-size="36" font-weight="700" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#16353b">{escape(title)}</text>',
        f'<text x="72" y="184" font-size="19" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#5d7078">{escape(subtitle)}</text>',
    ]

    for index, panel in enumerate(panels):
        x, y = panel_positions[index]
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="{panel_width}" height="520" rx="24" fill="#fcfefe" stroke="#dbe8ed" stroke-width="2"/>',
                f'<rect x="{x}" y="{y}" width="{panel_width}" height="54" rx="24" fill="#ebf6f8"/>',
                f'<circle cx="{x + 28}" cy="{y + 28}" r="6" fill="#9fc8cf"/>',
                f'<circle cx="{x + 48}" cy="{y + 28}" r="6" fill="#9fc8cf"/>',
                f'<circle cx="{x + 68}" cy="{y + 28}" r="6" fill="#9fc8cf"/>',
                f'<text x="{x + 92}" y="{y + 36}" font-size="20" font-weight="600" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#27474d">{escape(str(panel["heading"]))}</text>',
            ]
        )

        lines = split_lines(str(panel["body"]), width=26 if len(panels) == 2 else 62)
        start_y = y + 98
        for line in lines[:12]:
            parts.append(
                f'<text x="{x + 28}" y="{start_y}" font-size="22" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#34454d">{escape(line)}</text>'
            )
            start_y += 38

        if "highlight" in panel:
            parts.extend(
                [
                    f'<rect x="{x + 24}" y="{y + 396}" width="{panel_width - 48}" height="90" rx="20" fill="#f4faf6" stroke="#c9e2cf" />',
                    f'<text x="{x + 40}" y="{y + 432}" font-size="20" font-weight="700" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#2c5b41">{escape(str(panel["highlight"]))}</text>',
                ]
            )

            highlight_lines = split_lines(str(panel.get("highlight_body", "")), width=27 if len(panels) == 2 else 62)
            hy = y + 462
            for line in highlight_lines[:2]:
                parts.append(
                    f'<text x="{x + 40}" y="{hy}" font-size="18" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#4f6763">{escape(line)}</text>'
                )
                hy += 24

    parts.extend(
        [
            '<rect x="72" y="790" width="1056" height="44" rx="18" fill="#eff6f8"/>',
            f'<text x="92" y="818" font-size="18" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#51656c">{escape(footer)}</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts)


def svg_instagram(drugs: list[str], footer: str) -> str:
    width = 1200
    height = 900
    positions = [
        (66, 220),
        (280, 220),
        (494, 220),
        (708, 220),
        (922, 220),
    ]
    colors = ["#e5f6f5", "#edf4fd", "#f8efe2", "#eef8eb", "#f8edf3"]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '<rect width="1200" height="900" fill="#f8fbfd"/>',
        '<rect x="36" y="32" width="1128" height="836" rx="30" fill="#ffffff" stroke="#d9e6eb" stroke-width="2"/>',
        '<text x="72" y="94" font-size="18" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#3f7f88">制作実績・サンプル</text>',
        '<text x="72" y="146" font-size="36" font-weight="700" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#16353b">看護師向け 眼科薬剤Instagram投稿制作</text>',
        '<text x="72" y="184" font-size="19" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#5d7078">薬剤名がすぐ確認できる投稿構成と、看護視点の要点整理を両立したサンプルプレビュー</text>',
    ]

    for i, (x, y) in enumerate(positions):
        color = colors[i % len(colors)]
        title = drugs[i]
        lines = split_lines(title, 12)
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="190" height="420" rx="26" fill="#ffffff" stroke="#d9e6eb" stroke-width="2"/>',
                f'<rect x="{x+12}" y="{y+12}" width="166" height="72" rx="18" fill="{color}"/>',
                f'<circle cx="{x+34}" cy="{y+48}" r="13" fill="#9bc7d0"/>',
                f'<text x="{x+56}" y="{y+54}" font-size="16" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#43626a">Instagram投稿</text>',
                f'<rect x="{x+12}" y="{y+98}" width="166" height="184" rx="18" fill="#f7fbfc" stroke="#e0ebef"/>',
                f'<polygon points="{x+78},{y+160} {x+78},{y+220} {x+128},{y+190}" fill="#5ca7b2"/>',
                f'<text x="{x+26}" y="{y+320}" font-size="15" font-weight="700" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#2b474d">薬剤名</text>',
            ]
        )

        ly = y + 348
        for line in lines[:4]:
            parts.append(
                f'<text x="{x+26}" y="{ly}" font-size="14" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#3d4f56">{escape(line)}</text>'
            )
            ly += 24

        for j in range(3):
            parts.append(
                f'<rect x="{x+24}" y="{y+ly - y + 28 + j * 24}" width="{120 - j * 14}" height="10" rx="5" fill="#d8e6ea"/>'
            )

    parts.extend(
        [
            '<rect x="72" y="696" width="1056" height="108" rx="24" fill="#eef6f8"/>',
            '<text x="96" y="736" font-size="22" font-weight="700" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#28464d">代表5本のプレビュー</text>',
            '<text x="96" y="772" font-size="18" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#50636b">キサラタン / ルミガン / ベガモックス / PA・ヨード / サンテゾーン を掲載。薬剤名の視認性と短時間で要点がつかめる構成を重視しています。</text>',
            f'<text x="96" y="804" font-size="16" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#62757c">{escape(footer)}</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts)


def svg_spreadsheet() -> str:
    width = 1200
    height = 900
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '<rect width="1200" height="900" fill="#f7fbfd"/>',
        '<rect x="36" y="32" width="1128" height="836" rx="30" fill="#ffffff" stroke="#d7e5eb" stroke-width="2"/>',
        '<text x="72" y="94" font-size="18" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#3f7f88">制作実績・サンプル</text>',
        '<text x="72" y="146" font-size="36" font-weight="700" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#16353b">クリニック向け 点検表・チェックリスト整備</text>',
        '<text x="72" y="184" font-size="19" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#5d7078">点検漏れや引き継ぎ漏れを防ぎやすいように、使い方と記録欄を整理した公開用サンプル</text>',
        '<rect x="70" y="222" width="410" height="500" rx="22" fill="#fcfefe" stroke="#dbe8ed" stroke-width="2"/>',
        '<rect x="70" y="222" width="410" height="58" rx="22" fill="#eef6f8"/>',
        '<text x="94" y="258" font-size="22" font-weight="700" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#28464d">表紙_使い方</text>',
        '<text x="96" y="320" font-size="20" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#36474f">1. シートごとの役割がひと目で分かる構成</text>',
        '<text x="96" y="362" font-size="20" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#36474f">2. 点検記録の書き方を冒頭で案内</text>',
        '<text x="96" y="404" font-size="20" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#36474f">3. 月次・日次の使い分けを整理</text>',
        '<text x="96" y="446" font-size="20" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#36474f">4. 引き継ぎ時に迷いにくい見出し設計</text>',
        '<rect x="96" y="502" width="352" height="156" rx="18" fill="#f5faf3" stroke="#d7e6d2"/>',
        '<text x="120" y="546" font-size="20" font-weight="700" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#30553d">掲載候補シート</text>',
        '<text x="120" y="584" font-size="18" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#51656c">・ 緊急セット点検表</text>',
        '<text x="120" y="616" font-size="18" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#51656c">・ AED点検表</text>',
        '<text x="120" y="648" font-size="18" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#51656c">・ 向精神薬_残数チェック表</text>',
    ]

    # Right-hand spreadsheet table
    x0 = 530
    y0 = 222
    col_widths = [140, 180, 110, 110, 120]
    row_height = 48
    headers = ["項目", "確認内容", "頻度", "担当", "記録"]
    rows = [
        ["緊急セット", "数量・期限を確認", "毎月", "看護師", "□"],
        ["AED", "バッテリー表示・備品", "毎月", "受付", "□"],
        ["向精神薬", "残数・施錠を確認", "毎日", "管理者", "□"],
        ["水交換", "交換日・実施者", "定期", "スタッフ", "□"],
        ["備考", "引き継ぎ内容を記録", "-", "-", "記入"],
    ]
    total_width = sum(col_widths)
    parts.append(f'<rect x="{x0}" y="{y0}" width="{total_width}" height="500" rx="22" fill="#fcfefe" stroke="#dbe8ed" stroke-width="2"/>')
    parts.append(f'<rect x="{x0}" y="{y0}" width="{total_width}" height="{row_height}" rx="22" fill="#eef6f8"/>')
    xx = x0
    for i, header in enumerate(headers):
        parts.append(f'<text x="{xx+14}" y="{y0+31}" font-size="18" font-weight="700" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#28464d">{escape(header)}</text>')
        xx += col_widths[i]
        if i < len(headers) - 1:
            parts.append(f'<line x1="{xx}" y1="{y0}" x2="{xx}" y2="{y0+500}" stroke="#d8e6ea"/>')
    for r, row in enumerate(rows, start=1):
        y = y0 + r * row_height
        fill = "#ffffff" if r % 2 else "#f9fcfd"
        parts.append(f'<rect x="{x0}" y="{y}" width="{total_width}" height="{row_height}" fill="{fill}"/>')
        parts.append(f'<line x1="{x0}" y1="{y}" x2="{x0+total_width}" y2="{y}" stroke="#d8e6ea"/>')
        xx = x0
        for i, cell in enumerate(row):
            parts.append(f'<text x="{xx+14}" y="{y+30}" font-size="16" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#3d4f56">{escape(cell)}</text>')
            xx += col_widths[i]
    parts.extend(
        [
            '<rect x="72" y="770" width="1056" height="44" rx="18" fill="#eff6f8"/>',
            '<text x="92" y="798" font-size="18" font-family="Segoe UI, Yu Gothic UI, sans-serif" fill="#51656c">公開用に再構成したサンプルです。実在の施設情報・患者情報は含みません。</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts)


def validate_source_dir(source_dir: Path) -> None:
    required_paths = [
        source_dir
        / "02_網膜剥離手術後の過ごし方説明資料"
        / "網膜剥離手術後の過ごし方説明資料.docx",
        source_dir
        / "03_クリニック向け_電子付箋運用マニュアル"
        / "クリニック向け_電子付箋運用マニュアル.jpg",
    ]
    missing = [path for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Required portfolio source files were not found. "
            "Run with --source-dir pointing to the prepared source directory."
        )


def create_assets(source_dir: Path, asset_dir: Path = DEFAULT_ASSET_DIR) -> None:
    source_dir = source_dir.expanduser().resolve()
    asset_dir = asset_dir.resolve()
    validate_source_dir(source_dir)
    asset_dir.mkdir(parents=True, exist_ok=True)

    surgery_panels = [
        {
            "heading": "手術後の通院予定",
            "body": "\n".join(
                [
                    "1. 手術後の診察、通院予定",
                    "※ 手術当日と翌日（午前中）、手術2日後、手術1週間後以後",
                    "  状況により通院が必要となります。",
                    "",
                    "4. 手術当日、翌日は眼帯をするため、",
                    "   付き添いの方が必要になります。",
                    "6. 手術翌日より日中・就寝時に保護メガネを使用します。",
                ]
            ),
            "highlight": "生活上の注意点",
            "highlight_body": "洗顔・洗髪・化粧の制限や、仕事・運動の調整が必要な場面を見返しやすく整理。",
        },
        {
            "heading": "眼の清拭方法",
            "body": "\n".join(
                [
                    "1. 手術した方の眼から始める",
                    "2. 消毒用コットンをふんわり二つ折りにして、",
                    "   目頭から目尻に向かって優しく拭く",
                    "4. 下の睫毛の生え際を拭く",
                    "5. 目頭をコットンの角で眼の外に向かって拭く",
                    "6. 目尻も同様に拭く",
                ]
            ),
            "highlight": "付き添い・保護メガネ・清拭方法",
            "highlight_body": "ご家族が説明を見返しやすいように、処置後の具体的な行動へ落とし込んだ構成。",
        },
    ]
    (asset_dir / "01-ophthalmic-surgery-guide.svg").write_text(
        svg_document(
            title="眼科手術を受ける方へのご案内資料",
            subtitle="患者さんとご家族が術後の過ごし方を見返しやすいように再構成した公開用サンプル",
            panels=surgery_panels,
            footer="一部内容を匿名化・再構成しています。実在情報・患者情報は含みません。",
        ),
        encoding="utf-8",
    )

    doc = Document(
        source_dir
        / "02_網膜剥離手術後の過ごし方説明資料"
        / "網膜剥離手術後の過ごし方説明資料.docx"
    )
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    body_left = "\n".join(paragraphs[:8])
    body_right = "\n".join(paragraphs[8:16]) if len(paragraphs) > 8 else "\n".join(paragraphs[:8])

    (asset_dir / "02-retinal-detachment-aftercare.svg").write_text(
        svg_document(
            title="網膜剥離手術後の過ごし方説明資料",
            subtitle="体位制限や生活上の注意点を、自宅でも確認しやすい流れに整理した公開用サンプル",
            panels=[
                {
                    "heading": "うつむき姿勢が必要な理由",
                    "body": body_left,
                    "highlight": "患者さんが知りたいポイント",
                    "highlight_body": "うつむき姿勢の期間、注意事項、つらくなったときの工夫まで一続きで確認できる構成。",
                },
                {
                    "heading": "姿勢保持の工夫",
                    "body": body_right,
                    "highlight": "生活場面に沿った説明",
                    "highlight_body": "うつむき姿勢枕の作り方など、退院後にそのまま見返せる粒度でまとめています。",
                },
            ],
            footer="一部内容を匿名化・再構成しています。実際の対応は医師・医療機関の指示に従ってください。",
        ),
        encoding="utf-8",
    )

    shutil.copy2(
        source_dir
        / "03_クリニック向け_電子付箋運用マニュアル"
        / "クリニック向け_電子付箋運用マニュアル.jpg",
        asset_dir / "03-digital-sticky-note-manual.jpg",
    )

    (asset_dir / "04-ophthalmic-medicine-instagram.svg").write_text(
        svg_instagram(
            [
                "キサラタン 点眼液0.005%",
                "ルミガン 点眼液0.03%",
                "ベガモックス 点眼液0.5%",
                "PA・ヨード 点眼・洗眼液",
                "サンテゾーン 0.05%眼軟膏",
            ],
            "掲載許可確認済みの制作物をもとに、薬剤名と投稿構成が伝わる形で再構成したプレビューです。",
        ),
        encoding="utf-8",
    )

    (asset_dir / "05-checklist-maintenance.svg").write_text(
        svg_spreadsheet(),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate portfolio preview assets from a prepared source directory."
    )
    parser.add_argument(
        "--source-dir",
        default=os.environ.get(SOURCE_ENV_VAR),
        help=f"Prepared source directory. Can also be set with {SOURCE_ENV_VAR}.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_ASSET_DIR,
        help="Output directory for generated portfolio assets.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not args.source_dir:
        raise SystemExit(
            "Source directory is required. "
            'Run with --source-dir "<source-directory>".'
        )
    create_assets(Path(args.source_dir), args.output_dir)
