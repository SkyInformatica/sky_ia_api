## Instruçoes e Padrões de preenchimento do JSON

### 1. Tabela – Tipos de Dados

| Tipo de dado     | Tipo XML | Descrição / Formato                            | Exemplo                 |
| ---------------- | -------- | ---------------------------------------------- | ----------------------- |
| Alfanumérico     | String   | Admite texto, caracteres especiais e números   | abc@123                 |
| Numérico         | String   | Texto que **só** aceita números                | 1234567890123456        |
| Inteiro          | Number   | Somente números inteiros                       | 100                     |
| Flutuante        | Number   | Número real em ponto flutuante (separador “.”) | 3.121314                |
| Monetário        | Number   | Número para moeda (2 casas decimais)           | 10518.65                |
| Data             | String   | Formato de data `YYYY-MM-DD`                   | 2025-07-22              |
| Data e Hora      | String   | Formato de data / hora `YYYY-MM-DD HH:MM:SS`   | 2025-07-22 09:30:00     |
| Booleano         | String   | Verdadeiro (1) / Falso (0)                     | 0                       |
| Lista controlada | Inteiro  | Valor restrito aos códigos da respectiva lista | —                       |
| TAG (lista)      | TAG      | Marca início/fim de lista de classes           | `<NEGOCIOS></NEGOCIOS>` |
| CPF              | String   | Formato `XXX.XXX.XXX-XX`                       | 111.222.333-44          |
| CNPJ             | String   | Formato `XX.XXX.XXX/XXXX-XX`                   | 11.222.333/4444-55      |
| Texto            | Text     | Conteúdo protegido por CDATA                   | `<![CDATA[ …texto… ]]>` |

---

### 2. Tabela – Estruturas de Dados (Tags e Campos)

#### 2.1 Classe `ESCRITURA`

| Tag / Campo          | Observação                                              | Tipo                          |
| -------------------- | ------------------------------------------------------- | ----------------------------- |
| VERSAO               | Valor fixo “2” – identificação do modelo XML (Tabelião) | Inteiro                       |
| CNS                  | Número do CNS do cartório de notas                      | Inteiro                       |
| NATUREZA             | Natureza do título (lista controlada)                   | Inteiro                       |
| DESCRICAONATUREZA    | Descrição da natureza do titulo.                        | Alfanumérico                  |
| DATAINSTRUMENTO      | Data do instrumento/escritura                           | Data                          |
| LIVRO                | Livro do instrumento/escritura                          | Alfanumérico                  |
| FOLHA                | Folha do instrumento/escritura                          | Alfanumérico                  |
| APRESENTANTE         | Apresentante do título                                  | Classe `APRESENTANTE`         |
| NEGOCIOS             | Lista de negócios                                       | `List<NEGOCIO>`               |
| PARTESNEGOCIO        | Lista de das partes da escritura                        | `List<PARTES>`                |
| FINANCIAMENTO        | Dados do financiamento                                  | Classe `FINANCIAMENTO`        |
| CEDULA               | Dados da cédula                                         | Classe `CEDULA`               |
| REPRESENTANTES       | Representantes                                          | `List<REPRESENTANTE>`         |
| IMPOSTOS             | Impostos (ITBI, DAJE etc.)                              | Classe `IMPOSTOS`             |
| CLAUSULASDECLARACOES | Cláusulas / Declarações                                 | Classe `CLAUSULASDECLARACOES` |
| AUTORIZACOES         | Autorizações                                            | Classe `AUTORIZACOES`         |

#### 2.2 Classe `APRESENTANTE`

| Tag            | Observação         | Tipo             |
| -------------- | ------------------ | ---------------- |
| NOME           | Nome               | Alfanumérico     |
| CPFCNPJ        | CPF ou CNPJ        | CPF/CNPJ         |
| CEP            | CEP                | Numérico         |
| TIPOLOGRADOURO | Tipo de logradouro | Alfanumérico     |
| LOGRADOURO     | Logradouro         | Alfanumérico     |
| NUMERO         | Número             | Alfanumérico     |
| UNIDADE        | Unidade            | Alfanumérico     |
| BAIRRO         | Bairro             | Alfanumérico     |
| CIDADE         | Cidade             | Alfanumérico     |
| UF             | Unidade federativa | Alfanumérico     |
| CONTATO        | Contato            | Classe `CONTATO` |

