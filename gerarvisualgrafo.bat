@echo off
REM Script para gerar visualizacao reduzida do grafo - Versao Final com Pasta PDF
setlocal enabledelayedexpansion

set "PROJECT_DIR=%~dp0"
set "GRAPHS_DIR=%PROJECT_DIR%graphs"
set "PDF_DIR=%GRAPHS_DIR%\PDF"
set "DOT_SCRIPT=%PROJECT_DIR%dot\dot.py"
set "INPUT_DOT=%GRAPHS_DIR%\grafo_curto.dot"
set "OUTPUT_PDF=%PDF_DIR%\resultado_teste.pdf"

echo ===============================================
echo   GERADOR DE VISUALIZACAO (AMOSTRA REDUZIDA)
echo ===============================================

REM 1. Garante que a pasta PDF existe
if not exist "%PDF_DIR%" (
    echo [INFO] Criando pasta PDF em: %PDF_DIR%
    mkdir "%PDF_DIR%"
)

REM 2. Deteccao de Python
set "PYEXEC="
py --version >nul 2>&1
if !errorlevel! equ 0 (set "PYEXEC=py") else (
    python --version >nul 2>&1
    if !errorlevel! equ 0 (set "PYEXEC=python")
)

if not defined PYEXEC (
    echo [ERRO] Python nao encontrado.
    pause
    exit /b 1
)

echo [1/2] Executando dot.py...
"!PYEXEC!" "%DOT_SCRIPT%"

echo.
echo [2/2] Renderizando PDF via Graphviz (SFDP)...
echo [INFO] Salvando em: \graphs\PDF\resultado_teste.pdf

REM Define o caminho absoluto para o executável do Graphviz
set "GRAPHVIZ_BIN=C:\Program Files (x86)\Graphviz\bin"

REM Executa o Graphviz usando o caminho completo
"!GRAPHVIZ_BIN!\sfdp.exe" -x -Goverlap=false -Tpdf "%INPUT_DOT%" -o "%OUTPUT_PDF%"

if errorlevel 1 (
    echo.
    echo [ERRO] Falha no sfdp. Verifique se o Graphviz esta instalado corretamente em: %GRAPHVIZ_BIN%
    pause
    exit /b 1
)

echo.
echo ===============================================
echo   PROCESSO FINALIZADO COM SUCESSO
echo ===============================================
echo Arquivo gerado: %OUTPUT_PDF%

REM Opcional: Abre o PDF automaticamente após gerar
REM start "" "%OUTPUT_PDF%"

pause