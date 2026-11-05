"""
עיצוב כהה בסגנון אפליקציית צ'אט:
רקע כהה עם משושים זוהרים, פס עליון עם זוהר כתום,
בועות מעוגלות ותיבת כתיבה כהה.
"""

from urllib.parse import quote


# ---------- רקע: משושים זוהרים עדינים ----------
def build_wallpaper():
    r = 26
    w = 3 ** 0.5 * r

    def hexagon(cx, cy):
        points = [
            (cx, cy - r), (cx + w / 2, cy - r / 2), (cx + w / 2, cy + r / 2),
            (cx, cy + r), (cx - w / 2, cy + r / 2), (cx - w / 2, cy - r / 2),
        ]
        text = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        return f'<polygon points="{text}" fill="none" stroke="#2a3142" stroke-width="1.5"/>'

    shapes = [
        hexagon(w / 2, r),
        hexagon(0, 2.5 * r), hexagon(w, 2.5 * r),
        hexagon(0, -0.5 * r), hexagon(w, -0.5 * r),
    ]
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.1f}" height="{3 * r}">'
        + "".join(shapes)
        + "</svg>"
    )
    return "data:image/svg+xml," + quote(svg)


WALLPAPER = build_wallpaper()

# ---------- הפס העליון ----------
HEADER = """
<div class="top-bar">
    <div class="avatar">🎲</div>
    <div class="info">
        <div class="name">בוט חוקי קטאן</div>
        <div class="status"><span class="dot"></span>מחובר · עונה לפי ספר החוקים של משחק קטאן</div>
    </div>
</div>
"""

# ---------- עיצוב (CSS) ----------
CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&display=swap');

/* צבעי הבסיס של Gradio, בגרסה כהה */
.gradio-container {{
    --body-background-fill: #0d1017;
    --background-fill-primary: #141823;
    --background-fill-secondary: #1b2030;
    --block-background-fill: transparent;
    --block-border-color: transparent;
    --input-background-fill: #1b2030;
    --body-text-color: #e8e6e3;
    --body-text-color-subdued: #9aa3b5;
    --border-color-primary: #2a3142;

    max-width: 820px !important;
    margin: 0 auto !important;
    padding: 12px !important;
    font-family: 'Rubik', sans-serif !important;
    background-color: #0d1017 !important;
    background-image:
        radial-gradient(circle at 50% 0%, rgba(249, 115, 22, 0.18), transparent 60%),
        url("{WALLPAPER}") !important;
}}

body, html {{
    background: #0d1017 !important;
}}

footer {{
    display: none !important;
}}

/* הפס העליון */
.top-bar {{
    direction: rtl;
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 18px;
    border-radius: 22px;
    background: rgba(27, 32, 48, 0.85);
    border: 1px solid rgba(249, 115, 22, 0.5);
    box-shadow: 0 0 24px rgba(249, 115, 22, 0.25), 0 8px 24px rgba(0, 0, 0, 0.5);
    color: #f5f5f4;
}}

.avatar {{
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f97316, #b91c1c);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    box-shadow: 0 0 16px rgba(249, 115, 22, 0.7);
    animation: wobble 4s ease-in-out infinite;
}}

@keyframes wobble {{
    0%, 85%, 100% {{ transform: rotate(0); }}
    90% {{ transform: rotate(-20deg) scale(1.1); }}
    95% {{ transform: rotate(20deg) scale(1.1); }}
}}

.info {{
    flex: 1;
}}

.name {{
    font-weight: 700;
    font-size: 1.3rem;
    background: linear-gradient(90deg, #fdba74, #f97316);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}

.status {{
    font-size: 0.85rem;
    color: #9aa3b5;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 8px #4ade80;
    animation: pulse 2s infinite;
}}

@keyframes pulse {{
    50% {{ opacity: 0.35; }}
}}

.resources {{
    font-size: 1.2rem;
    letter-spacing: 4px;
}}

/* אזור ההודעות */
.catan-chat {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

.catan-chat [data-testid="user"] {{
    background: linear-gradient(135deg, #f97316, #c2410c) !important;
    color: white !important;
    border: none !important;
    border-radius: 20px 20px 6px 20px !important;
    box-shadow: 0 4px 14px rgba(249, 115, 22, 0.35);
}}

.catan-chat [data-testid="bot"] {{
    background: #1b2030 !important;
    color: #e8e6e3 !important;
    border: 1px solid #2a3142 !important;
    border-radius: 20px 20px 20px 6px !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
}}

/* תיבת הכתיבה */
.catan-input {{
    background: #1b2030 !important;
    border: 1px solid rgba(249, 115, 22, 0.6) !important;
    border-radius: 999px !important;
    box-shadow: 0 0 18px rgba(249, 115, 22, 0.15);
}}

.catan-input textarea {{
    background: transparent !important;
    color: #f5f5f4 !important;
    font-size: 1rem !important;
}}

.catan-input textarea::placeholder {{
    color: #7c8597 !important;
}}

.gradio-container button {{
    color: #e8e6e3 !important;
}}

.gradio-container button.primary {{
    background: linear-gradient(135deg, #f97316, #c2410c) !important;
    border: none !important;
    border-radius: 999px !important;
    color: white !important;
    box-shadow: 0 0 12px rgba(249, 115, 22, 0.5);
}}
"""