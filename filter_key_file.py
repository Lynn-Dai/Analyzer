import json

key_files = []
key_entities = []
entities = {}
# key_entities_qualifiedName = []
res = []

def read_key(path: str):
    f = open(path, encoding="utf-8")
    lines = f.readlines()
    for line in lines:
        key_files.append(line)


def filter_json(path: str):
    with open(path, 'r') as f:
        data = json.loads(f.read())
        for entity in data['variables']:
            entities[entity['id']] = entity
            if entity['File'] in key_files:
                key_entities.append(entity['id'])
                # signature = entity['qualifiedName']
                # if entity['category'] == "Method":
                #     signature += "(" + entity['parameter']['types'] + ")"
                # key_entities_qualifiedName.append(signature)
        for relation in data['cells']:
            if relation['src'] in key_entities:
                src_entity = entities[relation['src']]



