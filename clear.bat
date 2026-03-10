@echo off
REM Script para limpar arquivos gerados no projeto de Grafos
setlocal enabledelayedexpansion

REM Defina o diretorio base do projeto com aspas para seguranca
set "PROJECT_DIR=%~dp0"

cls
echo ========================================
echo   LIMPANDO ARQUIVOS ANTIGOS...
echo ========================================

REM 1. Apagar arquivos .class compilados
if exist "%PROJECT_DIR%algs4\build" (
    rmdir /s /q "%PROJECT_DIR%algs4\build"
    echo [OK] Deletado: algs4/build
)

if exist "%PROJECT_DIR%algs4\src\main\java\edu\princeton\cs\algs4\Graph.class" (
    del /f /q "%PROJECT_DIR%algs4\src\main\java\edu\princeton\cs\algs4\Graph.class"
    echo [OK] Arquivo Graph.class removido com sucesso.
)

REM 2. Apagar arquivo de entrada formatado
if exist "%PROJECT_DIR%graphs\grafo_formatado.txt" (
    del /f /q "%PROJECT_DIR%graphs\grafo_formatado.txt"
    echo [OK] Deletado: grafo_formatado.txt
)

REM 3. Apagar todos os arquivos .dot na pasta graphs
if exist "%PROJECT_DIR%graphs\*.dot" (
    del /f /q "%PROJECT_DIR%graphs\*.dot" 2>nul
    echo [OK] Deletados arquivos .dot em graphs
)

REM 4. LIMPAR A PASTA PDF (Nova funcionalidade)
if exist "%PROJECT_DIR%graphs\PDF" (
    rmdir /s /q "%PROJECT_DIR%graphs\PDF"
    echo [OK] Deletada pasta: graphs/PDF
)

REM 5. Apagar pasta de saida geral
if exist "%PROJECT_DIR%output" (
    rmdir /s /q "%PROJECT_DIR%output"
    echo [OK] Deletada pasta: output
)

echo.
echo ========================================
echo   LIMPEZA CONCLUIDA!
echo ========================================
pause