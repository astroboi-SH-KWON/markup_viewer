import xml.etree.ElementTree as ET
import json
import pandas as pd


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
        tmp_list = []
        for val in trello_json['actions']:
            if val['memberCreator']['username'] == username:
                if 'text' in val['data']:
                    tmp_list.append([str(val['date']).split('T')[0].replace('-', ''), val['data']['card']['name'],
                                     val['data']['text']])
        return pd.DataFrame(tmp_list, columns=['DATE', 'WEEK', 'REPORT'])
