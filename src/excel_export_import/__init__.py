from models import Path

__author__ = 'darvin'
import xlwt

HEADER_STYLE = xlwt.easyxf("font: bold true")

def _get_field_option(field, option_name):
    if issubclass(field.__class__, dict):
        if option_name in field:
            return field[option_name]
    return None

def _get_headers_for_sheetscheme(sheet_scheme, scheme):
    result = ["id"]
    for field in sheet_scheme["Fields"]:
        field_path = _get_field_option(field, "Path") or field
        field_path = field_path.replace("/", "/SubElements/")

        result.append(_get_field_option(field, "Name") or Path.from_string(sheet_scheme["Path"]+"/*/"+field_path).get(scheme)["Description"].get())
    return result


def _export_sheet(data, sheet_scheme, scheme, ws):
    for i, field in enumerate(_get_headers_for_sheetscheme(sheet_scheme, scheme)):
        ws.write(0, i, field, HEADER_STYLE)


    for row, item_data in enumerate(Path.from_string(sheet_scheme["Path"]).get(data).values()):
        ws.write(row+1,0, item_data.name)
        for col, field in enumerate(sheet_scheme["Fields"]):
            field_path = _get_field_option(field, "Path") or field
            cell_data = Path.from_string(field_path).get(item_data)
            ws.write(row+1,col+1, cell_data.get())



    

def export_to_excel(data, scheme, filename):
    wb = xlwt.Workbook()
    export_scheme = scheme.get_meta().dump()["excel_scheme"]
    for sheet_name, sheet_scheme in export_scheme["sheets"].iteritems():
        ws = wb.add_sheet(sheet_name)
        _export_sheet(data, sheet_scheme, scheme, ws)

    wb.save(filename)


def import_from_excel(scheme, filename):
    pass