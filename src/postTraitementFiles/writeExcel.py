from openpyxl import Workbook
from datetime import datetime

from enums import ZoneName


def writeResultsInExcel(mesZones, nbHeures):
    wb = Workbook()
    timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")
    dest_filename = f"src/postTraitementFiles/results_{timestamp}.xlsx"

    ws1 = wb.active
    zone = mesZones[ZoneName.NORD]
    ws1.title = f"{zone.nom.name}_dispatchable"

    for h in range(nbHeures):
        ws1.append(
            [prod.solutionProduction[h] for prod in zone.producteursDispatchable]
        )

    # for row in range(1, 40):
    #     ws1.append(range(600))

    # ws2 = wb.create_sheet(title="Pi")
    # ws2["F5"] = 3.14
    # ws3 = wb.create_sheet(title="Data")
    # for row in range(10, 20):
    #     for col in range(27, 54):
    #         _ = ws3.cell(
    #             column=col, row=row, value="{0}".format(get_column_letter(col))
    #         )
    # print(ws3["AA10"].value)
    wb.save(filename=dest_filename)
