from pprint import pprint
import xlrd
from models import Path, StructuredNode, Node
from widgets import NodeWidget

__author__ = 'darvin'
import xlwt

HEADER_STYLE = xlwt.easyxf("font: bold true")
ID_FIELD = "%id_field%"

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
    export_scheme = scheme.get_meta().dump()["ExcelScheme"]
    for sheet_name, sheet_scheme in export_scheme["Sheets"].iteritems():
        ws = wb.add_sheet(sheet_name)
        _export_sheet(data, sheet_scheme, scheme, ws)

    wb.save(filename)


def _get_sheet_by_name(wb, sheet_name):
    for sheet in wb.sheets():
        if sheet.name.startswith(sheet_name):
            return sheet
    raise KeyError


def import_from_excel(scheme, filename):
    export_scheme = scheme.get_meta().dump()["ExcelScheme"]
    rb = xlrd.open_workbook(filename)
    result = StructuredNode({})
    for sheet_name, sheet_scheme in export_scheme["Sheets"].iteritems():
        sheet = _get_sheet_by_name(rb, sheet_name)
        for rownum in range(1,sheet.nrows):
            row = sheet.row_values(rownum)
            current_id = None
            for field, cell_data in zip([ID_FIELD] + sheet_scheme["Fields"], row):
                if field==ID_FIELD:
                    current_id = cell_data
                else:
                    field_path = _get_field_option(field, "Path") or field
                    full_field_path = "/{}/{}/{}".format(sheet_scheme["Path"], current_id, field_path)
                    full_scheme_field_path = "/{}/{}/{}".format(sheet_scheme["Path"], current_id, field_path.replace("/", "/SubElements/"))
                    path = Path.from_string(full_field_path)
                    field_scheme = Path.from_string(full_scheme_field_path).get(scheme)
                    path.set(result, NodeWidget.get_data_class(field_scheme)(cell_data))
    pprint(result)
    return result.dump()
            
            