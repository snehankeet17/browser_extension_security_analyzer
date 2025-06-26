import os
from permission_rater import rate_permissions
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def detect_red_flags(perms):
    red_flags = []
    flagged = ["<all_urls>", "webRequest", "webRequestBlocking", "cookies", "history", "clipboardWrite"]
    for perm in perms:
        if perm in flagged:
            red_flags.append(perm)
    return red_flags

#  def export_pdf_report(extensions, filename="sample_output/report.pdf"):
    # os.makedirs(os.path.dirname(filename), exist_ok=True)

    # c = canvas.Canvas(filename, pagesize=A4)
    # width, height = A4
    # y = height - 40

    # c.setFont("Helvetica-Bold", 14)
    # c.drawString(40, y, "Browser Extension Security Analyzer Report")
    # y -= 30

    # for ext in extensions:
    #     if y < 100:
    #         c.showPage()
    #         y = height - 40

    #     c.setFont("Helvetica-Bold", 12)
    #     c.drawString(40, y, f"Extension: {ext['name']} (ID: {ext['id']})")
    #     y -= 20
    #     c.setFont("Helvetica", 10)
    #     c.drawString(60, y, f"Version: {ext['version']}")
    #     y -= 15

    #     combined = ext['permissions'] + ext.get("host_permissions", [])
    #     risks = rate_permissions(combined)
    #     red_flags = detect_red_flags(combined)

    #     # ✅ Calculate risk score
    #     score = (len(risks["High"]) * 5) + (len(risks["Medium"]) * 3) + (len(risks["Low"]) * 1) + (len(risks["Unknown"]) * 2)
    #     c.drawString(60, y, f"📊 Risk Score: {score}")
    #     y -= 15

    #     for level in ["High", "Medium", "Low", "Unknown"]:
    #         if risks[level]:
    #             c.drawString(60, y, f"{level} Risk: {', '.join(risks[level])}")
    #             y -= 15

    #     if red_flags:
    #         c.drawString(60, y, f"⚠️ Privacy Red Flags: {', '.join(red_flags)}")
    #         y -= 15

    #     y -= 10  # space between extensions

    # c.save()
    # print(f"\n✅ PDF report with Risk Score saved as '{filename}'")
def export_pdf_report(extensions, filename="sample_output/report.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Browser Extension Security Analyzer Report")
    y -= 30

    for ext in extensions:
        if y < 100:
            c.showPage()
            y = height - 40

        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, f"Extension: {ext['name']} (ID: {ext['id']})")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(60, y, f"Version: {ext['version']}")
        y -= 15

        combined = ext['permissions'] + ext.get("host_permissions", [])
        risks = rate_permissions(combined)
        red_flags = detect_red_flags(combined)

        # ✅ Calculate risk score
        score = (len(risks["High"]) * 5) + (len(risks["Medium"]) * 3) + (len(risks["Low"]) * 1) + (len(risks["Unknown"]) * 2)
        c.drawString(60, y, f"📊 Risk Score: {score}")
        y -= 15

        for level in ["High", "Medium", "Low", "Unknown"]:
            if risks[level]:
                c.drawString(60, y, f"{level} Risk: {', '.join(risks[level])}")
                y -= 15

        if red_flags:
            c.drawString(60, y, f"⚠️ Privacy Red Flags: {', '.join(red_flags)}")
            y -= 15

        y -= 10  # space between extensions
        
        if red_flags:
            c.drawString(60, y, f"⚠️ Privacy Red Flags: {', '.join(red_flags)}")
            y -= 15

            for flag in red_flags:
                if flag in permission_mitigation:
                    advice = permission_mitigation[flag]
                    c.drawString(80, y, f"🛡️ Mitigation: {advice}")
                    y -= 15

        permission_mitigation = {
    "<all_urls>": "Avoid extensions with full web access unless highly trusted.",
    "webRequest": "Used for intercepting traffic. Only enable if necessary.",
    "cookies": "Could expose sensitive sessions. Use only with trusted extensions.",
    "clipboardWrite": "May modify clipboard data. Ensure extension is essential.",
    "tabs": "Allows tab tracking. Prefer extensions that don’t require this.",
    "history": "Avoid unless the extension needs to access browsing history."
}

    c.save()
    print(f"\n✅ PDF report with Risk Score saved as '{filename}'")
