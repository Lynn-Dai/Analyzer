import os
from typing import List
# from utils import FileCSV


class SDKApi:
    code_path: str
    out_path: str
    api_path: str

    def __init__(self, code_path, out_path):
        self.code_path = code_path
        self.out_path = out_path
        self.api_path = os.path.join(code_path, 'api/current.txt') if os.path.exists(
            os.path.join(code_path, 'api/current.txt')) else \
            os.path.join(code_path, 'core/api/current.txt')

    def get_apis(self):
        apis = []
        stack: List[str] = []
        with open(self.api_path, 'r', encoding='utf-8') as f:
            for line_data in f:
                line = str(line_data).strip().split(' ')
                if line[0] == 'package' and line[2] == '{':
                    stack.append(line[1])
                elif 'class' in line and '{' in line:
                    stack.append(line[line.index('class') + 1])
                elif 'interface' in line and '{' in line:
                    stack.append(line[line.index('interface') + 1])
                elif '@interface' in line and '{' in line:
                    stack.append(line[line.index('@interface') + 1])
                elif 'enum' in line and '{' in line:
                    stack.append(line[line.index('enum') + 1])
                elif '}' in line:
                    stack.pop()
                else:
                    pre_name = '.'.join(stack) + '.'
                    if 'ctor' in line:
                        ctor = ''
                        for content in line:
                            if '(' in content:
                                ctor = content
                                break
                        apis.append(pre_name + ctor[max(ctor.find('.') + 1, 0): ctor.rfind('(')])
                    elif 'method' in line:
                        method = ''
                        for content in line:
                            if '(' in content:
                                method = content
                                break
                        apis.append(pre_name + method[0: method.rfind('(')])
                    elif 'field' in line:
                        if '=' in line:
                            field = line[line.index('=') - 1]
                        else:
                            field = line[-1][0: line[-1].rfind(';')]
                        apis.append(pre_name + field)

        # FileCSV.base_write_to_csv(self.out_path, 'sdk_apis', apis)
        return apis


if __name__ == '__main__':
    SDKApi('D:\\Honor\\source_code\\LineageOS\\base\\api\\current.txt', 'D:\\Honor\\source_code\\LineageOS').get_apis()
