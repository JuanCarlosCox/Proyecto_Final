@echo off
chcp 65001 >nul
setlocal ENABLEDELAYEDEXPANSION

:: Comprobar si Python está instalado
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Instalando Python...
    powershell -Command "Start-Process -Wait -FilePath './python-3.12.4-amd64.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1'"
    echo Reiniciando terminal...
    exit /b
)

:: Asegurar que Python está en la ruta
set PATH=%PATH%;%CD%\venv\Scripts

:: Crear entorno virtual
echo Creando entorno virtual...
python -m venv venv
if not exist "venv\Scripts\activate" (
    echo Error: No se pudo crear el entorno virtual.
    exit /b
)

:: Activar el entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate >nul 2>&1

:: Asegurar que pip está actualizado
echo Preparando entorno...
python -m ensurepip >nul 2>&1
python -m pip install --upgrade pip >nul 2>&1

:: Instalar librerías necesarias con barra de progreso
echo Instalando dependencias...
set dependencies=streamlit torch torchvision timm pillow matplotlib scikit-learn joblib
set count=0
for %%d in (%dependencies%) do (
    set /a count+=1
    echo Instalando %%d...
    pip install %%d >nul 2>&1
    call :progress_bar !count! 6
)

echo.
echo Instalación completada.

:: Ejecutando aplicación...
echo Iniciando aplicación...
echo. & powershell -command "Write-Host 'Aplicación ejecutada con éxito.' -ForegroundColor Blue"
echo. & powershell -command "Write-Host 'No cierres esta ventana hasta terminar de usar la aplicación.' -ForegroundColor DarkRed"
streamlit run app.py >nul 2>&1


:: Esperar antes de cerrar
ping -n 6 127.0.0.1 > nul

endlocal
exit /b

:progress_bar
setlocal ENABLEDELAYEDEXPANSION
set /a percent=(%1*100)/%2
set bar=
for /L %%i in (1,1,%1) do set bar=!bar!#
echo [!bar!] !percent!%%
endlocal
exit /b