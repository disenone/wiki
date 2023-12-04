# -*- coding: utf-8 -*-
import os
import json
from auto_translater import CreateProcessInfo, processed_dict_file, dir_to_translate


def main(working_folder='.'):
    # 按文件名称顺序排序
    dir_to_translate_abs = os.path.abspath(os.path.join(working_folder, dir_to_translate))
    file_list = os.listdir(dir_to_translate_abs)
    file_list = sorted(file_list)
    file_list = [os.path.join(dir_to_translate_abs, file) for file in file_list]

    processed_dict = {}
    # 遍历目录下的所有.md文件，并进行翻译
    for input_file in file_list:
        processed_dict[os.path.basename(input_file)] = CreateProcessInfo(input_file)

    with open(processed_dict_file, 'wb') as f:
        f.write(json.dumps(processed_dict, indent=2, ensure_ascii=False).encode('utf-8'))


if __name__ == '__main__':
    main()
