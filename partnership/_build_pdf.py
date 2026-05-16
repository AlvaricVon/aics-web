"""Convert markdown files to branded AICS PDFs."""
import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether
)

# ============ AICS BRAND COLORS ============
BG = HexColor("#FAFAF7")
SURFACE = HexColor("#FFFFFF")
SURFACE_ALT = HexColor("#F5F4F1")
TEXT = HexColor("#1C1917")
TEXT_SOFT = HexColor("#44403C")
MUTED = HexColor("#78716C")
BORDER = HexColor("#E7E5E4")
ACCENT = HexColor("#C2410C")
ACCENT_BG = HexColor("#FFF7ED")

# ============ STYLES ============
def make_styles():
    s = getSampleStyleSheet()

    title = ParagraphStyle(
        "AICSTitle", parent=s["Title"], fontName="Helvetica-Bold",
        fontSize=32, leading=38, textColor=TEXT, spaceAfter=20, spaceBefore=80
    )
    subtitle = ParagraphStyle(
        "AICSSubtitle", parent=s["Normal"], fontName="Helvetica",
        fontSize=14, leading=20, textColor=MUTED, spaceAfter=40, alignment=TA_LEFT
    )
    title_meta = ParagraphStyle(
        "AICSTitleMeta", parent=s["Normal"], fontName="Helvetica",
        fontSize=11, leading=16, textColor=TEXT_SOFT, spaceAfter=4
    )
    h1 = ParagraphStyle(
        "AICS_H1", parent=s["Heading1"], fontName="Helvetica-Bold",
        fontSize=22, leading=28, textColor=TEXT, spaceBefore=24, spaceAfter=14,
        keepWithNext=1
    )
    h2 = ParagraphStyle(
        "AICS_H2", parent=s["Heading2"], fontName="Helvetica-Bold",
        fontSize=16, leading=22, textColor=TEXT, spaceBefore=18, spaceAfter=10,
        keepWithNext=1
    )
    h3 = ParagraphStyle(
        "AICS_H3", parent=s["Heading3"], fontName="Helvetica-Bold",
        fontSize=12, leading=16, textColor=ACCENT, spaceBefore=12, spaceAfter=6,
        keepWithNext=1
    )
    body = ParagraphStyle(
        "AICSBody", parent=s["BodyText"], fontName="Helvetica",
        fontSize=10, leading=15, textColor=TEXT_SOFT, spaceAfter=8, alignment=TA_LEFT
    )
    bullet = ParagraphStyle(
        "AICSBullet", parent=body, leftIndent=18, bulletIndent=4, spaceAfter=4
    )
    code = ParagraphStyle(
        "AICSCode", parent=body, fontName="Courier", fontSize=8.5,
        textColor=TEXT, backColor=SURFACE_ALT,
        leftIndent=10, rightIndent=10, spaceAfter=8, spaceBefore=4,
        borderColor=BORDER, borderWidth=0.5, borderPadding=8, leading=12
    )
    quote = ParagraphStyle(
        "AICSQuote", parent=body, fontName="Helvetica-Oblique",
        textColor=MUTED, leftIndent=12, borderColor=ACCENT, borderWidth=0,
        spaceAfter=10
    )

    return dict(title=title, subtitle=subtitle, title_meta=title_meta,
                h1=h1, h2=h2, h3=h3, body=body, bullet=bullet, code=code, quote=quote)


# ============ MARKDOWN PARSER ============
def inline_md(text: str) -> str:
    """Convert markdown inline syntax to reportlab-supported HTML."""
    # Escape HTML special chars first (except those we'll convert)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Bold **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # Italic *text*
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", text)
    # Inline code `code`
    text = re.sub(r"`([^`]+?)`", r'<font face="Courier" backColor="#F5F4F1" color="#1C1917">\1</font>', text)
    # Links [text](url)
    text = re.sub(r"\[([^\]]+?)\]\(([^)]+?)\)", r'<link href="\2" color="#C2410C"><u>\1</u></link>', text)
    return text


