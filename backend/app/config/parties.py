"""
Dados estáticos das partes fixas envolvidas nos contratos do Loteamento
Residencial Rota do Sol.

Estes valores NÃO devem ser expostos no formulário do frontend, pois são
constantes entre todos os contratos gerados. Alterá-los aqui reflete
automaticamente em todos os contratos futuros.
"""

# -----------------------------------------------------------------------------
# VENDEDOR — LALU Administradora de Bens Ltda
# -----------------------------------------------------------------------------
VENDEDOR_LALU = {
    "VENDEDOR_CONTA": "577590324-9",
    "VENDEDOR_AGENCIA": "0368",
    "VENDEDOR_BANCO_NOME": "Caixa Econômica Federal",
    "VENDEDOR_BANCO_CODIGO": "104",
    "VENDEDOR_PIX": "08.296.247/0001-09",
}

# Dict consolidado para uso no pipeline de preenchimento.
STATIC_PARTIES: dict[str, str] = {
    **VENDEDOR_LALU,
}

