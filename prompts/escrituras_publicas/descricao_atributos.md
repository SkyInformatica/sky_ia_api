# Instruçoes e Padrões de preenchimento do JSON

## Tipos de Dados

| Tipo de dado | Tipo XML | Descrição / Formato                            | Exemplo             |
| ------------ | -------- | ---------------------------------------------- | ------------------- |
| Alfanumérico | String   | Admite texto, caracteres especiais e números   | abc@123             |
| Numérico     | String   | Texto que **só** aceita números                | 1234567890123456    |
| Inteiro      | Number   | Somente números inteiros                       | 100                 |
| Flutuante    | Number   | Número real em ponto flutuante (separador “.”) | 3.121314            |
| Monetário    | Number   | Número para moeda (2 casas decimais)           | 10518.65            |
| Data         | String   | Formato de data `YYYY-MM-DD`                   | 2025-07-22          |
| Data e Hora  | String   | Formato de data / hora `YYYY-MM-DD HH:MM:SS`   | 2025-07-22 09:30:00 |
| Booleano     | String   | Verdadeiro (1) / Falso (0)                     | 0                   |
| CPF          | String   | Formato `XXX.XXX.XXX-XX`                       | 111.222.333-44      |
| CNPJ         | String   | Formato `XX.XXX.XXX/XXXX-XX`                   | 11.222.333/4444-55  |

---

## Estruturas de Dados (Tags e Campos)

### Classe `ESCRITURA`

| Tag / Campo                        | Observação                                                               | Tipo                                       |
| ---------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------ |
| TITULO                             | Tipo da escritura. Normalmente encontrado na primeira frase da escritura | Alfanumérico                               |
| DATA                               | Data do instrumento/escritura                                            | Data                                       |
| LIVRO                              | Livro do instrumento/escritura                                           | Alfanumérico                               |
| FOLHA                              | Folha do instrumento/escritura                                           | Alfanumérico                               |
| NEGOCIOS                           | Lista de negócios                                                        | `List<NEGOCIO>`                            |
| PARTES_NEGOCIO                     | Lista de das partes da escritura                                         | `List<PARTES>`                             |
| FINANCIAMENTO                      | Dados do financiamento                                                   | Classe `FINANCIAMENTO`                     |
| IMPOSTOS                           | Impostos recolhidos                                                      | Classe `IMPOSTOS`                          |
| CLAUSULAS_CERTIDOES                | Certidões apresentadas referente as partes e imóveis                     | `List<CLAUSULAS_CERTIDOES>`                |
| CLAUSULAS_DECLARACOES_AUTORIZACOES | Autorizações e declarações das partes                                    | `List<CLAUSULAS_DECLARACOES_AUTORIZACOES>` |

### Classe `NEGOCIO`

| Tag / Campo           | Observação                              | Tipo           |
| --------------------- | --------------------------------------- | -------------- |
| SEQUENCIAL            | Sequência do negócio (chave de vínculo) | Inteiro        |
| TIPO_ATO              | Tipo de ato (lista controlada)          | Inteiro        |
| DESCRICAO_TIPO_ATO    | Descrição do tipo de ato                | Alfanumérico   |
| VALOR_TRANSMISSAO     | Valor da transmissão                    | Monetário      |
| VALOR_VENAL           | Valor venal                             | Monetário      |
| VALOR_FINANCIAMENTO   | Valor do financiamento                  | Monetário      |
| VALOR_AVALIACAO       | Valor de avaliação do imóvel            | Monetário      |
| VALOR_LEILAO          | Valor de leilão                         | Monetário      |
| RECURSOS_PROPRIOS     | Recursos próprios                       | Monetário      |
| RECURSOS_FINANCIADO   | Recursos financiados                    | Monetário      |
| PRIMEIRA_AQUISICAO    | Primeira aquisição? (1 Sim / 0-Não)     | Booleano       |
| PAGO_EM_ESPECIE       | Pagamento em espécie? (1 Sim / 0-Não)   | Booleano       |
| VALOR_PAGO_EM_ESPECIE | Valor pago em espécie                   | Monetário      |
| OBSERVACOES_GERAIS    | Observações                             | Alfanumérico   |
| IMOVEIS               | Imóveis vinculado                       | `List<IMOVEL>` |
| PARTES                | Partes deste ato                        | `List<PARTE>`  |

### Classe `IMOVEL`

| Tag                   | Observação                                         | Tipo                     |
| --------------------- | -------------------------------------------------- | ------------------------ |
| CNM                   | Codigo Nacional da Matricula (se houver)           | Alfanumérico             |
| LOCALIZACAO           | 1 = Urbano / 2 = Rural                             | Inteiro                  |
| DESCRICAO_LOCALIZACAO | Descrição da localizacao                           | Alfanumérico             |
| NUMERO_MATRICULA      | Número de matricula do imóvel                      | Inteiro                  |
| IPTU                  | Número do IPTU                                     | Alfanumérico             |
| CCIR                  | Número do CCIR                                     | Alfanumérico             |
| NIRF                  | Número do NIRF                                     | Alfanumérico             |
| TIPO_IMOVEL           | Tipo de imóvel (lista controlada)                  | Inteiro                  |
| DESCRICAO_TIPO_IMOVEL | Descrição tipo de imóvel                           | Alfanumérico             |
| DESCRICAO_IMOVEL      | Texto descrevendo o imóvel e confrontações         | Alfanumérico             |
| VALOR_AVALICACAO      | Valor de avaliação do imóvel                       | Monetário                |
| VALOR_ATRIBUIDO       | Valor atribuído ao imóvel                          | Monetário                |
| ENDERECO              | Endereço do imóvel extraído da descrição do imóvel | Classe `ENDERECO_IMOVEL` |

