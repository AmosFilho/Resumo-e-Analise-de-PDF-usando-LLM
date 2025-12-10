# 🧠 Ferramenta de Resumo e Análise de PDF

## Como rodar o código
1. Instale as dependência do projeto com o comando `pip install -r config/requirements.txt`
2. Baixe o modelo LLLM **Qwen-4B** com o comando `python llm/import_model.py`
3. Adicione os arquivos que serão analisados a pasta cli/pdf_files
4. Inicialize o programa no terminal utilizando o comando `python main.py cli/pdf_files/nome_do_arquivo.pdf`.

### Exemplo de execução
- Use o comando `python main.py cli/pdf_files/example.pdf` no terminal.
- O Comando vai executar o código com o documento **"example.pdf"** como exemplo.

## Descrição

Este projeto é uma ferramenta para **processamento automático de arquivos PDF**, capaz de:

- Extrair **imagens** de PDFs  
- Extrair **texto** página a página  
- Gerar **resumos automáticos** usando um modelo local (Qwen-1.7B) 
- Indentificar **Título** e **Seções** de um documento pdf.
- Criar arquivos de relatório em formato `.md`  
- Registrar **logs unificados** para depuração e auditoria  
- Executar fluxos completos a partir de argumentos de linha de comando

---



## Detalhes a serem avaliados

- Escolha da nomenclatura das variáveis e formatação.
- Consistência do resumo com a realidade do texto presente no documento.
- Resultados da análise do pdf e como foram implementados os métodos
- Modularização dos métodos
- Organização do código
- Comentários explicando seções do código
- Separação de funções
- Organização da estrutura de pastas 
- Cuidado com a formatação da saída para melhor entendimento dos resultados
- Geração de um relatório unificado
