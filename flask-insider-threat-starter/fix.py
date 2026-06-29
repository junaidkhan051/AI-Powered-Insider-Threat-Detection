import re
import os

base_dir = r"c:/Users/CC/Downloads/flask-insider-threat-starter (3)/flask-insider-threat-starter"
html_file = os.path.join(base_dir, "templates", "landing.html")

with open(html_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace all requestAnimationFrame(funcName) with setTimeout(funcName, 1000/120)
content = re.sub(
    r"requestAnimationFrame\s*\(\s*(animateExplosion|loopGlobe|loopAiCore|loopWorkflow|drawDbg|drawDcGlobe|animateHex|drawOrbit|loopSilhouette)\s*\)",
    r"setTimeout(\1, 1000 / 120)",
    content
)

# For masterAnimationLoop, replace it carefully
content = re.sub(
    r"masterRafId = requestAnimationFrame\(masterAnimationLoop\);",
    r"masterRafId = setTimeout(masterAnimationLoop, 1000 / 120);",
    content
)

# Inject scroll lag fix at the start of the first script block
injection = """
let isScrolling = false;
let scrollTimeout = null;
window.addEventListener('scroll', () => {
    isScrolling = true;
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => { isScrolling = false; }, 100);
}, { passive: true });
const origSetTimeout = window.setTimeout;
window.setTimeout = function(cb, delay) {
    if (delay > 8 && delay < 9 && isScrolling) { // ~8.33ms for 120fps
        return origSetTimeout(cb, 100); // Throttle heavily during scroll
    }
    return origSetTimeout(cb, delay);
};
"""
if "let isScrolling = false;" not in content:
    content = content.replace("<script>", f"<script>\n{injection}\n", 1)

with open(html_file, "w", encoding="utf-8") as f:
    f.write(content)

print("HTML updated.")

css_file = os.path.join(base_dir, "static", "css", "style.css")
with open(css_file, "r", encoding="utf-8") as f:
    css = f.read()

if "scroll-behavior: smooth;" not in css:
    css = css.replace(":root {", "html, body { scroll-behavior: smooth; }\n\n:root {", 1)

with open(css_file, "w", encoding="utf-8") as f:
    f.write(css)

print("CSS updated.")