### Classe `ENDERECO_IMOVEL`

| Tag             | Observação         | Tipo         |
| --------------- | ------------------ | ------------ |
| TIPO_LOGRADOURO | Tipo de logradouro | Alfanumérico |
| LOGRADOURO      | Logradouro         | Alfanumérico |
| NUMERO          | Número             | Alfanumérico |
| UNIDADE         | Unidade            | Alfanumérico |
| BAIRRO          | Bairro             | Alfanumérico |
| CIDADE          | Cidade             | Alfanumérico |
| UF              | UF                 | Alfanumérico |
| LOTE            | Lote               | Alfanumérico |
| QUADRA          | Quadra             | Alfanumérico |
| TORRE           | Torre              | Alfanumérico |
| NOME_LOTEAMENTO | Nome do loteamento | Alfanumérico |
| NOME_CONDOMINIO | Nome do condomínio | Alfanumérico |
| COMPLEMENTO     | Complemento        | Alfanumérico |

### Classe `PARTE`

| Tag                    | Observação                      | Tipo         |
| ---------------------- | ------------------------------- | ------------ |
| QUALIFICACAO           | Qualificação (lista controlada) | Inteiro      |
| DESCRICAO_QUALIFICACAO | Descricao da qualificação       | Alfanumérico |
| CPF_CNPJ               | CPF / CNPJ                      | CPF/CNPJ     |
| FRACAO                 | Fração                          | Flutuante    |

### Classe `PARTES` (vínculo Parte × Negócio)

| Tag                        | Observação                                                                                    | Tipo                  |
| -------------------------- | --------------------------------------------------------------------------------------------- | --------------------- |
| SEQUENCIAL_NEGOCIO         | Lista de sequenciais do(s) negócio(s) (ex.: “1,2,3”)                                          | Alfanumérico          |
| NOME                       | Nome                                                                                          | Alfanumérico          |
| CPF_CNPJ                   | CPF / CNPJ                                                                                    | CPF/CNPJ              |
| GENERO                     | Gênero (1 = Masculino, 2 = Feminimo)                                                          | Inteiro               |
| DESCRICAO_GENERO           | Descrição do gênero                                                                           | Alfanumérico          |
| DOCUMENTO                  | Outro documento de identificação alem do CPF (RG, OAB, PASSAPORTE, etc )                      | Alfanumérico          |
| ORGAO_EMISSOR              | Órgão emissor                                                                                 | Alfanumérico          |
| NACIONALIDADE              | Nacionalidade                                                                                 | Alfanumérico          |
| ESTADO_CIVIL               | Estado civil (lista controlada)                                                               | Inteiro               |
| DESCRICAO_ESTADO_CIVIL     | Descricao estado civil                                                                        | Alfanumérico          |
| CAPACIDADE_CIVIL           | Capacidade civil (lista controlada)                                                           | Inteiro               |
| DESCRICAO_CAPACIDADE_CIVIL | Descrição da capacidade civil                                                                 | Alfanumérico          |
| REGIME_BENS                | Regime de bens (lista controlada)                                                             | Inteiro               |
| DESCRICAO_REGIME_BENS      | Descricao do regime de bens                                                                   | Alfanumérico          |
| DATA_CASAMENTO             | Data do casamento                                                                             | Data                  |
| DATA_NASCIMENTO            | Data de nascimento                                                                            | Data                  |
| NUMERO_PACTO               | Numero do pacto antenupcial                                                                   | Alfanumérico          |
| DATA_PACTO                 | Data do pacto antenupcial                                                                     | Data                  |
| LOCAL_REGISTRO_PACTO       | Local do registro do pacto antenupcial                                                        | Alfanumérico          |
| UNIAO_ESTAVEL              | Vive em únião estável? 1 = Sim / 0 = Não                                                      | Booleano              |
| PROFISSAO                  | Profissão                                                                                     | Inteiro               |
| ENDERECO                   | Todos os campos de endereço residencial                                                       | Classe `<ENDERECO>`   |
| CPF_CONJUGE                | CPF do cônjuge                                                                                | CPF                   |
| EMAIL                      | E-mail                                                                                        | Alfanumérico          |
| FILIACAO1                  | Nome do 1º genitor                                                                            | Alfanumérico          |
| FILIACAO2                  | Nome do 2º genitor                                                                            | Alfanumérico          |
| REPRESENTANTES             | Representantes desta parte quando uma pessoa juridica (dados do instrumento de representação) | `List<REPRESENTANTE>` |

