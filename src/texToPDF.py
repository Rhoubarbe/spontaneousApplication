from pathlib import Path
import subprocess, DB

def convertTexToPdf():
    tex_dir = Path("../LM_latex")
    pdf_dir = Path("../LM_PDF")

    # Create a file without raising an exception
    pdf_dir.mkdir(exist_ok=True)

    # Convert .tex to .pdf, launch pdflatex command
    for tex_file in tex_dir.glob("*.tex"):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-output-directory", str(pdf_dir), str(tex_file)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # allows you to delete unwanted files
    for f in pdf_dir.iterdir():
        if f.is_file() and f.suffix.lower() != ".pdf":
            f.unlink()

    # add YES to BDD
    DB.updateDatabase("converted")

