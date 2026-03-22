from pathlib import Path
import shutil, DB, configparser

def copyAndRename():
    pathTex = Path("../LM_latex")

    # get last modified file from LM_ref
    latestFile = max(Path("../LM_ref/").iterdir(), key=lambda f: f.stat().st_mtime)

    companyNames = DB.getCompanies("companyName", "parsedFile")

    config = configparser.ConfigParser()
    config.read('config.ini')
    firstName = config.get('GENERAL', 'firstName')
    lastName = config.get('GENERAL', 'lastName')
    
    for companyName in companyNames:
            newFileName = f"LM_{firstName}_{lastName}_{companyName}{latestFile.suffix}"
            destination = pathTex / newFileName
            shutil.copy2(latestFile, destination)

            with open(destination, "r", encoding="utf-8") as f:
                content = f.read()
            content = content.replace("[CompanyName]", companyName)
            with open(destination, "w", encoding="utf-8") as f:
                f.write(content)
    
    DB.updateDatabase("parsedFile")