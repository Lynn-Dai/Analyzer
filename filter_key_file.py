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
        for relation in data['cells']:
            if relation['src'] in key_entities:
                src_entity = entities[relation['src']]
                src_signature = src_entity['qualifiedName']
                if src_entity['category'] == "Method":
                    src_signature += "(" + src_entity['parameter']['types'] + ")"
                # key_entities_qualifiedName.append(signature)
                dest_entity = entities[relation['dest']]
                dest_signature = dest_entity['qualifiedName']
                if dest_entity['category'] == "Method":
                    dest_signature += "(" + dest_entity['parameter']['types'] + ")"
                value = relation['values'].keys().remove('loc')




