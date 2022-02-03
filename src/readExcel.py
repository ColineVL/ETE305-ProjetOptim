from openpyxl import load_workbook

wb = load_workbook("./data/donnees optim sujet interco.xlsx")
sheetNord = wb[wb.sheetnames[1]]
sheetSud = wb[wb.sheetnames[2]]


consoNord = [float(cell.value) for cell in sheetNord["B"][1:]]
prodSolaireNord = [float(cell.value) for cell in sheetNord["C"][1:]]

consoSud = [float(cell.value) for cell in sheetSud["B"][1:]]
prodSolaireSud = [float(cell.value) for cell in sheetSud["C"][1:]]
prodEolienSud = [float(cell.value) for cell in sheetSud["D"][1:]]
prodHydroSud = [float(cell.value) for cell in sheetSud["E"][1:]]
prodBioenergiesSud = [float(cell.value) for cell in sheetSud["F"][1:]]

nbHeures = len(consoNord)

assert (
    len(consoNord)
    == len(prodSolaireNord)
    == len(consoSud)
    == len(prodSolaireSud)
    == len(prodEolienSud)
    == len(prodHydroSud)
    == len(prodBioenergiesSud)
)
