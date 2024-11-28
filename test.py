from markup_viewer import xml_viewer
import glob
import json


def get_file_list(f_pattern):
    return glob.glob(f_pattern)


def view_xml(file_path, n=1):
    xml_v = xml_viewer()
    xml_list = get_file_list(file_path)

    for f_path in xml_list[:n]:
        print(f"\n\nfile path : {f_path}\n")
        tree = xml_v.get_xml_tree(f_path)
        root = xml_v.get_xml_root(tree)
        print(f"{root}\n{root.tag} |0| {root.attrib}")

        res_list = xml_v.get_xml_tree_recursively(root, [])
        for i in res_list:
            print(i)


def view_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        print(data)


if __name__ == '__main__':
    # view_xml("./input/*.xml", n=2)
    # view_xml("./input/*.ts", n=1)
    view_json("input/mGFQyyXX_2024.json")