def parse_table(lines, i):
    """Parse markdown table starting at line i. Returns (Table, next_i)."""
    # Header line
    header_cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
    # Separator line (skip)
    i += 2
    # Data rows
    rows = []
    while i < len(lines) and lines[i].strip().startswith("|"):
        row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        rows.append(row)
        i += 1

    # Build table data
    data = [[Paragraph(inline_md(c), ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=white, alignment=TA_LEFT)) for c in header_cells]]
    cell_style = ParagraphStyle("td", fontName="Helvetica", fontSize=9, textColor=TEXT_SOFT, leading=12, alignment=TA_LEFT)
    for r in rows:
        # Pad row to match header length
        while len(r) < len(header_cells):
            r.append("")
        data.append([Paragraph(inline_md(c), cell_style) for c in r[:len(header_cells)]])

    # Compute column widths — distribute evenly
    page_width = A4[0] - 4 * cm
    col_width = page_width / len(header_cells)
    col_widths = [col_width] * len(header_cells)

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0, 0), (-1, 0), TEXT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        # Alternating row colors
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [SURFACE, SURFACE_ALT]),
        # Borders
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, BORDER),
        # Padding
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return table, i


def parse_md(md_text: str, styles: dict, title: str, subtitle: str, meta_lines: list):
    """Convert markdown to list of reportlab flowables."""
    flowables = []

    # ===== Title Page =====
    # Brand badge
    brand_style = ParagraphStyle(
        "Brand", fontName="Helvetica-Bold", fontSize=14, textColor=TEXT,
        backColor=ACCENT_BG, borderColor=ACCENT, borderWidth=1, borderPadding=6,
        spaceAfter=4
    )
    flowables.append(Spacer(1, 6 * cm))
    flowables.append(Paragraph("AICS", ParagraphStyle("BrandLarge", fontName="Helvetica-Bold", fontSize=48, textColor=ACCENT, spaceAfter=4)))
    flowables.append(Paragraph("AI Customer Support untuk UMKM Indonesia", styles["title_meta"]))
    flowables.append(Spacer(1, 2 * cm))
    flowables.append(Paragraph(title, styles["title"]))
    flowables.append(Paragraph(subtitle, styles["subtitle"]))

    for line in meta_lines:
        flowables.append(Paragraph(line, styles["title_meta"]))

    flowables.append(PageBreak())

    # ===== Body =====
    lines = md_text.split("\n")
    i = 0
    in_code_block = False
    code_buffer = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Code blocks (```)
        if stripped.startswith("```"):
            if in_code_block:
                # End code block
                code_text = "\n".join(code_buffer)
                code_text = code_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                code_text = code_text.replace("\n", "<br/>")
                flowables.append(Paragraph(code_text, styles["code"]))
                code_buffer = []
                in_code_block = False
            else:
                in_code_block = True
            i += 1
            continue
        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        # Empty line
        if not stripped:
            i += 1
            continue

        # H1, H2, H3
        if stripped.startswith("### "):
            flowables.append(Paragraph(inline_md(stripped[4:]), styles["h3"]))
            i += 1
            continue
        if stripped.startswith("## "):
            flowables.append(Paragraph(inline_md(stripped[3:]), styles["h2"]))
            i += 1
            continue
        if stripped.startswith("# "):
            flowables.append(Paragraph(inline_md(stripped[2:]), styles["h1"]))
            i += 1
            continue

        # Horizontal rule
        if stripped in ("---", "***"):
            flowables.append(Spacer(1, 0.3 * cm))
            i += 1
            continue

        # Table
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[-:\s|]+\|$", lines[i + 1].strip()):
            table, i = parse_table(lines, i)
            flowables.append(table)
            flowables.append(Spacer(1, 0.4 * cm))
            continue

        # Bullet list
        if re.match(r"^[\-\*]\s+", stripped):
            text = re.sub(r"^[\-\*]\s+", "", stripped)
            flowables.append(Paragraph(f"• {inline_md(text)}", styles["bullet"]))
            i += 1
            continue

        # Numbered list
        if re.match(r"^\d+\.\s+", stripped):
            num_match = re.match(r"^(\d+)\.\s+(.+)$", stripped)
            if num_match:
                flowables.append(Paragraph(f"{num_match.group(1)}. {inline_md(num_match.group(2))}", styles["bullet"]))
                i += 1
                continue

        # Blockquote
        if stripped.startswith("> "):
            flowables.append(Paragraph(inline_md(stripped[2:]), styles["quote"]))
            i += 1
            continue

        # Checkbox list
        if re.match(r"^[\-\*]?\s*☐\s+", stripped):
            text = re.sub(r"^[\-\*]?\s*☐\s+", "☐ ", stripped)
            flowables.append(Paragraph(inline_md(text), styles["bullet"]))
            i += 1
            continue
        if re.match(r"^[\-\*]?\s*[✅✓]\s+", stripped):
            text = re.sub(r"^[\-\*]?\s*[✅✓]\s+", "✓ ", stripped)
            flowables.append(Paragraph(inline_md(text), styles["bullet"]))
            i += 1
            continue

        # Regular paragraph (may span multiple lines)
        para_lines = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,3}\s|[\-\*]\s|\d+\.\s|>\s|\|)", lines[i].strip()) and not lines[i].strip().startswith("```"):
            para_lines.append(lines[i].strip())
            i += 1
        para_text = " ".join(para_lines)
        flowables.append(Paragraph(inline_md(para_text), styles["body"]))

    return flowables


# ============ PAGE TEMPLATE (header/footer) ============
def make_canvas_callback(header_text: str):
    """Return a function that draws header + footer on each page."""
    def add_header_footer(canvas, doc):
        canvas.saveState()
        # Skip header/footer on title page (page 1)
        if doc.page == 1:
            canvas.restoreState()
            return

        # Header (top)
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(MUTED)
        canvas.drawString(2 * cm, A4[1] - 1.2 * cm, header_text)
        canvas.drawRightString(A4[0] - 2 * cm, A4[1] - 1.2 * cm, "aics-web.vercel.app")
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.4)
        canvas.line(2 * cm, A4[1] - 1.4 * cm, A4[0] - 2 * cm, A4[1] - 1.4 * cm)

        # Footer (bottom)
        canvas.setFillColor(MUTED)
        canvas.drawString(2 * cm, 1.2 * cm, "AICS · by Kamil Alfaris")
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
        canvas.line(2 * cm, 1.5 * cm, A4[0] - 2 * cm, 1.5 * cm)
        canvas.restoreState()
    return add_header_footer


# ============ MAIN ============
def build_pdf(md_path: str, pdf_path: str, title: str, subtitle: str, meta_lines: list, header: str):
    md = Path(md_path).read_text(encoding="utf-8")
    styles = make_styles()
    flowables = parse_md(md, styles, title, subtitle, meta_lines)

    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=title, author="Kamil Alfaris",
    )
    callback = make_canvas_callback(header)
    doc.build(flowables, onFirstPage=callback, onLaterPages=callback)
    print(f"Saved: {pdf_path}")


if __name__ == "__main__":
    base = Path("C:/Users/ASUS VIVOBOOK 15/aics-web/partnership")

    # 1. Project Brief
    build_pdf(
        md_path=str(base / "01_project_brief.md"),
        pdf_path=str(base / "01_project_brief.pdf"),
        title="Project Brief",
        subtitle="Onboarding document untuk Alvin Zaidan Faizal Putra",
        meta_lines=[
            "<b>Untuk:</b> Alvin Zaidan Faizal Putra (Growth Partner)",
            "<b>Dari:</b> Kamil Alfaris (Founder &amp; CEO)",
            "<b>Versi:</b> 1.0 · Mei 2026",
            "<b>Status:</b> Active — Day 1 launch",
        ],
        header="AICS · Project Brief"
    )

    # 2. Alvin Todo List
    build_pdf(
        md_path=str(base / "03_alvin_todo_list.md"),
        pdf_path=str(base / "03_alvin_todo_list.pdf"),
        title="Daily Routine & Marketing Playbook",
        subtitle="Untuk Alvin Zaidan Faizal Putra — Growth Partner @ AICS",
        meta_lines=[
            "<b>Total commitment:</b> 10-15 jam per minggu",
            "<b>Compensation:</b> Commission per customer (recurring 3 bulan)",
            "<b>Path to co-founder:</b> Bawa 5+ paying customer dalam 90 hari",
            "<b>Versi:</b> 1.0 · Mei 2026",
        ],
        header="AICS · Daily Routine & Marketing Playbook"
    )

    # 3. Lead Tracking Guide
    build_pdf(
        md_path=str(base / "02b_lead_tracking_guide.md"),
        pdf_path=str(base / "02b_lead_tracking_guide.pdf"),
        title="Lead Tracking Guide",
        subtitle="Setup &amp; cara pakai Excel/Google Sheet",
        meta_lines=[
            "<b>File:</b> 02_lead_tracking.xlsx",
            "<b>Format:</b> Excel (bisa import ke Google Sheet)",
            "<b>Update:</b> Daily oleh Alvin, weekly review oleh Kamil",
        ],
        header="AICS · Lead Tracking Guide"
    )

    print("\nAll 3 PDFs generated successfully.")
