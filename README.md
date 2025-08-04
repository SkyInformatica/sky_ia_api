# sky_ia_api

## Descrição

API para extração de dados estruturados de documentos utilizando IA.

## Endpoints

### Qualificação

```
POST /qualificacao
```

Endpoint para qualificação de documentos através de upload direto de arquivos.

**Tipos de arquivos suportados:**

- Imagens: PNG, JPEG/JPG
- Documentos: PDF

### Escritura Pública

```
POST /escritura_publica
```

Endpoint para extração de dados de escritura pública através de upload direto de arquivos.

**Tipos de arquivos suportados:**

- Imagens: PNG, JPEG/JPG
- Documentos: PDF

## Exemplos de uso

Veja os exemplos de como utilizar a API nos diretórios `exemplos/`:

- `qualificacao_upload.py` e `qualificacao_upload.sh` - Exemplos de como enviar documentos para o endpoint de qualificação
- `escritura_publica_upload.py` e `escritura_publica_upload.sh` - Exemplos de como enviar documentos para o endpoint de escritura pública
