import xml.etree.ElementTree as ET


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