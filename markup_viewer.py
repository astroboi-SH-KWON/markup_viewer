import xml.etree.ElementTree as ET
import json
import xlsxwriter
import time


class xml_viewer:
    def __init__(self):
        pass

    def get_xml_tree(self, fl_path):
        tree = ET.parse(fl_path)
        return tree

    def get_xml_root(self, tree):
        return tree.getroot()

    def get_xml_tree_recursively(self, node, res_list, indent="\t", idx=1):
        for child in node:
            res_list.append(f"{indent}{child.tag} |{idx}| {child.attrib}")
            self.get_xml_tree_recursively(child, res_list, indent + "\t", idx + 1)
        return res_list


class json_viewer:
    def __init__(self):
        pass

    def get_json(self, file_path):
        try:
            f = open(file_path, 'r')
            data = json.load(f)
            f.close()
            return data
        except:
            raise Exception

    def parse_weekly_report_by_username(self, trello_json, username):
        st_time = time.strftime('%Y%m%d_%H_%M')

        idx = 2
        # Create a workbook and add a worksheet
        workbook = xlsxwriter.Workbook(f"output/weekly_report_{username}_{st_time}.xlsx")
        worksheet = workbook.add_worksheet()

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Text with formatting.
        worksheet.write('A1', "날짜", bold)
        worksheet.write('B1', "주간보고", bold)
        worksheet.write('C1', "비고", bold)

        for val in trello_json['actions']:
            if val['memberCreator']['username'] == username:
                if 'text' in val['data']:
                    print(f"[주간보고] 어니소프트 기업연구소_{str(val['date']).split('T')[0].replace('-', '')}")
                    print(f"date:{val['data']['card']['name']}")
                    print(f"{val['data']['text']}\n\n")

                    worksheet.write(f'A{idx}', val['data']['card']['name'])
                    worksheet.write(f'B{idx}', val['data']['text'])
                    worksheet.write(f'C{idx}', f"_{str(val['date']).split('T')[0].replace('-', '')}")
                    idx += 1
        # Close the workbook
        workbook.close()
