import os

def initialize():
    pathBdd = "../bdd"
    pathCV = "../CV"
    pathPDF = "../LM_PDF"
    pathLMRef = "../LM_ref"
    pathLMLatex = "../LM_latex"

    if not os.path.exists(pathBdd):
        os.makedirs(pathBdd)
    if not os.path.exists(pathCV):
        os.makedirs(pathCV)
    if not os.path.exists(pathPDF):
        os.makedirs(pathPDF)
    if not os.path.exists(pathLMRef):
        os.makedirs(pathLMRef)
    if not os.path.exists(pathLMLatex):
        os.makedirs(pathLMLatex)