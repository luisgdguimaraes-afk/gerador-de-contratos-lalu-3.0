# Como iniciar a aplicação (preview)

Use este guia **sempre que ligar o computador** ou abrir o projeto de novo. Não é necessário refazer o processo de `taskkill` — depois de desligar o PC, a porta 8000 fica livre.

---

## Importante: um backend por vez

- **Só deve existir um processo** rodando `python run.py` (porta 8000).
- Se você abrir **dois ou mais** terminais e rodar `python run.py` em cada um, vários backends vão disputar a porta e o navegador pode falar com um backend antigo (que gera só 1 PDF). Por isso o preview e o download das Condições Gerais falhavam.
- **Depois de desligar o PC**, não há processos antigos; basta iniciar **uma vez** o backend e o frontend.

---

## Passo a passo (novos terminais)

### 1. Abrir o projeto no Cursor

Abra a pasta do projeto: `Contratos LALU`.

### 2. Terminal 1 — Backend

1. Abra um terminal no Cursor: **Terminal → New Terminal** (ou `` Ctrl+` ``).
2. **Não digite `powershell`** — use o terminal que abriu direto.
3. No terminal, rode **só** estes dois comandos (um por vez):

```powershell
cd "c:\Users\luisg\Downloads\Contratos LALU\Contratos LALU\backend"
python run.py
```

3. Espere aparecer algo como:
   - `INFO: Uvicorn running on http://0.0.0.0:8000`
   - `INFO: Application startup complete.`
4. **Deixe esse terminal aberto.** Não feche nem rode `python run.py` de novo em outro terminal.

### 3. Terminal 2 — Frontend

1. Abra **outro** terminal: **Terminal → New Terminal** (ou clique no **+** na aba do terminal).
2. Rode:

```powershell
cd "c:\Users\luisg\Downloads\Contratos LALU\Contratos LALU\frontend"
npm run dev
```

3. Espere aparecer algo como:
   - `Local: http://localhost:3000`
4. **Deixe esse terminal aberto** também.

### 4. Abrir o preview no navegador

1. Abra o navegador (Chrome, Edge, etc.).
2. Acesse: **http://localhost:3000**
3. Você deve ver a tela do **Gerador de Contratos** (LALU).

### 5. Testar o fluxo completo

1. Preencha o formulário e clique em **Gerar Contrato**.
2. Na tela de download devem aparecer:
   - **Baixar Contrato (PDF)** — Quadro Resumo
   - **Condições Gerais** — PDF das condições gerais
3. Clique em cada botão e confira se os dois PDFs baixam sem erro.

---

## Se a porta 8000 já estiver em uso

Se ao rodar `python run.py` aparecer erro de **porta em uso** (ex.: *Address already in use*):

1. No PowerShell, rode para ver quem está usando a porta 8000:

```powershell
netstat -ano | findstr :8000
```

2. Para **cada** número da última coluna (PID), encerre o processo:

```powershell
taskkill /PID <número_do_PID> /F
```

Exemplo: se aparecer `12345`, rode `taskkill /PID 12345 /F`.

3. Rode de novo:

```powershell
cd "c:\Users\luisg\Downloads\Contratos LALU\Contratos LALU\backend"
python run.py
```

---

## Resumo

| O que fazer | Comando / ação |
|-------------|-----------------|
| **Sempre que ligar o PC** | Não precisa de `taskkill`. Siga os passos 2 e 3 (um terminal para backend, outro para frontend). |
| **Ver o preview** | Abrir http://localhost:3000 no navegador. |
| **Evitar erro de download** | Garantir que só existe **um** `python run.py` rodando (um único terminal para o backend). |

Se algo não funcionar, descreva o que aparece nos terminais (backend e frontend) e no navegador (ou um print) para analisarmos o próximo passo.