#### 2.3 Classe `CONTATO`

| Tag      | Observação | Tipo         |
| -------- | ---------- | ------------ |
| EMAIL    | E-mail     | Alfanumérico |
| DDD      | DDD        | Numérico     |
| TELEFONE | Telefone   | Numérico     |

#### 2.4 Classe `NEGOCIO`

| Tag / Campo        | Observação                              | Tipo           |
| ------------------ | --------------------------------------- | -------------- |
| SEQUENCIAL         | Sequência do negócio (chave de vínculo) | Inteiro        |
| TIPOATO            | Tipo de ato (lista controlada)          | Inteiro        |
| DESCRICAOTIPOATO   | Descrição do tipo de ato                | Alfanumérico   |
| VALORTRANSMISSAO   | Valor da transmissão                    | Monetário      |
| VALORVENAL         | Valor venal                             | Monetário      |
| VALORFINANCIAMENTO | Valor do financiamento                  | Monetário      |
| VALORAVALIACAO     | Valor de avaliação do imóvel            | Monetário      |
| VALORLEILAO        | Valor de leilão                         | Monetário      |
| RECURSOSPROPRIOS   | Recursos próprios                       | Monetário      |
| RECURSOSFINANCIADO | Recursos financiados                    | Monetário      |
| PRIMEIRAAQUISICAO  | Primeira aquisição?                     | Booleano       |
| PAGOEMESPECIE      | Pagamento em espécie?                   | Booleano       |
| VALORPAGOEMESPECIE | Valor pago em espécie                   | Monetário      |
| OBSERVACOESGERAIS  | Observações                             | Texto          |
| IMOVEIS            | Imóveis vinculado                       | `List<IMOVEL>` |
| PARTES             | Partes deste ato                        | `List<PARTE>`  |

#### 2.5 Classe `IMOVEL`

| Tag                           | Observação                                                | Tipo         |
| ----------------------------- | --------------------------------------------------------- | ------------ |
| CNS                           | CNS do Registro de Imóveis                                | Inteiro      |
| LOCALIZACAO                   | 1 = Urbano / 2 = Rural (lista constrolada)                | Inteiro      |
| DESCRICAOLOCALIZACAO          | Descrição da localizacao                                  | Alfanumérico |
| NUMEROREGISTRO                | Número de registro                                        | Inteiro      |
| IPTU                          | Número do IPTU                                            | Alfanumérico |
| CCIR                          | Número do CCIR                                            | Alfanumérico |
| NIRF                          | Número do NIRF                                            | Alfanumérico |
| LIVROREGISTROIMOVEIS          | Livro do registro de imoveis referente (lista controlada) | Inteiro      |
| DESCRICAOLIVROREGISTROIMOVEIS | Descrição do Livro do registro de imoveis referente       | Alfanumérico |
| TIPOIMOVEL                    | Tipo de imóvel (lista controlada)                         | Inteiro      |
| DESCRICAOTIPOIMOVEL           | Descrição tipo de imóvel                                  | Alfanumérico |
| DESCRICAO                     | Texto descrevendo o imóvel e confrontações                | Alfanumérico |
| VALORAVALICACAO               | Valor de avaliação do imóvel                              | Monetário    |
| VALORATRIBUIDO                | Valor atribuído ao imóvel                                 | Monetário    |
| TIPOLOGRADOURO                | Tipo de logradouro                                        | Alfanumérico |
| LOGRADOURO                    | Logradouro                                                | Alfanumérico |
| NUMERO                        | Número                                                    | Alfanumérico |
| UNIDADE                       | Unidade                                                   | Alfanumérico |
| BAIRRO                        | Bairro                                                    | Alfanumérico |
| CIDADE                        | Cidade                                                    | Alfanumérico |
| UF                            | UF                                                        | Alfanumérico |
| LOTE                          | Lote                                                      | Alfanumérico |
| QUADRA                        | Quadra                                                    | Alfanumérico |
| TORRE                         | Torre                                                     | Alfanumérico |
| NOMELOTEAMENTO                | Nome do loteamento                                        | Alfanumérico |
| NOMECONDOMINIO                | Nome do condomínio                                        | Alfanumérico |
| COMPLEMENTO                   | Complemento                                               | Alfanumérico |

#### 2.6 Classe `PARTE`

