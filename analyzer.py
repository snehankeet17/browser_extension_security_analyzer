import os
import json
from permission_rater import rate_permissions
from report_generator import print_report

def find_profiles(chrome_profile_path):
    profiles = []
    for name in os.listdir(chrome_profile_path):
        full_path = os.path.join(chrome_profile_path, name)
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
            except Exception as e:
                print(f"[!] Could not read {manifest_path}: {e}")
    return extensions

if __name__ == "__main__":
    chrome_path = input("Enter Chrome user data path (e.g., C:\\Users\\YOU\\AppData\\Local\\Google\\Chrome\\User Data): ").strip()

    print("\n🔍 Scanning for Chrome profiles...")
    profiles = find_profiles(chrome_path)

    if not profiles:
        print("❌ No valid Chrome profiles with Extensions folder found.")
    else:
        print("✅ Found profiles:")
        for i, p in enumerate(profiles):
            print(f"  [{i}] {p}")

        choice = int(input("Select profile number: "))
        selected_profile = os.path.join(chrome_path, profiles[choice])

        extensions = list_extensions(selected_profile)
        print_report(extensions)


# C:\Users\sneha\AppData\Local\Google\Chrome\User Data ---path of the chrome data