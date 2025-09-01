@echo off
REM ================================
REM Script para ejecutar proyecto Django en local
REM ================================

REM Activar entorno virtual (se crea si no existe)
IF NOT EXIST venv (
    echo Creando entorno virtual...
    python -m venv venv
)

call venv\Scripts\activate

REM Instalar dependencias
IF EXIST requirements.txt (
    echo Instalando dependencias...
    pip install --upgrade pip
    pip install -r requirements.txt
) ELSE (
    echo No se encontro requirements.txt
)

REM Migraciones
echo Ejecutando migraciones...
python manage.py migrate

REM Levantar servidor
echo Iniciando servidor en http://127.0.0.1:8000
python manage.py runserver
