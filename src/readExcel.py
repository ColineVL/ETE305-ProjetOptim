from openpyxl import load_workbook

wb = load_workbook("./data/donnees optim sujet interco.xlsx")
sheetNord = wb[wb.sheetnames[1]]
sheetSud = wb[wb.sheetnames[2]]

consoNord = [cell.value for cell in sheetNord["B"]]
prodSolaireNord = [cell.value for cell in sheetNord["C"]]

consoSud = [cell.value for cell in sheetSud["B"]]
prodSolaireSud = [cell.value for cell in sheetSud["C"]]
prodEolienSud = [cell.value for cell in sheetSud["D"]]
prodHydroSud = [cell.value for cell in sheetSud["E"]]
prodBioenergiesSud = [cell.value for cell in sheetSud["F"]]

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
