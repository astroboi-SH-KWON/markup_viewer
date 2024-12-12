import xml.etree.ElementTree as ET
import json
import pandas as pd
import os, shutil
import datetime


class XmlViewer:
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


class JsonViewer:
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
        tmp_list = []
        for val in trello_json['actions']:
            if val['memberCreator']['username'] == username:
                if 'text' in val['data']:
                    tmp_list.append([str(val['date']).split('T')[0].replace('-', ''), val['data']['card']['name'],
                                     val['data']['text']])
        return pd.DataFrame(tmp_list, columns=['DATE', 'WEEK', 'REPORT'])


def replace_text(replacements: dict, shapes: list):
    """
    https://stackoverflow.com/questions/37924808/python-pptx-power-point-find-and-replace-text-ctrl-h
    https://stackoverflow.com/questions/73219378/python-pptx-how-to-replace-keyword-across-multiple-runs
    Takes dict of {match: replacement, ... } and replaces all matches.
    Currently not implemented for charts or graphics.
    """
    for shape in shapes:
        for match, replacement in replacements.items():
            if shape.has_text_frame:
                if (shape.text.find(match)) != -1:
                    text_frame = shape.text_frame
                    for paragraph in text_frame.paragraphs:
                        for run in paragraph.runs:
                            cur_text = run.text
                            new_text = cur_text.replace(str(match), str(replacement))
                            run.text = new_text
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        if match in cell.text:
                            new_text = cell.text.replace(match, replacement)
                            cell.text = new_text


def unzip_target_file(fl):
    import zipfile
    with zipfile.ZipFile(f"{fl}.pptx", 'r') as zip_ref:
        zip_ref.extractall(fl)


def make_onysoft_weekly_report_ppt(df):
    for index, row in df.iterrows():
        end_date_week = row['DATE']
        report = row['REPORT']
        en_date = datetime.datetime.strptime(end_date_week, '%Y%m%d')
        d = datetime.timedelta(days=4)
        st_date = en_date - d
        st = str(st_date).split(" ")[0].replace("2024-", "'24").replace("2023-", "'23").replace("-", "")
        en = str(en_date).split(" ")[0].replace("2024-", "'24").replace("2023-", "'23").replace("-", "")

        # if en[1:] == '240802' or en[1:] == '240811':
        #     print(st + " ~ " + en)
        #     print(report)
        #     continue

        replacements = {
            'week': st + " ~ " + en,
            '[title0]': '',
            'detail0': '',
            '[title1]': '',
            'detail1': '',
            '[title2]': '',
            'detail2': '',
            '[title3]': '',
            'detail3': '',
        }
        report_list = [x for x in report.split("\n") if str(x).strip()]
        cnt = 0
        for rep_line in report_list:
            if rep_line[0] == "[" and rep_line[-1] == "]":
                cnt += 1
                replacements['[title' + str(cnt - 1) + "]"] = rep_line
                continue
            if replacements['detail' + str(cnt - 1)] == '':
                replacements['detail' + str(cnt - 1)] = rep_line.rstrip()
            else:
                replacements['detail' + str(cnt - 1)] = replacements['detail' + str(cnt - 1)] + f"\n{rep_line.rstrip()}"

        fl_nm = f"output/weekly_report/[주간보고] 어니소프트 기업연구소_{en[1:]}"
        shutil.copyfile('input/weekly_report_template.pptx', f"{fl_nm}.pptx")

        unzip_target_file(fl_nm)

        # Read in the file
        with open(f"{fl_nm}/ppt/slides/slide1.xml", 'r') as file:
            filedata = file.read()

        # Replace the target string
        for k, v in replacements.items():
            filedata = filedata.replace(k, v)

        # Write the file out again
        with open(f"{fl_nm}/ppt/slides/slide1.xml", 'w') as file:
            file.write(filedata)

        shutil.make_archive(f"{fl_nm}.pptx", 'zip', fl_nm)
        shutil.rmtree(fl_nm)
        os.rename(f"{fl_nm}.pptx.zip", f"{fl_nm}.pptx")