| Tag                   | Observação                      | Tipo         |
| --------------------- | ------------------------------- | ------------ |
| QUALIFICACAO          | Qualificação (lista controlada) | Inteiro      |
| DESCRICAOQUALIFICACAO | Descricao da qualificação       | Alfanumérico |
| CPFCNPJ               | CPF / CNPJ                      | CPF/CNPJ     |
| FRACAO                | Fração                          | Flutuante    |

#### 2.7 Classe `FINANCIAMENTO` (DADOS)

| Tag                                 | Observação                                             | Tipo         |
| ----------------------------------- | ------------------------------------------------------ | ------------ |
| PRAZOCARENCIA                       | Prazo de carência                                      | Inteiro      |
| ENQUADRAMENTOFINANCIAMENTO          | Enquadramento (lista controlada)                       | Inteiro      |
| DESCRICAOENQUADRAMENTOFINANCIAMENTO | Descricao do enquadramento (lista controlada)          | Alfanumérico |
| SISTEMAAMORTIZACAO                  | Descricao do Sistema de amortização (lista controlada) | Inteiro      |
| DESCRICAOSISTEMAAMORTIZACAO         | Sistema de amortização                                 | Alfanumérico |
| ORIGEMRECURSOS                      | Origem dos recursos                                    | Inteiro      |
| DESCRICAOORIGEMRECURSOS             | Descricao do Origem dos recursos                       | Alfanumérico |
| JUROSANUALNOMINAL                   | Juros anual nominal                                    | Flutuante    |
| JUROSANUALEFETIVO                   | Juros anual efetivo                                    | Flutuante    |
| JUROSMENSALNOMINAL                  | Juros mensal nominal                                   | Flutuante    |
| JUROSMENSALEFETIVO                  | Juros mensal efetivo                                   | Flutuante    |
| PRAZOAMORTIZACAO                    | Prazo de amortização                                   | Inteiro      |
| VLPRIMEIRAPARCELA                   | Valor da primeira parcela                              | Monetário    |
| DTPRIMEIRAPARCELA                   | Data da primeira parcela                               | Data         |
| DESTFINANCIAMENTO                   | Destino do financiamento                               | Alfanumérico |
| FORMADEPAGAMENTO                    | Forma de pagamento                                     | Alfanumérico |

#### 2.8 Classe `PARTES` (vínculo Parte × Negócio)

| Tag                  | Observação                                                   | Tipo         |
| -------------------- | ------------------------------------------------------------ | ------------ |
| SEQUENCIALNEGOCIO    | Lista de sequenciais do(s) negócio(s) (ex.: “1,2,3”)         | Alfanumérico |
| NOME                 | Nome                                                         | Alfanumérico |
| CPFCNPJ              | CPF / CNPJ                                                   | CPF/CNPJ     |
| GENERO               | Gênero (1 = Masc., 2 = Fem.) (lista controlada)              | Inteiro      |
| DESCRICAOGENERO      | Descrição do gênero (1 = Masc., 2 = Fem.) (lista controlada) | Alfanumérico |
| DOCUMENTO            | Documento                                                    | Alfanumérico |
| ORGAOEMISSOR         | Órgão emissor                                                | Alfanumérico |
| NACIONALIDADE        | Nacionalidade                                                | Alfanumérico |
| ESTADOCIVIL          | Estado civil (lista controlada)                              | Inteiro      |
| DESCRICAOESTADOCIVIL | Descricao estado civil                                       | Alfanumérico |
| REGIMEBENS           | Regime de bens (lista controlada)                            | Inteiro      |
| DESCRICAOREGIMEBENS  | Descricao do regime de bens                                  | Alfanumérico |
| DTCASAMENTO          | Data do casamento                                            | Data         |
| DTNASCIMENTO         | Data de nascimento                                           | Data         |
| NRPACTO              | Nº do pacto                                                  | Alfanumérico |
| DTPACTO              | Data do pacto                                                | Data         |
| LOCALREGISTROPACTO   | Local do registro do pacto                                   | Alfanumérico |
| UNIAOESTAVEL         | 1 = Sim / 0 = Não                                            | Booleano     |
| PROFISSAO            | Profissão (lista controlada)                                 | Inteiro      |
| CEP / LOGRADOURO …   | Todos os campos de endereço (mesmo layout de APRESENTANTE)   | —            |
| CPFCONJUGE           | CPF do cônjuge                                               | CPF          |
| EMAIL                | E-mail                                                       | Alfanumérico |
| FILIACAO1            | Nome do 1º genitor                                           | Alfanumérico |
| FILIACAO2            | Nome do 2º genitor                                           | Alfanumérico |

