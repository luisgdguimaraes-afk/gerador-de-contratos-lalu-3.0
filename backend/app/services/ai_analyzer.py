"""
Serviço para análise inteligente usando modelo de linguagem
"""
import os
import json
from openai import OpenAI
from typing import List, Dict
from app.models.schemas import FieldInfo, FieldType
from dotenv import load_dotenv

load_dotenv()


class AIAnalyzer:
    """Usa IA para analisar contexto e gerar labels inteligentes"""
    
    def __init__(self):
        # Garantir que o .env seja carregado do diretório correto
        from pathlib import Path
        import re
        
        # Tentar múltiplos caminhos
        possible_paths = [
            Path(__file__).parent.parent.parent / ".env",  # backend/.env
            Path.cwd() / ".env",  # Diretório atual
            Path(".env"),  # Relativo
        ]
        
        api_key = None
        
        # Primeiro tentar load_dotenv
        for env_path in possible_paths:
            if env_path.exists():
                load_dotenv(dotenv_path=env_path)
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key:
                    break
        
        # Se ainda não encontrou, tentar ler diretamente do arquivo
        if not api_key:
            for env_path in possible_paths:
                if env_path.exists():
                    try:
                        with open(env_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            match = re.search(r'OPENAI_API_KEY\s*=\s*(.+)', content, re.MULTILINE)
                            if match:
                                api_key = match.group(1).strip()
                                # Remover aspas se houver
                                api_key = api_key.strip('"\'')
                                if api_key:
                                    break
                    except Exception as e:
                        print(f"Erro ao ler .env de {env_path}: {e}")
                        continue
        
        if not api_key or api_key.strip() == "" or api_key == "your_openai_api_key_here":
            raise ValueError("OPENAI_API_KEY não configurada no .env. Por favor, edite o arquivo backend/.env e adicione sua chave da OpenAI.")
        
        try:
            # Inicializar cliente OpenAI de forma explícita
            # A versão 2.x da OpenAI tem uma API diferente da 1.x
            import openai
            
            # Verificar versão e inicializar adequadamente
            openai_version = openai.__version__
            print(f"Versão da biblioteca OpenAI: {openai_version}")
            
            # Para versão 2.x, usar apenas api_key
            # Não passar nenhum outro argumento que possa causar conflitos
            if openai_version.startswith('2.'):
                self.client = OpenAI(api_key=api_key)
            else:
                # Fallback para versões mais antigas
                self.client = OpenAI(api_key=api_key)
            
            # Modelo pode ser configurado via variável de ambiente ou usa padrão
            # Opções: gpt-4o-mini (padrão, econômico), gpt-4o, gpt-3.5-turbo
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            print(f"Modelo OpenAI configurado: {self.model}")
        except TypeError as e:
            # Erro específico de argumentos inválidos
            import traceback
            error_trace = traceback.format_exc()
            print(f"Erro de tipo ao inicializar OpenAI: {error_trace}")
            # Tentar inicialização mínima
            try:
                self.client = OpenAI(api_key=api_key)
                self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
                print(f"Modelo OpenAI configurado (fallback): {self.model}")
            except Exception as e2:
                raise ValueError(f"Erro ao inicializar cliente OpenAI: {str(e2)}")
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Erro detalhado ao inicializar OpenAI: {error_trace}")
            raise ValueError(f"Erro ao inicializar cliente OpenAI: {str(e)}")
    
    async def analyze_fields(self, document_text: str, 
                            placeholders: List[Dict]) -> List[FieldInfo]:
        """
        Analisa placeholders e gera informações estruturadas sobre cada campo
        """
        # Preparar contexto para a IA
        context_prompt = self._build_analysis_prompt(document_text, placeholders)
        
        try:
            print(f"Enviando requisição para OpenAI com modelo: {self.model}")
            print(f"Tamanho do prompt: {len(context_prompt)} caracteres")
            print(f"Número de placeholders: {len(placeholders)}")
            
            # Usar o cliente existente diretamente
            # A versão 2.x da OpenAI gerencia timeout internamente
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Você é um especialista em análise de contratos jurídicos e imobiliários.
                        Sua tarefa é analisar campos editáveis em contratos e criar labels descritivos e semânticos.
                        
                        REGRAS IMPORTANTES:
                        1. Crie labels claros e específicos, nunca genéricos como "Campo 1"
                        2. Identifique o tipo correto de cada campo (text, number, currency, date, cpf, cnpj, phone, email)
                        3. Use o contexto ao redor do campo para entender seu significado
                        4. Campos semelhantes devem ter o mesmo field_id (ex: nome do comprador em vários lugares)
                        5. Identifique a seção do contrato (COMPRADOR, VENDEDOR, IMÓVEL, etc.)
                        6. Mantenha o texto jurídico intacto, apenas identifique campos editáveis
                        
                        Retorne APENAS um JSON válido com a lista de campos."""
                    },
                    {
                        "role": "user",
                        "content": context_prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            print("Resposta recebida da OpenAI com sucesso")
            
            # Parsear resposta JSON
            result = json.loads(response.choices[0].message.content)
            fields = result.get("fields", [])
            
            # Converter para FieldInfo
            field_infos = []
            for field_data in fields:
                field_info = FieldInfo(
                    field_id=field_data.get("field_id"),
                    label=field_data.get("label"),
                    type=FieldType(field_data.get("type", "text")),
                    required=field_data.get("required", True),
                    original_text=field_data.get("original_text"),
                    context=field_data.get("context", ""),
                    placeholder=field_data.get("placeholder"),
                    section=field_data.get("section")
                )
                field_infos.append(field_info)
            
            return field_infos
            
        except Exception as e:
            # Log detalhado do erro
            import traceback
            error_trace = traceback.format_exc()
            print(f"Erro na análise de IA: {str(e)}")
            print(f"Traceback: {error_trace}")
            
            # Verificar tipo de erro
            error_str = str(e).lower()
            if "api key" in error_str or "authentication" in error_str:
                raise ValueError("Erro de autenticação com OpenAI. Verifique se a OPENAI_API_KEY está correta.")
            elif "rate limit" in error_str:
                raise ValueError("Limite de requisições da OpenAI atingido. Aguarde alguns minutos e tente novamente.")
            elif "insufficient_quota" in error_str:
                raise ValueError("Cota da OpenAI esgotada. Adicione créditos à sua conta OpenAI.")
            else:
                # Em caso de outros erros, criar campos básicos como fallback
                print("Usando fallback: criando campos básicos sem IA")
                return self._create_fallback_fields(placeholders)
    
    def _build_analysis_prompt(self, document_text: str, 
                               placeholders: List[Dict]) -> str:
        """
        Constrói o prompt para análise pela IA
        """
        # Limitar tamanho do texto para não exceder tokens
        # Aumentado para 12000 para documentos maiores, mas ainda dentro do limite
        max_text_length = 12000
        if len(document_text) > max_text_length:
            print(f"Documento muito grande ({len(document_text)} chars), truncando para {max_text_length}")
            document_text = document_text[:max_text_length] + "..."
        
        placeholder_info = []
        for i, placeholder in enumerate(placeholders):
            placeholder_info.append({
                "index": i,
                "text": placeholder.get("text"),
                "context": placeholder.get("context", "")
            })
        
        prompt = f"""Analise o seguinte contrato e identifique os campos editáveis:

TEXTO DO CONTRATO:
{document_text}

CAMPOS IDENTIFICADOS:
{json.dumps(placeholder_info, indent=2, ensure_ascii=False)}

Para cada campo, forneça:
1. field_id: ID único e semântico (ex: "buyer_name", "property_address")
2. label: Label descritivo em português (ex: "Nome completo do comprador")
3. type: Tipo de dado (text, number, currency, date, cpf, cnpj, phone, email)
4. required: Se é obrigatório (true/false)
5. original_text: O texto placeholder original encontrado
6. context: Contexto ao redor do campo
7. section: Seção do contrato (COMPRADOR, VENDEDOR, IMÓVEL, etc.)

IMPORTANTE: Campos semelhantes devem ter o mesmo field_id.

Retorne um JSON no formato:
{{
  "fields": [
    {{
      "field_id": "buyer_name",
      "label": "Nome completo do comprador",
      "type": "text",
      "required": true,
      "original_text": "xxxxx",
      "context": "...",
      "section": "COMPRADOR"
    }}
  ]
}}"""
        
        return prompt
    
    def _create_fallback_fields(self, placeholders: List[Dict]) -> List[FieldInfo]:
        """
        Cria campos básicos quando a IA falha
        """
        fields = []
        for i, placeholder in enumerate(placeholders):
            field = FieldInfo(
                field_id=f"field_{i+1}",
                label=f"Campo {i+1}",
                type=FieldType.TEXT,
                required=True,
                original_text=placeholder.get("text", ""),
                context=placeholder.get("context", "")
            )
            fields.append(field)
        
        return fields
