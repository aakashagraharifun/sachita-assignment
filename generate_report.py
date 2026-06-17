"""Generate the CET138 Assignment 1 concepts report as a PDF.

Pulls code snippets directly from index.html, style.css and script.js
in this same directory, so the report always reflects the real project.
"""

from pathlib import Path

from reportlab.lib.colors import HexColor, black
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)

HERE = Path(__file__).parent
OUTPUT = HERE / "CET138_Assignment1_Report.pdf"

ACCENT = HexColor("#d33c15")
TEXT = HexColor("#111111")
MUTED = HexColor("#555555")
CODE_BG = HexColor("#f4f1ec")


# ---------------------------------------------------------------------------
# Helpers to pull real snippets out of the source files
# ---------------------------------------------------------------------------

def read_lines(filename: str) -> list[str]:
    return (HERE / filename).read_text(encoding="utf-8").splitlines()


def extract(filename: str, start_marker: str, end_marker: str,
            include_end: bool = False) -> str:
    """Return the slice between the first line containing start_marker
    and the first line after it containing end_marker."""
    lines = read_lines(filename)
    start = next(i for i, ln in enumerate(lines) if start_marker in ln)
    end = next(i for i, ln in enumerate(lines[start + 1:], start + 1)
               if end_marker in ln)
    if include_end:
        end += 1
    snippet = lines[start:end]
    # Trim shared left indentation so the snippet looks tidy in the PDF
    non_empty = [ln for ln in snippet if ln.strip()]
    if non_empty:
        common = min(len(ln) - len(ln.lstrip()) for ln in non_empty)
        snippet = [ln[common:] if len(ln) >= common else ln for ln in snippet]
    return "\n".join(snippet).rstrip()


# ---------------------------------------------------------------------------
# Build the report
# ---------------------------------------------------------------------------

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=26, leading=32, textColor=TEXT, spaceAfter=6, alignment=TA_LEFT,
)
subtitle_style = ParagraphStyle(
    "Subtitle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=12, leading=16, textColor=MUTED, spaceAfter=24,
)
section_style = ParagraphStyle(
    "Section", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=18, leading=22, textColor=ACCENT, spaceBefore=12, spaceAfter=10,
)
subhead_style = ParagraphStyle(
    "SubHead", parent=styles["Heading3"], fontName="Helvetica-Bold",
    fontSize=12, leading=16, textColor=TEXT, spaceBefore=10, spaceAfter=4,
)
body_style = ParagraphStyle(
    "Body", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=11, leading=16, textColor=TEXT, spaceAfter=8,
)
code_style = ParagraphStyle(
    "Code", parent=styles["Code"], fontName="Courier",
    fontSize=8.5, leading=11, textColor=TEXT,
    backColor=CODE_BG, borderPadding=8,
    leftIndent=0, rightIndent=0, spaceBefore=4, spaceAfter=8,
)


def section(story, number, title, intro, what_built, code, explanation, why):
    story.append(Paragraph(f"{number}. {title}", section_style))
    story.append(Paragraph(intro, body_style))

    story.append(Paragraph("What I built", subhead_style))
    story.append(Paragraph(what_built, body_style))

    story.append(Paragraph("Code from the project", subhead_style))
    story.append(Preformatted(code, code_style))

    story.append(Paragraph("What the code does", subhead_style))
    story.append(Paragraph(explanation, body_style))

    story.append(Paragraph("Why I did it this way", subhead_style))
    story.append(Paragraph(why, body_style))
    story.append(Spacer(1, 0.4 * cm))


