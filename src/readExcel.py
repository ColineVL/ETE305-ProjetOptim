from openpyxl import load_workbook

wb = load_workbook("./data/donnees optim sujet interco.xlsx")
sheetNord = wb[wb.sheetnames[1]]
sheetSud = wb[wb.sheetnames[2]]

nbHeures = len(sheetNord["B"])
# nbHeures = 24 * 30  # 1 mois

consoNord = [float(cell.value) for cell in sheetNord["B"][1:nbHeures]]
prodSolaireNord = [float(cell.value) for cell in sheetNord["C"][1:nbHeures]]

consoSud = [float(cell.value) for cell in sheetSud["B"][1:nbHeures]]
prodSolaireSud = [float(cell.value) for cell in sheetSud["C"][1:nbHeures]]
prodEolienSud = [float(cell.value) for cell in sheetSud["D"][1:nbHeures]]
prodHydroSud = [float(cell.value) for cell in sheetSud["E"][1:nbHeures]]
prodBioenergiesSud = [float(cell.value) for cell in sheetSud["F"][1:nbHeures]]

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
