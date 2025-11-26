import pypdf
import sys

pdf_path = "/Users/neha/Architecting-Professional-Grade-Multi-Agent-Systems-with-LangGraph/Multi-Agent Systems Roadmap Upgrade.pdf"
output_path = "/Users/neha/Architecting-Professional-Grade-Multi-Agent-Systems-with-LangGraph/pdf_content.txt"

try:
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    with open(output_path, "w") as f:
        f.write(text)
    print(f"Successfully wrote content to {output_path}")
except Exception as e:
    print(f"Error reading PDF: {e}", file=sys.stderr)
