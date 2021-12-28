#!/usr/bin/env python3

import sys
import json
import yaml

if len(sys.argv) > 1:
    file = sys.argv[1]
    with open('./' + file, 'r') as j_file:
        try:
            json_file = json.load(j_file)
            with open('./' + file.split('.')[0] + '.yml', 'w') as yml_file:
                yml_data = yaml.dump(json_file)
                yml_file.write(yml_data)
        except Exception:
            try:
                with open('./' + file, 'r') as y_file:
                    yaml_file = yaml.safe_load(y_file)
                    print(yaml_file)
                with open('./' + file.split('.')[0] + '.json', 'w') as jsn_file:
                    jsn_data = json.dumps(yaml_file)
                    jsn_file.write(jsn_data)

            except Exception:
                print('This is not json or yaml file')
