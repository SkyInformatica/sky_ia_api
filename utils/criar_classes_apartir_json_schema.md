#criar_classes_apartir_json_schema

```shell
.venv/bin/python -c "import json; open('temp_schema.json', 'w').write(json.dumps(json.loads(open('/prompts/escrituras_publicas/escrituras.schema.json').read())['schema']))"
```

```shell
.venv/bin/datamodel-codegen --input temp_schema.json --output models/escritura_publica.py --input-file-type jsonschema
```