### Classe `ENDERECO`

| Tag               | Observação                 | Tipo         |
| ----------------- | -------------------------- | ------------ |
| CEP               | CEP                        | Alfanumérico |
| TIPO_LOGRADOURO   | Tipo de logradouro         | Alfanumérico |
| LOGRADOURO        | Logradouro                 | Alfanumérico |
| NUMERO            | Número                     | Alfanumérico |
| UNIDADE           | Unidade                    | Alfanumérico |
| COMPLEMENTO       | Complemento                | Alfanumérico |
| BAIRRO            | Bairro                     | Alfanumérico |
| CIDADE            | Cidade                     | Alfanumérico |
| ENDERECO_COMPLETO | Texto do endereço completo | Alfanumérico |

### Classe `REPRESENTANTE`

| Tag                | Observação            | Tipo         |
| ------------------ | --------------------- | ------------ |
| NOME_REPRESENTANTE | Nome do representante | Alfanumérico |
| CPF_REPRESENTANTE  | CPF do representante  | CPF          |
| CNPJ_REPRESENTADO  | CNPJ do representado  | CNPJ         |
| NUMERO_INSTRUMENTO | Número do instrumento | Alfanumérico |
| TIPO_REGISTRO      | Tipo de registro      | Alfanumérico |
| ORGAO              | Órgão                 | Alfanumérico |
| FORMA_REGISTRO     | Forma de registro     | Alfanumérico |
| NUMERO_LIVRO       | Número do livro       | Alfanumérico |
| NUMERO_FOLHA       | Número da Folha       | Alfanumérico |
| NUMERO_REGISTRO    | Número do registro    | Inteiro      |
| DATA_REGISTRO      | Data do registro      | Data         |

### Classe `FINANCIAMENTO`

| Tag                                   | Observação                                             | Tipo         |
| ------------------------------------- | ------------------------------------------------------ | ------------ |
| PRAZO_CARENCIA                        | Prazo de carência                                      | Inteiro      |
| ENQUADRAMENTO_FINANCIAMENTO           | Enquadramento (lista controlada)                       | Inteiro      |
| DESCRICAO_ENQUADRAMENTO_FINANCIAMENTO | Descricao do enquadramento                             | Alfanumérico |
| SISTEMA_AMORTIZACAO                   | Descricao do Sistema de amortização (lista controlada) | Inteiro      |
| DESCRICAO_SISTEMA_AMORTIZACAO         | Sistema de amortização                                 | Alfanumérico |
| ORIGEM_RECURSOS                       | Origem dos recursos                                    | Inteiro      |
| DESCRICAO_ORIGEM_RECURSOS             | Descricao do Origem dos recursos                       | Alfanumérico |
| JUROS_ANUAL_NOMINAL                   | Juros anual nominal                                    | Flutuante    |
| JUROS_ANUAL_EFETIVO                   | Juros anual efetivo                                    | Flutuante    |
| JUROS_MENSAL_NOMINAL                  | Juros mensal nominal                                   | Flutuante    |
| JUROS_MENSAL_EFETIVO                  | Juros mensal efetivo                                   | Flutuante    |
| PRAZO_AMORTIZACAO                     | Prazo de amortização                                   | Inteiro      |
| VALOR_PRIMEIRA_PARCELA                | Valor da primeira parcela                              | Monetário    |
| DATA_PRIMEIRA_PARCELA                 | Data da primeira parcela                               | Data         |
| DESTINO_FINANCIAMENTO                 | Destino do financiamento                               | Alfanumérico |
| FORMA_DE_PAGAMENTO                    | Forma de pagamento                                     | Alfanumérico |

### Classe `IMPOSTOS`

| Tag                 | Observação                   | Tipo                       |
| ------------------- | ---------------------------- | -------------------------- |
| IMPOSTO_TRANSMISSAO | Dados da guia do ITBI, ITCMD | `List<IMPOSTO_TRANSMISSO>` |

### Classe `IMPOSTO_TRANSMISSAO`

| Tag       | Observação      | Tipo         |
| --------- | --------------- | ------------ |
| ISENCAO   | Possui isenção? | Booleano     |
| INSCRICAO | Nº da inscrição | Alfanumérico |
| GUIA      | Nº da guia      | Alfanumérico |
| VALOR     | Valor pago      | Monetário    |

### Classe `CLAUSULAS_CERTIDOES`

| Tag           | Observação                              | Tipo         |
| ------------- | --------------------------------------- | ------------ |
| TIPO_CERTIDAO | Tipo da certidão                        | Alfanumérico |
| DESCREVER     | Texto descrição da certidão apresentada | Alfanumérico |

### Classe `CLAUSULAS_DECLARACOES_AUTORIZACOES`

| Tag                         | Observação                           | Tipo         |
| --------------------------- | ------------------------------------ | ------------ |
| TIPO_DECLARACAO_AUTORIZACAO | Tipo da declaracao ou da autorização | Alfanumérico |
| DESCREVER                   | Texto da declaração autorização      | Alfanumérico |
