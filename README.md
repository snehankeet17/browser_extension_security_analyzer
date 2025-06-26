 # 🔐 Browser Extension Security Analyzer

## 📌 Overview
This tool is developed as part of the **Deltaware Internship** project. It analyzes the installed Google Chrome extensions on a user's system, evaluates the permissions each extension uses, and flags potential **privacy** or **data-leak risks**.

## 🛠 Features
- ✅ Lists installed browser extensions from Chrome.
- ✅ Analyzes `permissions` and `host_permissions` from each `manifest.json`.
- ✅ Rates permissions by risk level: High, Medium, Low, Unknown.
- ✅ Flags potentially dangerous or privacy-invading permissions.
- ✅ (Optional) Exports analysis as a **PDF report**.
- ✅ CLI-based — no external GUI required.

## 📁 File Structure

browser-extension-analyzer/
├── analyzer.py # Main script
├── permission_rater.py # Risk rating for permissions
├── report_generator.py # Report formatting and PDF export
├── sample_output/
│ └── sample_report.pdf # Example output
├── requirements.txt
└── README.md