#### 2.9 Classe `REPRESENTANTE` (INSTRUMENTO)

| Tag                | Observação                          | Tipo         |
| ------------------ | ----------------------------------- | ------------ |
| NOME_REPRESENTANTE | Nome do representante               | Alfanumérico |
| REPRESENTANTE      | CPF do representante                | CPF          |
| REPRESENTADO       | CNPJ do representado                | CNPJ         |
| NUMERO             | Nº do instrumento                   | Alfanumérico |
| TIPOREGISTRO       | Tipo de registro (lista controlada) | Inteiro      |
| ORGAO              | Órgão                               | Alfanumérico |
| FORMAREGISTRO      | Forma de registro                   | Alfanumérico |
| NUMEROLIVRO        | Nº do livro                         | Alfanumérico |
| FOLHA              | Folha                               | Numérico     |
| NUMEROREGISTRO     | Nº do registro                      | Inteiro      |
| DATAREGISTRO       | Data do registro                    | Data         |

#### 2.10 Classe `CEDULA`

| Tag                    | Observação                                        | Tipo         |
| ---------------------- | ------------------------------------------------- | ------------ |
| IDENTIFICACAOCEDULA    | Identificação da cédula                           | Alfanumérico |
| TIPOCEDULA             | 1 = Integral / 2 = Fracionária (lista controlada) | Inteiro      |
| DESCRICAOTIPOCEDULA    | Descrição do tipo da cédula                       | Alfanumérico |
| NUMERO                 | Nº da cédula                                      | Alfanumérico |
| FRACAO                 | Fração                                            | Flutuante    |
| SERIE                  | Série                                             | Alfanumérico |
| ESPECIECEDULA          | 1 = Cartular / 2 = Escritural (lista controlada)  | Inteiro      |
| DESCRICAOESPECIECEDULA | Descrição da espécie da cédula                    | Alfanumérico |
| CUSTODIANTE_EMISSOR    | Custodiante emissor                               | Alfanumérico |

#### 2.11 Classe `IMPOSTOTRANSMISSAO`

| Tag       | Observação      | Tipo         |
| --------- | --------------- | ------------ |
| ISENCAO   | Possui isenção? | Booleano     |
| INSCRICAO | Nº da inscrição | Alfanumérico |
| GUIA      | Nº da guia      | Alfanumérico |
| VALOR     | Valor pago      | Monetário    |

#### 2.12 Classe `DAJE`

| Tag     | Observação | Tipo         |
| ------- | ---------- | ------------ |
| EMISSOR | Emissor    | Alfanumérico |
| SERIE   | Série      | Alfanumérico |
| NUMERO  | Número     | Alfanumérico |
| VALOR   | Valor      | Monetário    |

#### 2.13 Classe `CLAUSULASDECLARACOES`

| Tag                  | Observação                       | Tipo                      |
| -------------------- | -------------------------------- | ------------------------- |
| VERIFICACAODAPARTES  | Lista de verificações de partes  | List<VERIFICACAODAPARTE>  |
| VERIFICACAODOIMOVEIS | Lista de verificações de imóveis | List<VERIFICACAODOIMOVEL> |

##### 2.13.1 `VERIFICACAODAPARTE`

| Tag       | Observação               | Tipo     |
| --------- | ------------------------ | -------- |
| PARTE     | CPF / CNPJ da parte      | CPF/CNPJ |
| DESCREVER | Descrição da verificação | Texto    |

##### 2.13.2 `VERIFICACAODOIMOVEL`

| Tag       | Observação                                  | Tipo    |
| --------- | ------------------------------------------- | ------- |
| IMOVEL    | Nº de registro (ref. IMOVEL.NUMEROREGISTRO) | Inteiro |
| DESCREVER | Descrição da verificação                    | Texto   |

#### 2.14 Classe `AUTORIZACOES`

| Tag      | Observação           | Tipo  |
| -------- | -------------------- | ----- |
| DECLARO  | Texto da declaração  | Texto |
| AUTORIZO | Texto da autorização | Texto |

### 3. Tabela – Listas Controladas

#### 3.1 NATUREZA

