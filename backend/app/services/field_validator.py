"""
Serviço para validação de campos do formulário
"""
import re
from typing import Dict, Any


class FieldValidator:
    """Valida valores de campos conforme seus tipos"""
    
    def validate_fields(self, fields: Dict[str, Any]):
        """
        Valida todos os campos fornecidos
        Levanta exceção se algum campo for inválido
        """
        for field_id, value in fields.items():
            # Pular campos vazios ou None (não são obrigatórios para validação)
            if value is None or value == "" or (isinstance(value, str) and value.strip() == ""):
                continue
            
            # Determinar tipo baseado no field_id ou valor
            field_type = self._infer_field_type(field_id, value)
            
            try:
                if field_type == "cpf":
                    self._validate_cpf(value)
                elif field_type == "cnpj":
                    self._validate_cnpj(value)
                elif field_type == "email":
                    self._validate_email(value)
                elif field_type == "phone":
                    self._validate_phone(value)
                elif field_type == "date":
                    self._validate_date(value)
                elif field_type == "currency":
                    self._validate_currency(value)
                elif field_type == "number":
                    self._validate_number(value)
            except ValueError as e:
                # Adicionar field_id ao erro para facilitar debug
                raise ValueError(f"Campo '{field_id}': {str(e)}")
    
    def _infer_field_type(self, field_id: str, value: Any) -> str:
        """
        Infere o tipo do campo baseado no field_id
        """
        field_id_lower = field_id.lower()
        
        if "cpf" in field_id_lower:
            return "cpf"
        elif "cnpj" in field_id_lower:
            return "cnpj"
        elif "email" in field_id_lower or "e-mail" in field_id_lower:
            return "email"
        elif ("phone" in field_id_lower or "telefone" in field_id_lower) and "ddd" not in field_id_lower:
            # Só valida como telefone se não for campo de DDD
            return "phone"
        elif ("date" in field_id_lower or "data" in field_id_lower) and "dia" not in field_id_lower and "mes" not in field_id_lower and "ano" not in field_id_lower:
            # Só valida como data se não for campo de dia, mês ou ano separado
            return "date"
        elif ("currency" in field_id_lower or "valor" in field_id_lower or "preco" in field_id_lower) and "extenso" not in field_id_lower:
            # Só valida como currency se não for campo de valor por extenso
            return "currency"
        elif "number" in field_id_lower or "numero" in field_id_lower:
            return "number"
        
        return "text"
    
    def _validate_cpf(self, value: str):
        """Valida CPF"""
        if not value:
            return
        
        # Remover formatação
        cpf = re.sub(r'\D', '', str(value))
        
        if len(cpf) != 11:
            raise ValueError(f"CPF inválido: deve ter 11 dígitos")
        
        # Validar dígitos verificadores
        if not self._validate_cpf_digits(cpf):
            raise ValueError(f"CPF inválido: dígitos verificadores incorretos")
    
    def _validate_cpf_digits(self, cpf: str) -> bool:
        """Valida dígitos verificadores do CPF"""
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        # Calcular primeiro dígito
        sum = 0
        for i in range(9):
            sum += int(cpf[i]) * (10 - i)
        digit1 = 11 - (sum % 11)
        if digit1 >= 10:
            digit1 = 0
        
        if digit1 != int(cpf[9]):
            return False
        
        # Calcular segundo dígito
        sum = 0
        for i in range(10):
            sum += int(cpf[i]) * (11 - i)
        digit2 = 11 - (sum % 11)
        if digit2 >= 10:
            digit2 = 0
        
        return digit2 == int(cpf[10])
    
    def _validate_cnpj(self, value: str):
        """Valida CNPJ"""
        if not value:
            return
        
        # Remover formatação
        cnpj = re.sub(r'\D', '', str(value))
        
        if len(cnpj) != 14:
            raise ValueError(f"CNPJ inválido: deve ter 14 dígitos")
    
    def _validate_email(self, value: str):
        """Valida e-mail"""
        if not value:
            return
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, str(value)):
            raise ValueError(f"E-mail inválido: {value}")
    
    def _validate_phone(self, value: str):
        """Valida telefone (sem DDD, pois DDD é campo separado)"""
        if not value:
            return
        
        # Remover formatação
        phone = re.sub(r'\D', '', str(value))
        
        # Telefone sem DDD pode ter:
        # - 8 dígitos (telefone fixo)
        # - 9 dígitos (celular com o 9 inicial)
        if len(phone) != 8 and len(phone) != 9:
            raise ValueError(f"Telefone inválido: deve ter 8 dígitos (fixo) ou 9 dígitos (celular)")
    
    def _validate_date(self, value: str):
        """Valida data"""
        if not value:
            return
        
        # Aceitar formatos comuns: DD/MM/YYYY, YYYY-MM-DD
        date_patterns = [
            r'^\d{2}/\d{2}/\d{4}$',
            r'^\d{4}-\d{2}-\d{2}$'
        ]
        
        valid = any(re.match(pattern, str(value)) for pattern in date_patterns)
        if not valid:
            raise ValueError(f"Data inválida: formato deve ser DD/MM/YYYY ou YYYY-MM-DD")
    
    def _validate_currency(self, value: Any):
        """Valida valor monetário"""
        if value is None:
            return
        
        try:
            # Remover formatação de moeda
            if isinstance(value, str):
                value = value.replace('R$', '').replace('.', '').replace(',', '.').strip()
            
            float_value = float(value)
            if float_value < 0:
                raise ValueError("Valor monetário não pode ser negativo")
        except (ValueError, TypeError):
            raise ValueError(f"Valor monetário inválido: {value}")
    
    def _validate_number(self, value: Any):
        """Valida número"""
        if value is None:
            return
        
        try:
            float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Número inválido: {value}")
