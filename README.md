# 🧠 Ferramenta de Resumo e Análise de PDF

## Como rodar o código
1. Instale as dependência do projeto com o comando `pip install -r config/requirements.txt`
2. Adicione os arquivos que serão analisados a pasta cli/pdf_files
3. Inicialize o programa no terminal utilizando o comando `python main.py caminho_do_arquivo.pdf`.

### Exemplo de execução
- Use o comando `python main.py cli/pdf_files/example.pdf` no terminal.

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




## 🚀 Funcionalidades Principais

### **1. Extração de Imagens**
O módulo responsável percorre todas as páginas do PDF e salva cada imagem encontrada em uma pasta dedicada:
