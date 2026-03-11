@echo off
REM Script para gerar visualizacao reduzida do grafo - Versao Corrigida
setlocal enabledelayedexpansion

set "PROJECT_DIR=%~dp0"
set "GRAPHS_DIR=%PROJECT_DIR%graphs"
set "PDF_DIR=%GRAPHS_DIR%\PDF"
set "DOT_SCRIPT=%PROJECT_DIR%dot\dot.py"
set "INPUT_DOT=%GRAPHS_DIR%\grafo_curto.dot"
set "OUTPUT_PDF=%PDF_DIR%\resultado_teste.pdf"

echo ===============================================
echo    GERADOR DE VISUALIZACAO (AMOSTRA REDUZIDA)
echo ===============================================

REM 1. Garante que a pasta PDF existe
if not exist "%PDF_DIR%" (
    echo [INFO] Criando pasta PDF em: %PDF_DIR%
    mkdir "%PDF_DIR%"
)

REM 2. Deteccao de Python
set "PYEXEC="
py --version >nul 2>&1 && set "PYEXEC=py"
if not defined PYEXEC python --version >nul 2>&1 && set "PYEXEC=python"

if not defined PYEXEC (
    echo [ERRO] Python nao encontrado.
    pause
    exit /b 1
)

echo [1/2] Executando dot.py...
"!PYEXEC!" "%DOT_SCRIPT%"

echo.
echo [2/2] Renderizando PDF via Graphviz (SFDP)...
echo [INFO] Salvando em: %OUTPUT_PDF%

REM 3. Deteccao do Graphviz (Modificado para evitar erro de parenteses)
set "GRAPHVIZ_BIN="

if exist "C:\Program Files (x86)\Graphviz\bin" set "GRAPHVIZ_BIN=C:\Program Files (x86)\Graphviz\bin"
if not defined GRAPHVIZ_BIN if exist "C:\Program Files\Graphviz\bin" set "GRAPHVIZ_BIN=C:\Program Files\Graphviz\bin"

if not defined GRAPHVIZ_BIN (
    echo [ERRO] Graphviz nao encontrado nos caminhos padrao.
    echo Verifique se o Graphviz esta instalado.
    pause
    exit /b 1
)

echo [INFO] Usando Graphviz em: %GRAPHVIZ_BIN%

REM Executa o Graphviz usando aspas duplas para proteger o caminho
"!GRAPHVIZ_BIN!\sfdp.exe" -x -Goverlap=false -Tpdf "%INPUT_DOT%" -o "%OUTPUT_PDF%"

if errorlevel 1 (
    echo.
    echo [ERRO] Falha no sfdp. Verifique se o Graphviz esta instalado corretamente.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo    PROCESSO FINALIZADO COM SUCESSO
echo ===============================================
echo Arquivo gerado: %OUTPUT_PDF%

pause