import xlrd
import xlwt
import copy
import json


class ColumnKey:
    def __init__(self, key, index=0, column=None):
        self.key = key
        if column is not None and column.strip() != "":
            self.column = column
        else:
            self.column = key
        self.index = index


class ExcelUtil:
    def __init__(self, simple_mode=True):
        self.simple_mode = simple_mode

    def list2excel_file(self, column_keys, data, name, sheet_name="Sheet1", path="../resources/excel/"):
        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建一个worksheet
        worksheet = workbook.add_sheet(sheet_name)
        for column_key in column_keys:
            if self.simple_mode:
                worksheet.write(0, column_key.index, label=column_key.column)
                for i in range(len(data)):
                    worksheet.write(i + 1, column_key.index, label=data[i][column_key.key])
            else:
                worksheet.write(0, column_key.index, label=column_key.column)
                for i in range(len(data)):
                    worksheet.write(i + 1, column_key.index, label=data[i][column_key.key])

        workbook.save(path + name + '.xls')

    @classmethod
    def excel_file2list(cls, column_keys, file_path, sheet_name=None, sheet_no=0):
        result_list = []
        wb = xlrd.open_workbook(file_path)
        if sheet_name is not None and sheet_name.strip() != "":
            sheet = wb.sheet_by_name(sheet_name)
        else:
            sheet = wb.sheet_by_index(sheet_no)  # 选择第0个表单
        columns = sheet.row_values(0)
        proto = {}
        key_index = {}
        for column_key in column_keys:
            key_index[column_key.key] = columns.index(column_key.column)
            proto[column_key.key] = None
        for i in range(1, sheet.nrows):
            entity = copy.deepcopy(proto)
            for key in entity:
                index = key_index.get(key)
                if index is not None:
                    entity[key] = sheet.row_values(i)[index]
            result_list.append(entity)
        return result_list

    @classmethod
    def excel_file2json_file(cls, column_keys, file_path, json_file_name, sheet_name=None, sheet_no=0,
                             path="../resources/excel/"):
        result_list = cls.excel_file2list(column_keys, file_path, sheet_name, sheet_no)
        with open(path + json_file_name, 'w', encoding='utf-8') as f:
            json.dump(result_list, f, indent=4)

# if __name__ == '__main__':
#     eu = ExcelUtil()
#     column_keys = []
#     column_key1 = ColumnKey("name", 0)
#     column_key2 = ColumnKey("age", 1)
#     column_key3 = ColumnKey("sex", 2)
#     column_key4 = ColumnKey("weight", 3)
#     column_keys.append(column_key1)
#     column_keys.append(column_key2)
#     column_keys.append(column_key3)
#     column_keys.append(column_key4)
#     data = [
#         {
#             "name": "wjj",
#             "age": "25",
#             "sex": "男",
#             "weight": "100kg"
#         },
#         {
#             "name": "wjj",
#             "age": "25",
#             "sex": "男",
#             "weight": "100kg"
#         }
#     ]
#     # eu.list2excel_file(column_keys, data, "person")
#     eu.excel_file2json_file(column_keys, "../resources/excel/person.xls", "person.myjson")
#     # print(eu.excel_file2list(column_keys, "../resources/excel/person.xls"))
# eu = ExcelUtil()
# column_keys = []
# column_key1 = ColumnKey("no", 0, "序号")
# column_key2 = ColumnKey("field", 1, "字段")
# column_key3 = ColumnKey("desp", 2, "描述")
# column_key4 = ColumnKey("type", 3, "类型")
# column_key5 = ColumnKey("isNeed", 4, "是否必须")
# column_key6 = ColumnKey("remark", 5, "备注")
# column_keys.append(column_key1)
# column_keys.append(column_key2)
# column_keys.append(column_key3)
# column_keys.append(column_key4)
# column_keys.append(column_key5)
# column_keys.append(column_key6)
# list = eu.excel_file2list(column_keys, "../../resources/excel/serialize.xlsx")
# print(list)
