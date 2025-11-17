import subprocess
import os
import re
from pathlib import Path

class MermaidBPMNConverter:
    """
    BPMN diagram converter in Mermaid.js to SVG
    Based on the approach in the article by Klievtsova et al. (2024)
    """

    def __init__(self):
        self.mermaid_cli_installed = self._check_mermaid_cli()

    def _check_mermaid_cli(self):        
        try:
            subprocess.run(['mmdc', '--version'],
                          capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def clean_mermaid_code(self, text):    
        
        pattern = r'```(?:mermaid)?\s*(graph.*?)```'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        if matches:
            mermaid_code = matches[0]
        else:            
            pattern = r'(graph\s+(?:TD|LR|TB|RL).*?)(?:\n\n|\Z)'
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            mermaid_code = matches[0] if matches else text
        
        mermaid_code = mermaid_code.strip()

        return mermaid_code

    def validate_mermaid_syntax(self, mermaid_code):
        """
        Valida sintaxe básica do Mermaid
        """
        if not mermaid_code.strip().startswith('graph'):
            return False, 
        lines = mermaid_code.split('\n')
        if len(lines) < 2:
            return False, 

        return True, 

    def convert_to_svg(self, mermaid_code, output_file='bpmn_diagram.svg'):
        """
        Converte código Mermaid para SVG usando Mermaid CLI
        """
        if not self.mermaid_cli_installed:
            return self._convert_using_api(mermaid_code, output_file)
        
        temp_file = 'temp_mermaid.mmd'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)

        try:
            subprocess.run([
                'mmdc',
                '-i', temp_file,
                '-o', output_file,
                '-b', 'transparent'
            ], check=True, capture_output=True, text=True)

            os.remove(temp_file)
            return True, f"SVG gerado com sucesso: {output_file}"

        except subprocess.CalledProcessError as e:
            os.remove(temp_file)
            return False, f"Erro na conversão: {e.stderr}"

    def _convert_using_api(self, mermaid_code, output_file):
        """
        Alternativa: gera HTML com renderização via Mermaid.js
        Útil quando CLI não está instalado
        """
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f5f5f5;
        }}
        .mermaid {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="mermaid">
{mermaid_code}
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true
            }}
        }});
    </script>