| Código | Descrição         |
| ------ | ----------------- |
| 4      | Escritura pública |

#### 3.2 TIPOATO

| Código | Descrição                |
| -----: | ------------------------ |
|      1 | Venda e compra           |
|      2 | Hipoteca                 |
|      3 | Alienação fiduciária     |
|     10 | Doação                   |
|     11 | Usufruto                 |
|     12 | Inventário               |
|     13 | Part. Separação/Divórcio |
|     14 | Dação em pagamento       |
|     15 | Permuta                  |
|     16 | Conferência de bens      |
|     17 | Bem de família           |

#### 3.3 CAPACIDADECIVIL

| Código | Descrição           |
| -----: | ------------------- |
|      1 | Capaz               |
|      2 | Relativamente capaz |
|      3 | Incapaz             |

#### 3.4 ENQUADRAMENTOFINANCIAMENTO

| Código | Descrição           |
| -----: | ------------------- |
|      1 | SFH taxa tabelada   |
|      2 | SFH taxa de mercado |
|      3 | PMCMV               |
|      4 | SFI                 |
|      5 | Outro               |

#### 3.5 SISTEMAAMORTIZACAO

| Código | Descrição                          |
| -----: | ---------------------------------- |
|      1 | SAC                                |
|      2 | SACRE                              |
|      3 | PRICE                              |
|      4 | Outro                              |
|      5 | Complementar em informações gerais |

#### 3.6 ORIGEMRECURSOS

| Código | Descrição   |
| -----: | ----------- |
|      1 | Não utiliza |
|      2 | FAR         |
|      3 | FGTS        |
|      4 | FGTS/UNIÃO  |
|      5 | SBPE        |
|      6 | Privados    |

#### 3.7 QUALIFICACAO

| Código | Descrição            |
| -----: | -------------------- |
|      1 | Adquirente           |
|      2 | Avalista             |
|      3 | Credor               |
|      4 | Depositário          |
|      5 | Devedor              |
|      6 | Incorporado          |
|      7 | Incorporador         |
|      8 | Interessado          |
|      9 | Interveniente        |
|     10 | Proprietário         |
|     11 | Requerente           |
|     12 | Transmitente         |
|     13 | Anuente              |
|     14 | Representante Credor |

#### 3.8 ESTADOCIVIL

| Código | Descrição                |
| -----: | ------------------------ |
|      1 | casada                   |
|      2 | Casado                   |
|      3 | divorciada               |
|      4 | divorciado               |
|      5 | Espólio                  |
|      6 | separada                 |
|      7 | separada judicialmente   |
|      8 | separado                 |
|      9 | separado judicialmente   |
|     10 | Solteira                 |
|     11 | solteira, maior          |
|     12 | solteira, menor impúbere |
|     13 | solteira, menor púbere   |
|     14 | Solteiro                 |
|     15 | solteiro, maior          |
|     16 | solteiro, menor impúbere |
|     17 | solteiro, menor púbere   |
|     18 | Viúva                    |
|     19 | Viúvo                    |
|     20 | menor emancipado         |
|     21 | Outros                   |

#### 3.9 REGIMEBENS

