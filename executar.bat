@echo off
REM Script para compilar e executar o projeto de Grafos com algs4 + Graphviz
REM Versao corrigida com deteccao robusta de Python

setlocal enabledelayedexpansion

REM Defina o diretorio base do projeto
set "PROJECT_DIR=%~dp0"
set "OUTPUT_DIR=%PROJECT_DIR%output"
set "ALGS4_DIR=%PROJECT_DIR%algs4"
set "JAVA_BUILD=%ALGS4_DIR%\build\classes\main"
set "GRAPH_INPUT=%PROJECT_DIR%data\entrada.csv"
set "GRAPHVIZ_PATH=C:\Program Files\Graphviz\bin"

REM Valida se os caminhos existem
if not exist "%ALGS4_DIR%" (
    echo [ERRO] Pasta algs4 nao encontrada: %ALGS4_DIR%
    pause
    exit /b 1
)

if not exist "%GRAPH_INPUT%" (
    echo [AVISO] Arquivo de entrada nao encontrado: %GRAPH_INPUT%
    echo [AVISO] Tentando arquivo do diretorio graphs...
    set "GRAPH_INPUT=%PROJECT_DIR%graphs\grafo_formatado.txt"
    if not exist "!GRAPH_INPUT!" (
        echo [ERRO] Nenhum arquivo de entrada encontrado em data\ ou graphs\
        pause
        exit /b 1
    )
)

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

if exist "%GRAPHVIZ_PATH%" (
    set "PATH=%GRAPHVIZ_PATH%;%PATH%"
)

cls
echo ===============================================
echo  SISTEMA DE PROCESSAMENTO DE GRAFOS
echo ===============================================
echo.

echo [1/5] Limpando arquivos anteriores...
echo -----------------------------------------------
if exist "%ALGS4_DIR%\build" rmdir /s /q "%ALGS4_DIR%\build" >nul 2>&1
if exist "%PROJECT_DIR%graphs\*.dot" del "%PROJECT_DIR%graphs\*.dot" 2>nul
echo [OK] Limpeza concluida!
echo.

echo [2/5] Formatando CSV de entrada...
echo -----------------------------------------------

REM Lógica Robusta para encontrar o Python Real
set "PYEXEC="

REM Testa o Python Launcher (Recomendado no Windows)
py --version >nul 2>&1
if !errorlevel! equ 0 (
    set "PYEXEC=py"
) else (
    REM Testa o comando python diretamente
    python --version >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYEXEC=python"
    )
)

REM Se falhou nos comandos globais, tenta caminhos especificos conhecidos
if not defined PYEXEC (
    if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe" (
        set "PYEXEC="%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe""
    ) else if exist "C:\Python311\python.exe" (
        set "PYEXEC=C:\Python311\python.exe"
    )
)

if not defined PYEXEC (
    echo [ERRO] Python nao foi encontrado. 
    echo Verifique se o Python esta instalado e marque "Add to PATH" no instalador.
    pause
    exit /b 1
)

echo [INFO] Usando: !PYEXEC!
"!PYEXEC!" "%PROJECT_DIR%python\reformata.py"
if errorlevel 1 (
    echo [ERRO] Falha ao executar reformata.py!
    pause
    exit /b 1
)
echo [OK] CSV formatado com sucesso.
echo.

echo [3/5] Verificando dependencias Python...
set PACKAGES=matplotlib numpy powerlaw networkx pydot
for %%p in (%PACKAGES%) do (
    echo Verificando %%p...
    !PYEXEC! -m pip show %%p >nul 2>&1
    if !errorlevel! neq 0 (
        echo Instalando %%p...
        !PYEXEC! -m pip install %%p
        if !errorlevel! neq 0 (
            echo [ERRO] Falha ao instalar %%p
            pause
            exit /b 1
        )
    ) else (
        echo %%p ja instalado.
    )
)
echo [OK] Dependencias verificadas.
echo.

echo [4/5] Compilando codigo Java...
echo -----------------------------------------------
REM Define o caminho raiz do código (onde começa o pacote edu/...)
set "JAVA_ROOT=%PROJECT_DIR%algs4\src\main\java"
set "PACKAGE_PATH=%JAVA_ROOT%\edu\princeton\cs\algs4"

if not exist "%PACKAGE_PATH%" (
    echo [ERRO] Diretorio de pacotes nao encontrado: %PACKAGE_PATH%
    pause
    exit /b 1
)

REM Entra na pasta do pacote, compila tudo, e volta
cd /d "%PACKAGE_PATH%"
echo [INFO] Compilando arquivos .java em: %CD%
javac *.java
if errorlevel 1 (
    echo [ERRO] Falha na compilacao com javac!
    cd /d "%PROJECT_DIR%"
    pause
    exit /b 1
)
cd /d "%PROJECT_DIR%"
echo [OK] Compilacao concluida!
echo.

echo [5/5] Executando aplicacao e gerando saidas...
echo -----------------------------------------------

REM O CP deve apontar para a RAIZ do código (antes do edu/...)
set "MY_CP=%JAVA_ROOT%"

echo [INFO] Iniciando Java (Alocando RAM)...
REM Note que chamamos o nome COMPLETO da classe: pacote.Classe
java -Xmx4g -XX:+UseSerialGC -cp "%MY_CP%" edu.princeton.cs.algs4.Graph "%PROJECT_DIR%graphs\grafo_formatado.txt"

if errorlevel 1 (
    echo.
    echo [ERRO] Falha na execucao do Graph.java! 
    pause
    exit /b 1
)

echo [INFO] Iniciando Java (Alocando 4GB de RAM)...
REM Reduzimos para 3GB e otimizamos o Garbage Collector para liberar espaço agressivamente
java -Xmx3g -XX:+UseSerialGC -cp "%MY_CP%" edu.princeton.cs.algs4.Graph "%PROJECT_DIR%graphs\grafo_formatado.txt"

if errorlevel 1 (
    echo.
    echo [ERRO] Falha na execucao do Graph.java! 
    echo Verifique se o arquivo .txt contem apenas numeros e se ha RAM disponivel.
    pause
    exit /b 1
)

echo [OK] Processamento Java concluido.
echo.

REM --- Execucao de Scripts Auxiliares ---

if exist "%PROJECT_DIR%dot\dot.py" (
    echo [INFO] Executando dot.py...
    "!PYEXEC!" "%PROJECT_DIR%dot\dot.py"
)

if exist "%PROJECT_DIR%python\histograma.py" (
    echo [INFO] Gerando histograma...
    "!PYEXEC!" "%PROJECT_DIR%python\histograma.py"
)

REM --- Geracao de Imagem (Aviso: Pode ser lento para 6M de arestas) ---

if exist "%GRAPHVIZ_PATH%\dot.exe" (
    echo [INFO] Tentando gerar imagens PNG (Graphviz)...
    echo [AVISO] Isso pode demorar muito para grafos grandes.
    for %%F in ("%PROJECT_DIR%graphs\*.dot") do (
        echo  + Processando: %%~nxF
        "%GRAPHVIZ_PATH%\dot.exe" -Tpng -o "%OUTPUT_DIR%\%%~nF.png" "%%F"
    )
)

echo.
echo ===============================================
echo PROCESSO CONCLUIDO COM SUCESSO!
echo ===============================================
pause