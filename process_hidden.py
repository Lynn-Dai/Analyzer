import csv
import json

from collections import defaultdict


def hidden_sum(path: str):
    hidden = defaultdict(int)
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        for row in rows:
            for index, column in enumerate(row):
                if index == 0:
                    if '$$' in column:
                        hidden["$$"] = hidden['$$'] + 1
                        if 'clinit' in column:
                            hidden['$$_type'] = hidden['$$_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['$$_method'] = hidden['$$_method'] + 1
                        else:
                            hidden['$$_field'] = hidden['$$_field'] + 1
                    elif column.startswith('Lcom/google/android/collect'):
                        hidden["collect"] = hidden['collect'] + 1
                        if '(' in column or ')' in column:
                            hidden['collect_method'] = hidden['collect_method'] + 1
                        else:
                            hidden['collect_field'] = hidden['collect_field'] + 1
                    elif column.startswith('Lcom/google/android/gles_jni'):
                        # java 原生接口
                        hidden["jni"] = hidden['jni'] + 1
                        if 'clinit' in column:
                            hidden['jni_type'] = hidden['jni_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['jni_method'] = hidden['jni_method'] + 1
                        else:
                            hidden['jni_field'] = hidden['jni_field'] + 1
                    elif column.startswith('Lcom/google/android/mms'):
                        # Android源代码中的内部包.它不旨在由其他应用使用.
                        hidden["mms"] = hidden['mms'] + 1
                        if 'clinit' in column:
                            hidden['mms_type'] = hidden['mms_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['mms_method'] = hidden['mms_method'] + 1
                        else:
                            hidden['mms_field'] = hidden['mms_field'] + 1
                    elif column.startswith('Lcom/google/android/rappor'):
                        # RAPPOR 是一款新型的保密技术，它在提供人口统计数据的同时，能保护用户的私人数据。这个库里包含了用 Python 和 R 写成的代码。
                        hidden["rappor"] = hidden['rappor'] + 1
                        if 'clinit' in column:
                            hidden['rappor_type'] = hidden['rappor_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['rappor_method'] = hidden['rappor_method'] + 1
                        else:
                            hidden['rappor_field'] = hidden['rappor_field'] + 1
                    elif column.startswith('Lcom/google/android/util'):
                        # 工具库
                        hidden["util"] = hidden['util'] + 1
                        if 'clinit' in column:
                            hidden['util_type'] = hidden['util_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['util_method'] = hidden['util_method'] + 1
                        else:
                            hidden['util_field'] = hidden['util_field'] + 1
                    elif column.startswith('Lcom/sun'):
                        # com.sun.* sun.* 则是不被官方支持的，Oracle不保证这些API是跨平台的
                        hidden["com_sun"] = hidden['com_sun'] + 1
                        if 'clinit' in column:
                            hidden['com_sun_type'] = hidden['com_sun_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['com_sun_method'] = hidden['com_sun_method'] + 1
                        else:
                            hidden['com_sun_field'] = hidden['com_sun_field'] + 1
                    elif column.startswith('Ldalvik'):
                        # Google 公司自己设计用于Android平台的Java虚拟机
                        hidden["dalvik"] = hidden['dalvik'] + 1
                        if 'clinit' in column:
                            hidden['dalvik_type'] = hidden['dalvik_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['dalvik_method'] = hidden['dalvik_method'] + 1
                        else:
                            hidden['dalvik_field'] = hidden['dalvik_field'] + 1
                    elif column.startswith('Lgov/nist'):
                        # NIST是美国国家标准技术研究所
                        hidden["gov"] = hidden['gov'] + 1
                        if 'clinit' in column:
                            hidden['gov_type'] = hidden['gov_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['gov_method'] = hidden['gov_method'] + 1
                        else:
                            hidden['gov_field'] = hidden['gov_field'] + 1
                    elif column.startswith('Ljava/'):
                        # java库
                        hidden["java"] = hidden['java'] + 1
                        if 'clinit' in column:
                            hidden['java_type'] = hidden['java_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['java_method'] = hidden['java_method'] + 1
                        else:
                            hidden['java_field'] = hidden['java_field'] + 1
                    elif column.startswith('Ljavax/'):
                        # javax库
                        hidden["javax"] = hidden['javax'] + 1
                        if 'clinit' in column:
                            hidden['javax_type'] = hidden['javax_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['javax_method'] = hidden['javax_method'] + 1
                        else:
                            hidden['javax_field'] = hidden['javax_field'] + 1
                    elif column.startswith('Ljdk/'):
                        # jdk库
                        hidden["jdk"] = hidden['jdk'] + 1
                        if 'clinit' in column:
                            hidden['jdk_type'] = hidden['jdk_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['jdk_method'] = hidden['jdk_method'] + 1
                        else:
                            hidden['jdk_field'] = hidden['jdk_field'] + 1
                    elif column.startswith('Llibcore/'):
                        # libcore库
                        hidden["libcore"] = hidden['libcore'] + 1
                        if 'clinit' in column:
                            hidden['libcore_type'] = hidden['libcore_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['libcore_method'] = hidden['libcore_method'] + 1
                        else:
                            hidden['libcore_field'] = hidden['libcore_field'] + 1
                    elif column.startswith('Lorg/apache/'):
                        # apache库
                        hidden["apache"] = hidden['apache'] + 1
                        if 'clinit' in column:
                            hidden['apache_type'] = hidden['apache_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['apache_method'] = hidden['apache_method'] + 1
                        else:
                            hidden['apache_field'] = hidden['apache_field'] + 1
                    elif column.startswith('Lorg/ccil/cowan/tagsoup/'):
                        # ccil库
                        hidden["ccil"] = hidden['ccil'] + 1
                        if 'clinit' in column:
                            hidden['ccil_type'] = hidden['ccil_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['ccil_method'] = hidden['ccil_method'] + 1
                        else:
                            hidden['ccil_field'] = hidden['ccil_field'] + 1
                    elif column.startswith('Lorg/chromium/'):
                        # chromium库
                        hidden["chromium"] = hidden['chromium'] + 1
                        if 'clinit' in column:
                            hidden['chromium_type'] = hidden['chromium_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['chromium_method'] = hidden['chromium_method'] + 1
                        else:
                            hidden['chromium_field'] = hidden['chromium_field'] + 1
                    elif column.startswith('Lorg/json/'):
                        # json
                        hidden["json"] = hidden['json'] + 1
                        if 'clinit' in column:
                            hidden['json_type'] = hidden['json_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['json_method'] = hidden['json_method'] + 1
                        else:
                            hidden['json_field'] = hidden['json_field'] + 1
                    elif column.startswith('Lorg/w3c/'):
                        # w3c
                        hidden["w3c"] = hidden['w3c'] + 1
                        if 'clinit' in column:
                            hidden['w3c_type'] = hidden['w3c_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['w3c_method'] = hidden['w3c_method'] + 1
                        else:
                            hidden['w3c_field'] = hidden['w3c_field'] + 1
                    elif column.startswith('Lorg/xml/sax/'):
                        # xml
                        hidden["xml"] = hidden['xml'] + 1
                        if 'clinit' in column:
                            hidden['xml_type'] = hidden['xml_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['xml_method'] = hidden['xml_method'] + 1
                        else:
                            hidden['xml_field'] = hidden['xml_field'] + 1
                    elif column.startswith('Lorg/xmlpull/'):
                        # xmlpull
                        hidden["xmlpull"] = hidden['xmlpull'] + 1
                        if 'clinit' in column:
                            hidden['xmlpull_type'] = hidden['xmlpull_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['xmlpull_method'] = hidden['xmlpull_method'] + 1
                        else:
                            hidden['xmlpull_field'] = hidden['xmlpull_field'] + 1
                    elif column.startswith('Lsun/'):
                        # sun
                        hidden["sun"] = hidden['sun'] + 1
                        if 'clinit' in column:
                            hidden['sun_type'] = hidden['sun_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['sun_method'] = hidden['sun_method'] + 1
                        else:
                            hidden['sun_field'] = hidden['sun_field'] + 1
                    elif column.startswith('Landroid/Manifest$'):
                        # Manifest$
                        hidden["Manifest"] = hidden['Manifest'] + 1
                        if 'clinit' in column:
                            hidden['Manifest_type'] = hidden['Manifest_type'] + 1
                        elif '(' in column or ')' in column:
                            hidden['Manifest_method'] = hidden['Manifest_method'] + 1
                        else:
                            hidden['Manifest_field'] = hidden['Manifest_field'] + 1
                    if 'clinit' in column:
                        hidden['type'] = hidden['type'] + 1
                    elif '(' in column or ')' in column:
                        hidden['method'] = hidden['method'] + 1
                    else:
                        hidden['field'] = hidden['field'] + 1
    return hidden


def check_hidden(column: str) -> str:
    if column == "blacklist" or column == "blocked":
        return column
    elif column == "greylist" or column == "unsupported":
        return column
    elif "greylist-max-" in column or "max-target-" in column:
        return column
    elif column == "whitelist" or column == "sdk":
        return column
    else:
        return ""


def read_csv(path: str) -> defaultdict:
    with open(path, encoding="utf-8") as f:
        hidden_api = defaultdict(list)
        reader = csv.reader(f)
        rows = [row for row in reader]
        # header_row = next(reader)
        for row in rows:
            hidden_flag = ""
            current_api = ""
            for index, column in enumerate(row):
                # print(index, column)
                if index == 0:
                    current_api = column
                else:
                    hidden_flag = hidden_flag + check_hidden(column)
            hidden_api[hidden_flag].append(current_api)
        return hidden_api


def compare_hidden(aosp: defaultdict, magic: defaultdict) -> defaultdict:
    modify_dict = defaultdict(list)
    for m_key in magic.keys():
        for m in magic[m_key]:
            for a_key in aosp.keys():
                if m in aosp[a_key]:
                    if a_key == m_key:
                        pass
                    else:
                        # print(a_key + "2" + m_key)
                        modify_dict[a_key + "2" + m_key].append(m)
                    break
            # modify_dict["new2" + m_key].append(m)
    return modify_dict


def dict_to_json_write_file(data_dict, filename):
    with open(filename, 'w') as f:
        json.dump(data_dict, f, sort_keys=True, indent=4, separators=(',', ':'))


def dict_to_csv(data_dict, file_name):
    with open(file_name, "wb") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data_dict.items:
            writer.writerow([key, value])


if __name__ == '__main__':
    aosp_13_beta = read_csv("E:/ASE/实验数据/2-Hidden/csvs/hiddenapi-flags-13-beta.csv")
    aosp_12 = read_csv("E:/ASE/实验数据/2-Hidden/csvs/hiddenapi-flags-12.csv")
    aosp_11 = read_csv("E:/ASE/实验数据/2-Hidden/csvs/hiddenapi-flags-11.csv")
    # aosp_10 = read_csv("E:/ASE/实验数据/2-Hidden/csvs/hiddenapi-flags-10.csv")
    # lineage_19 = read_csv("E:/ASE/实验数据/2-Hidden/csvs/hiddenapi-flags-lineage19.csv")
    # lineage_18 = read_csv("E:/ASE/实验数据/2-Hidden/csvs/hiddenapi-flags-lineage18.csv")
    #
    result = compare_hidden(aosp_12, aosp_13_beta)
    for key in result.keys():
        print(key)
        print(len(result[key]))
        if key == "max-target-o2sdk":
            print(result[key])
        elif key == "blocked2sdk":
            print(result[key])
        elif key == "unsupported2blocked":
            print(result[key])
    #
    # print("LINEAGE 19")
    #
    # conflicts = compare_hidden(aosp_12, lineage_19)
    # for key in conflicts.keys():
    #     print(key)
    #     print(len(conflicts[key]))
    #     print(conflicts[key])

    # process_hidden(read_csv(hidden_path))
    # hidden_path = "E:/ASE/实验数据/2-Hidden/csvs/hiddenapi-flags_10_r2.csv"
    # hiddens = read_csv(hidden_path)
    # for keys in hiddens.keys():
    #     print(keys)
    #     print(len(hiddens[keys]))
    #
    # sum = hidden_sum(hidden_path)
    # for k in sum.keys():
    #     print(k)
    #     print(sum[k])
