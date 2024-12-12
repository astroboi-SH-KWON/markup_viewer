from markup_viewer import XmlViewer, JsonViewer
import glob
import time


def get_file_list(f_pattern):
    return glob.glob(f_pattern)


def view_xml(file_path, n=1):
    xml_v = XmlViewer()
    xml_list = get_file_list(file_path)

    for f_path in xml_list[:n]:
        print(f"\n\nfile path : {f_path}\n")
        tree = xml_v.get_xml_tree(f_path)
        root = xml_v.get_xml_root(tree)
        print(f"{root}\n{root.tag} |0| {root.attrib}")

        res_list = xml_v.get_xml_tree_recursively(root, [])
        for i in res_list:
            print(i)


if __name__ == '__main__':
    # unzip_target_file()

    username = 'terry007x'
    st_time = time.strftime('%Y%m%d_%H_%M')

    json_v = JsonViewer()
    json_dict = json_v.get_json('input/mGFQyyXX_2024.json')
    res_df = json_v.parse_weekly_report_by_username(json_dict, username)

    df = res_df.reset_index()  # make sure indexes pair with number of rows