| Código | Descrição                                                     |
| -----: | ------------------------------------------------------------- |
|      1 | comunhão de bens                                              |
|      2 | comunhão de bens vigente na Venezuela                         |
|      3 | comunhão parcial de bens                                      |
|      4 | comunhão parcial de bens às Leis da Noruega                   |
|      5 | comunhão parcial de bens, à Lei Suíça                         |
|      6 | comunhão parcial de bens, antes da vigência da Lei 6.515/77   |
|      7 | comunhão parcial de bens, na vigência da Lei 6.515/77         |
|      8 | comunhão universal de bens                                    |
|      9 | comunhão universal de bens, antes da vigência da Lei 6.515/77 |
|     10 | comunhão universal de bens, às Leis de Angola                 |
|     11 | comunhão universal de bens, às Leis italianas                 |
|     12 | comunhão universal de bens, na vigência da Lei 6.515/77       |
|     13 | conforme a lei vigente em Israel                              |
|     14 | Leis da Alemanha                                              |
|     15 | Leis da Argentina                                             |
|     16 | Leis da Austrália                                             |
|     17 | Leis da Bolívia                                               |
|     18 | Leis da China                                                 |
|     19 | Leis da Colômbia                                              |
|     20 | Leis da Costa do Marfim                                       |
|     21 | Leis da Costa Rica                                            |
|     22 | Leis da Dinamarca                                             |
|     23 | Leis da Espanha                                               |
|     24 | Leis da Finlândia                                             |
|     25 | Leis da França                                                |
|     26 | Leis da Guatemala                                             |
|     27 | Leis da Holanda                                               |
|     28 | Leis da Inglaterra                                            |
|     29 | Leis da Itália                                                |
|     30 | Leis da Jordania                                              |
|     31 | Leis da Jordânia                                              |
|     32 | Leis da Polonia                                               |
|     33 | Leis da República da Coréia                                   |
|     34 | Leis da Suíça                                                 |
|     35 | Leis de Angola                                                |
|     36 | Leis de Cuba                                                  |
|     37 | Leis de Moscou                                                |
|     38 | Leis de Taiwan                                                |
|     39 | Leis do Canadá                                                |
|     40 | Leis do Japão                                                 |
|     41 | Leis do Líbano                                                |
|     42 | Leis do Paraguai                                              |
|     43 | Leis do Uruguai                                               |
|     44 | Leis dos Estados Unidos                                       |
|     45 | Leis Egípcias                                                 |
|     46 | Leis Portuguesas                                              |
|     47 | participação final nos aquestos                               |
|     48 | regime de bens conforme as Leis americanas                    |
|     49 | regime vigente no Chile                                       |
|     50 | separação de bens                                             |
|     51 | separação de bens conforme as Leis da Áustria                 |
|     52 | separação de bens, antes da vigência da Lei 6.515/77          |
|     53 | separação de bens, na vigência da Lei 6.515/77                |
|     54 | separação obrigatória de bens                                 |
|     55 | separação parcial, antes da vigência da Lei 6.515/77          |
|     56 | separação parcial, na vigência da Lei 6.515/77                |
|     57 | separação total de bens, na vigência da Lei 6.515/77          |

#### 3.10 LIVROREGISTROIMOVEIS

| Código | Descrição                            |
| -----: | ------------------------------------ |
|      1 | Lv. 2 – Registro Geral (matrícula)   |
|      2 | Lv. 3 – Transcrição das Transmissões |

### 3.11 LOCALIZACAO

| Código | Descrição |
| -----: | --------- |
|      1 | urbano    |
|      2 | rural     |

#### 3.12 GENERO

| Código | Descrição |
| -----: | --------- |
|      1 | Masculino |
|      2 | Feminino  |

#### 3.13 TIPOINSTRUMENTO

| Código | Descrição                |
| -----: | ------------------------ |
|      1 | contrato social          |
|      2 | estatuto social          |
|      3 | ata de assembleia        |
|      4 | ata de reunião de sócios |
|      5 | procuração               |
|      6 | outro                    |

#### 3.14 TIPOCEDULA

| Código | Descrição   |
| -----: | ----------- |
|      1 | Integral    |
|      2 | Fracionária |

#### 3.15 ESPECIECEDULA

| Código | Descrição  |
| -----: | ---------- |
|      1 | Cartular   |
|      2 | Escritural |

#### 3.16 TIPOIMOVEL

| Código | Descrição           |
| -----: | ------------------- |
|      1 | Apartamento         |
|      2 | Área de Terra       |
|      3 | Área de terras      |
|      4 | Armazém             |
|      5 | Bangalô             |
|      6 | Barracão            |
|      7 | Casa de moradia     |
|      8 | Chácara             |
|      9 | Chalé               |
|     10 | Cômodo comercial    |
|     11 | Conjunto            |
|     12 | Depósito            |
|     13 | Edícula             |
|     14 | Fazenda             |
|     15 | Galpão              |
|     16 | Garagem             |
|     17 | Gleba de terra      |
|     18 | Kitchenette         |
|     19 | Loja                |
|     20 | Prédio              |
|     21 | Prédio comercial    |
|     22 | Prédio p/ indústria |
|     23 | Prédio residencial  |
|     24 | Quinhão de terra    |
|     25 | Rua particular      |
|     26 | Sala                |
|     27 | Salão               |
|     28 | Sítio               |
|     29 | Sobreloja           |
|     30 | Terreno             |
|     31 | Unid. res. autônoma |
|     32 | Unidade Autônoma    |
|     33 | Unidade residencial |
