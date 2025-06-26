import os
import json
import platform
import streamlit as st
from permission_rater import rate_permissions
from report_generator import export_pdf_report, detect_red_flags

# ✅ Determine if running on Streamlit Cloud
IS_CLOUD = platform.system() != "Windows"

# ✅ Optional: mitigation advice
permission_mitigation = {
    "<all_urls>": "Avoid extensions with full web access unless highly trusted.",
    "webRequest": "Only use extensions with this permission if necessary for security tools.",
    "cookies": "Use extensions that limit cookie access and review their privacy policy.",
    "tabs": "Prefer extensions that don’t need access to your browser tabs.",
    "history": "Avoid extensions that access history unless essential.",
    "identity": "Used for Google sign-in. Only allow from trusted sources.",
    "webview": "Used to embed content. Check for potential malicious injection.",
    "unlimitedStorage": "May consume large storage. Monitor suspicious behavior.",
    "clipboardWrite": "May modify clipboard. Allow only if the extension needs it.",
    "alarms": "Used for background tasks. Verify extension purpose.",
    "offscreen": "Can run tasks in background. Use with caution.",
    "https://docs.google.com/*": "Limit access to trusted extensions only.",
    "https://drive.google.com/*": "Restrict to productivity tools you trust.",
    "https://www.googleapis.com/*": "May access personal data. Confirm extension credibility.",
    "https://payments.google.com/*": "Ensure financial data is accessed only by secure extensions."
}

# ✅ Real Chrome profile support (for local use)
def find_profiles(chrome_user_data_path):
    profiles = []
    for name in os.listdir(chrome_user_data_path):
        full_path = os.path.join(chrome_user_data_path, name)
        if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, "Extensions")):
            profiles.append(name)
    return profiles

def list_extensions(profile_path):
    extensions_dir = os.path.join(profile_path, 'Extensions')
    extensions = []
    for ext_id in os.listdir(extensions_dir):
        ext_path = os.path.join(extensions_dir, ext_id)
        versions = os.listdir(ext_path)
        if versions:
            latest = sorted(versions)[-1]
            manifest_path = os.path.join(ext_path, latest, 'manifest.json')
            try:
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                    extensions.append({
                        "name": manifest.get("name", "N/A"),
                        "id": ext_id,
                        "version": manifest.get("version", "N/A"),
                        "permissions": manifest.get("permissions", []),
                        "host_permissions": manifest.get("host_permissions", [])
                    })
            except:
                pass
    return extensions

# ✅ Streamlit App
st.set_page_config(page_title="Browser Extension Security Analyzer", layout="centered")
st.title("🛡️ Browser Extension Security Analyzer")
st.write("Analyze Chrome extensions, check permissions, risk scores, and mitigation advice.")

# 🔁 Streamlit session state
if "extensions" not in st.session_state:
    st.session_state.extensions = []

# 🚫 Demo mode for Streamlit Cloud
if IS_CLOUD:
    st.warning("🚫 This cloud version cannot scan your Chrome. Showing demo data only.")
    st.session_state.extensions = [
        {
            "name": "MSG_extName",
            "id": "ghbmnnjooekpmoecnnnilnnbdlolhkhi",
            "version": "1.85.1",
            "permissions": ["storage", "alarms", "unlimitedStorage"],
            "host_permissions": ["https://docs.google.com/*", "https://drive.google.com/*"]
        },
        {
            "name": "MSG_APP_NAME",
            "id": "nmmhkkegccagdldgiimedpiccmgmieda",
            "version": "1.0.0.6",
            "permissions": ["identity", "webview"],
            "host_permissions": [
                "https://www.google.com/",
                "https://www.googleapis.com/*",
                "https://payments.google.com/payments/v4/js/integrator.js"
            ]
        }
    ]
else:
    chrome_path = st.text_input("📂 Enter Chrome User Data Path", value=r"C:\Users\YourName\AppData\Local\Google\Chrome\User Data")
    if chrome_path and os.path.exists(chrome_path):
        profiles = find_profiles(chrome_path)
        if profiles:
            selected_profile = st.selectbox("👤 Choose Chrome Profile", profiles)

            if st.button("🔍 Scan Extensions"):
                full_profile_path = os.path.join(chrome_path, selected_profile)
                st.session_state.extensions = list_extensions(full_profile_path)

# ✅ Show Extension Results
if st.session_state.extensions:
    for ext in st.session_state.extensions:
        st.subheader(f"🧩 {ext['name']} (v{ext['version']})")
        st.caption(f"Extension ID: `{ext['id']}`")

        combined = ext['permissions'] + ext.get("host_permissions", [])
        risks = rate_permissions(combined)
        red_flags = detect_red_flags(combined)

        score = (len(risks["High"]) * 5) + (len(risks["Medium"]) * 3) + (len(risks["Low"]) * 1) + (len(risks["Unknown"]) * 2)
        st.markdown(f"📊 **Risk Score:** `{score}`")

        for level in ["High", "Medium", "Low", "Unknown"]:
            if risks[level]:
                st.markdown(f"**{level} Risk Permissions:** `{', '.join(risks[level])}`")

        if red_flags:
            st.error(f"⚠️ Privacy Red Flags: {', '.join(red_flags)}")

        # ✅ Mitigation Advice
        mitigation_displayed = False
        for perm in combined:
            if perm in permission_mitigation:
                if not mitigation_displayed:
                    st.markdown("### 🛡️ How to Overcome the Risks:")
                    mitigation_displayed = True
                st.markdown(f"• **{perm}** → _{permission_mitigation[perm]}_")

# ✅ Generate PDF Report
if st.session_state.extensions and st.button("📄 Generate PDF Report"):
    output_path = os.path.join("sample_output", "report.pdf")
    export_pdf_report(st.session_state.extensions, filename=output_path)

    if os.path.exists(output_path):
        with open(output_path, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF Report",
                data=f,
                file_name="browser_extension_report.pdf",
                mime="application/pdf"
            )
    else:
        st.error("❌ Failed to generate PDF.")
