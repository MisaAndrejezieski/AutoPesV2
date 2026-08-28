# AutoPes V2

Aplicativo desktop para executar e registrar roteiros de pesquisa configuraveis no Microsoft Edge.

Cada tema segue uma sequencia de perguntas voltada ao estudo: fundamentos, conceitos de
maior impacto (regra 20/80), elementos essenciais, aplicacoes, erros comuns e proximo passo.
Os roteiros podem ser adaptados em `config/settings.json`.

## Requisitos

- Windows com Microsoft Edge instalado
- Python 3.10 ou superior

## Instalação e uso

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Edite `config/settings.json` para ajustar os temas, perguntas e tempos. A ordem das perguntas
e mantida para que cada tema tenha uma progressao didatica. Os resultados sao gravados em
`data/resultados` durante o desenvolvimento; no executavel, ficam em `%LOCALAPPDATA%\AutoPesV2`.

## Segurança operacional

O aplicativo abre o Edge com um perfil isolado e encerra exclusivamente a árvore de processos que ele mesmo iniciou. Suas janelas e sessões pessoais do Edge não são fechadas.

Mover o cursor para o canto superior esquerdo aciona o mecanismo de segurança do PyAutoGUI. O botão **Parar** também interrompe as esperas imediatamente e salva os resultados parciais.

## Testes

```powershell
python -m unittest discover -s tests -v
```