def build():
    story = []

    # --- Cover ---
    story.append(Paragraph("CET138 Assignment 1 — Concepts Report", title_style))
    story.append(Paragraph(
        "A walk-through of the Full Stack, HTML, CSS, Bootstrap and JavaScript "
        "concepts used in the <b>Eventide</b> Event Booking website, with code "
        "pulled straight from the project files.",
        subtitle_style,
    ))

    # =====================================================================
    # 1. Full Stack Development
    # =====================================================================
    fullstack_code = extract("script.js",
                             "form.addEventListener('submit'",
                             "confirmModal.show();", include_end=True)
    section(
        story,
        1,
        "Full Stack Development",
        intro=(
            "Full stack development just means a developer can work on both "
            "halves of a website. The <b>front-end</b> is everything you see "
            "and click — built with HTML, CSS and JavaScript and running in "
            "your browser. The <b>back-end</b> is the server-side bit that "
            "handles logins, processes data and talks to a <b>database</b>, "
            "which is where information is actually stored long term. The "
            "three pieces talk to each other over an API: the browser sends a "
            "request, the server runs some logic and asks the database for "
            "what it needs, then sends an answer back."
        ),
        what_built=(
            "This project is front-end only — there is no real server. The "
            "<b>booking form</b> is the part that would talk to a back-end in a "
            "production version: a Node/Express API would receive the booking, "
            "validate it, store the record in a database like MongoDB or MySQL, "
            "and email a confirmation. For the assignment, JavaScript fakes "
            "that last step by showing a confirmation modal."
        ),
        code=fullstack_code,
        explanation=(
            "<b>preventDefault()</b> stops the browser from doing its usual "
            "full-page reload on submit, so the JavaScript can take over. The "
            "next few lines collect the values the user typed in — name, "
            "email, event, quantity — exactly the kind of payload a real API "
            "would receive. The <b>if</b> block does basic client-side "
            "validation so we don't try to confirm an empty booking. In a real "
            "full stack version, the next step would be a <code>fetch()</code> "
            "call sending this data to a server endpoint; here, the modal "
            "stands in for that response."
        ),
        why=(
            "Splitting validation between the browser and the server is "
            "standard practice — the front-end catches obvious mistakes "
            "quickly, and the back-end does the proper, trusted check before "
            "anything ever reaches a database."
        ),
    )
    story.append(PageBreak())

    # =====================================================================
    # 2. HTML
    # =====================================================================
    html_code = extract("index.html",
                        "<header>",
                        "</header>", include_end=True)
    section(
        story,
        2,
        "HTML",
        intro=(
            "HTML is the layer that gives a webpage its structure. It is not a "
            "programming language — there are no loops or calculations — it "
            "just labels each chunk of content so the browser knows what it "
            "is. Modern HTML5 also gives us <b>semantic tags</b> like "
            "<code>&lt;header&gt;</code>, <code>&lt;nav&gt;</code>, "
            "<code>&lt;main&gt;</code> and <code>&lt;footer&gt;</code>, which "
            "describe the role of each section. This matters for "
            "accessibility (screen readers can navigate the page properly) "
            "and for SEO (Google understands the page layout better)."
        ),
        what_built=(
            "The whole Eventide page uses semantic tags rather than a wall of "
            "<code>&lt;div&gt;</code>s. The top of the page is wrapped in "
            "<code>&lt;header&gt;</code>, the main listing in "
            "<code>&lt;main&gt;</code>, each event in its own "
            "<code>&lt;article&gt;</code>, and the bottom in "
            "<code>&lt;footer&gt;</code>."
        ),
        code=html_code,
        explanation=(
            "The outer <code>&lt;header&gt;</code> groups everything at the "
            "top of the page — the site-wide <code>&lt;nav&gt;</code> bar "
            "and the hero <code>&lt;section&gt;</code> with the welcome "
            "message and call-to-action. Using a real "
            "<code>&lt;nav&gt;</code> rather than a generic "
            "<code>&lt;div&gt;</code> tells screen readers \"this is the "
            "site navigation\", and the four <code>&lt;a&gt;</code> tags "
            "inside the unordered list jump to the matching sections of the "
            "page using their <code>id</code> attributes as anchors."
        ),
        why=(
            "Semantic HTML costs nothing extra to write and makes the site "
            "more accessible and easier for search engines to index — it is "
            "the modern default for good reason."
        ),
    )
    story.append(PageBreak())

    # =====================================================================
    # 3. CSS
    # =====================================================================
    css_code = extract("style.css", ":root {", "}", include_end=True)
    section(
        story,
        3,
        "CSS",
        intro=(
            "CSS — Cascading Style Sheets — is what makes a page actually "
            "look like something. HTML lays the bones down; CSS picks the "
            "colours, fonts, spacing and layout. <b>CSS variables</b> "
            "(properties defined with <code>--name</code> inside "
            "<code>:root</code>) let you define a value once and reuse it "
            "everywhere, so updating the whole theme is a one-line change."
        ),
        what_built=(
            "The whole Eventide colour palette and spacing scale lives in a "
            "single <code>:root</code> block at the top of "
            "<code>style.css</code>. The rest of the stylesheet pulls those "
            "values in with <code>var(--name)</code>, so anything from the "
            "hero banner to the booking form picks up the same accent red and "
            "rounded corners."
        ),
        code=css_code,
        explanation=(
            "<code>:root</code> is the top of the CSS tree — variables "
            "defined here are available to every element on the page. "
            "<code>--bg</code> and <code>--surface</code> are the two main "
            "background tones, <code>--accent</code> is the brand red used on "
            "buttons and hover states, and the <code>--space-*</code> values "
            "give a consistent rhythm so padding looks the same across "
            "sections. The <code>--radius</code> and <code>--shadow</code> "
            "variables keep card corners and drop shadows uniform."
        ),
        why=(
            "Without variables, swapping the accent colour later would mean "
            "hunting through the whole stylesheet — with them, it's a "
            "one-line change that the rest of the site picks up "
            "automatically."
        ),
    )
    story.append(PageBreak())

    # =====================================================================
    # 4. Bootstrap
    # =====================================================================
    bootstrap_code = extract("index.html",
                             "<nav class=\"navbar",
                             "</nav>", include_end=True)
    section(
        story,
        4,
        "Bootstrap",
        intro=(
            "Bootstrap is a CSS framework that gives you ready-made, "
            "responsive components — navbars, grids, forms, modals — out of "
            "the box. Instead of writing media queries and layout maths "
            "yourself, you drop classes like <code>col-md-6</code> onto your "
            "HTML and Bootstrap handles the rest, including how things "
            "rearrange on phones."
        ),
        what_built=(
            "Bootstrap powers the Eventide <b>navbar with mobile hamburger "
            "collapse</b>, the <b>responsive 3-column event grid</b> that "
            "stacks on small screens, the <b>booking form layout</b> "
            "(<code>col-md-6</code> fields side by side), and the "
            "<b>confirmation modal</b>."
        ),
        code=bootstrap_code,
        explanation=(
            "<code>navbar-expand-lg</code> tells Bootstrap to keep the menu "
            "expanded on large screens and collapse it on smaller ones. The "
            "<code>navbar-toggler</code> button is the hamburger that appears "
            "on mobile — its <code>data-bs-toggle=\"collapse\"</code> and "
            "<code>data-bs-target=\"#mainNav\"</code> attributes wire it up "
            "to the menu without any JavaScript I have to write. Inside the "
            "collapsible <code>div</code>, the four nav links use "
            "<code>nav-link</code> classes so they pick up Bootstrap's "
            "default styling on top of my own overrides in CSS."
        ),
        why=(
            "Writing a fully accessible, responsive navbar from scratch is a "
            "lot of work — Bootstrap solves it in a handful of classes, which "
            "lets me focus on the bits of the site that are actually "
            "specific to Eventide."
        ),
    )
    story.append(PageBreak())

    # =====================================================================
    # 5. JavaScript
    # =====================================================================
    js_code = extract("script.js",
                      "searchInput.addEventListener('input'",
                      "noResults.classList.toggle", include_end=True)
    # Close the missing brace so the snippet reads cleanly
    if not js_code.rstrip().endswith("});"):
        js_code += "\n  });"

    section(
        story,
        5,
        "JavaScript",
        intro=(
            "JavaScript is what makes a webpage actually <i>do</i> things. "
            "HTML and CSS only describe what's on screen; JavaScript reacts "
            "to clicks, key presses and form submissions, updates the page "
            "without reloading, and can talk to a back-end over the network. "
            "It works by listening for <b>events</b> and then changing the "
            "<b>DOM</b> — the live tree of elements the browser is showing."
        ),
        what_built=(
            "Two of the most interactive bits of Eventide are pure "
            "JavaScript: the <b>live search filter</b> that hides and shows "
            "event cards as you type, and the <b>live total price</b> in the "
            "booking form that updates the moment you change the quantity or "
            "the event. The booking modal is also built dynamically — its "
            "summary HTML is generated by JavaScript at the point of submit."
        ),
        code=js_code,
        explanation=(
            "<code>addEventListener('input', ...)</code> fires on every "
            "keystroke, so the filter feels instant. Inside, I lowercase the "
            "search term once, then loop through every event card and check "
            "whether its <code>data-name</code> attribute contains the term. "
            "Cards that match stay visible; non-matches have their column "
            "parent's <code>display</code> set to <code>none</code> so the "
            "grid re-flows neatly. A small counter tracks how many cards are "
            "still visible, and a Bootstrap <code>d-none</code> class is "
            "toggled on a \"no results\" message accordingly."
        ),
        why=(
            "Filtering on the front-end is fine here because the dataset is "
            "tiny — six cards. For thousands of events I'd send the search "
            "term to a server and let the database do the filtering instead, "
            "which is much more efficient at scale."
        ),
    )

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="CET138 Assignment 1 — Concepts Report",
    )
    doc.build(story)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