</body>
</html>"""

        html_file = output_file.replace('.svg', '.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return True, f"HTML gerado: {html_file}\nAbra no navegador para visualizar.\nPara SVG, instale: npm install -g @mermaid-js/mermaid-cli"

    def process_llm_response(self, llm_response, output_file='bpmn_diagram.svg'):
        print("=== Processando resposta do LLM ===\n")
        mermaid_code = self.clean_mermaid_code(llm_response)

        is_valid, message = self.validate_mermaid_syntax(mermaid_code)
        if not is_valid:
            print(f"✗ Erro: {message}")
            return False

        success, message = self.convert_to_svg(mermaid_code, output_file)
        print(f"{'✓' if success else '✗'} {message}\n")

        return success


# EXAMPLE OF USE - Based on the diagram in Figure 1 of the article.

import subprocess
import os
import re
from pathlib import Path

class MermaidBPMNConverter:
    """
    Conversor de diagramas BPMN em Mermaid.js para SVG
    Baseado na abordagem do artigo de Klievtsova et al. (2024)
    """

    def __init__(self):
        self.mermaid_cli_installed = self._check_mermaid_cli()

    def _check_mermaid_cli(self):
        """Verifica se o Mermaid CLI está instalado"""
        try:
            subprocess.run(['mmdc', '--version'],
                          capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def clean_mermaid_code(self, text):
        """
        Extrai e limpa código Mermaid de uma resposta de LLM
        """
        # Remove blocos de código markdown
        pattern = r'```(?:mermaid)?\s*(graph.*?)```'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        if matches:
            mermaid_code = matches[0]
        else:
            # Se não encontrou em blocos, tenta encontrar graph direto
            pattern = r'(graph\s+(?:TD|LR|TB|RL).*?)(?:\n\n|\Z)'
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            mermaid_code = matches[0] if matches else text

        # Limpeza básica
        mermaid_code = mermaid_code.strip()

        return mermaid_code

    def validate_mermaid_syntax(self, mermaid_code):
        """
        Valida sintaxe básica do Mermaid
        """
        if not mermaid_code.strip().startswith('graph'):
            return False, "Código deve começar com 'graph TD', 'graph LR', etc."

        # Verifica estrutura básica
        lines = mermaid_code.split('\n')
        if len(lines) < 2:
            return False, "Código muito curto, deve ter pelo menos 2 linhas"

        return True, "Sintaxe válida"

    def convert_to_svg(self, mermaid_code, output_file='bpmn_diagram.svg'):
        """
        Converte código Mermaid para SVG usando Mermaid CLI
        """
        if not self.mermaid_cli_installed:
            return self._convert_using_api(mermaid_code, output_file)

        # Salva código temporário
        temp_file = 'temp_mermaid.mmd'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)

        try:
            # Executa conversão
            subprocess.run([
                'mmdc',
                '-i', temp_file,
                '-o', output_file,
                '-b', 'transparent'
            ], check=True, capture_output=True, text=True)

            os.remove(temp_file)
            return True, f"SVG gerado com sucesso: {output_file}"

        except subprocess.CalledProcessError as e:
            os.remove(temp_file)
            return False, f"Erro na conversão: {e.stderr}"

    def _convert_using_api(self, mermaid_code, output_file):
        """
        Alternativa: gera HTML com renderização via Mermaid.js
        Útil quando CLI não está instalado
        """
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f5f5f5;
        }}
        .mermaid {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="mermaid">
{mermaid_code}
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true
            }}
        }});
    </script>
</body>
</html>"""

        html_file = output_file.replace('.svg', '.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return True, f"HTML gerado: {html_file}\nAbra no navegador para visualizar.\nPara SVG, instale: npm install -g @mermaid-js/mermaid-cli"

    def process_llm_response(self, llm_response, output_file='bpmn_diagram.svg'):
        """
        Pipeline completo: limpa, valida e converte resposta do LLM
        """
        print("=== Processando resposta do LLM ===\n")

        # 1. Extrair código Mermaid
        print("1. Extraindo código Mermaid...")
        mermaid_code = self.clean_mermaid_code(llm_response)
        print(f"✓ Código extraído ({len(mermaid_code)} caracteres)\n")

        # 2. Validar sintaxe
        print("2. Validando sintaxe...")
        is_valid, message = self.validate_mermaid_syntax(mermaid_code)
        if not is_valid:
            print(f"✗ Erro: {message}")
            return False
        print(f"✓ {message}\n")

        # 3. Converter para SVG
        print("3. Convertendo para SVG...")
        success, message = self.convert_to_svg(mermaid_code, output_file)
        print(f"{'✓' if success else '✗'} {message}\n")

        # 4. Mostrar código
        print("=== Código Mermaid Processado ===")
        print(mermaid_code)
        print("\n" + "="*50)

        return success


# ================= 
# EXAMPLE OF USE  
# ================= 

converter = MermaidBPMNConverter()
text = '''
```mermaid
      graph TD

    %% --- SWIMLANES ---
    subgraph Guest["Guest"]
        G_Start([Guest arrives at reception])
        G_GoesRoom[Go to the room]
        G_RequestsServices[Request additional services]
        G_Checkout[Return to reception for checkout]
        G_End([End of stay])
    end

    subgraph Reception["Front Desk"]
        R_CheckReservation[Verify reservation in system]
        R_ReservationValid{Is reservation valid?}
        R_RequestDocs[Request identification documents]
        R_CheckIn[Perform check-in and deliver key/card]
        R_InformNoReservation[Inform guest and offer options]
        R_FinalizeBill[Finalize bill and charge additional services]
        R_CheckoutIssues{Any issues with billing or room handover?}
        R_ResolveIssues[Resolve issues before completing checkout]
    end

    subgraph Housekeeping["Housekeeping"]
        H_CheckRoom[Check if room is clean and ready]
    end

    %% --- PROCESS FLOW ---
    G_Start --> R_CheckReservation
    R_CheckReservation --> R_ReservationValid

    R_ReservationValid -->|Yes| R_RequestDocs
    R_RequestDocs --> R_CheckIn
    R_CheckIn --> G_GoesRoom
    G_GoesRoom --> H_CheckRoom

    R_ReservationValid -->|No| R_InformNoReservation

    %% During stay
    G_GoesRoom --> G_RequestsServices

    %% Checkout
    G_RequestsServices --> G_Checkout
    G_Checkout --> R_FinalizeBill
    R_FinalizeBill --> R_CheckoutIssues

    R_CheckoutIssues -->|Yes| R_ResolveIssues
    R_ResolveIssues --> R_FinalizeBill

    R_CheckoutIssues -->|No| G_End

    %% --- STYLES ---
    style G_Start fill:#90EE90,stroke:#333,stroke-width:2px
    style G_End fill:#FFB6C6,stroke:#333,stroke-width:2px
    style R_ReservationValid fill:#E6E6FA,stroke:#333,stroke-width:2px
    style R_CheckoutIssues fill:#E6E6FA,stroke:#333,stroke-width:2px


```
'''
converter.process_llm_response(text, 'my_diagram.svg')
