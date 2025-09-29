#!/bin/bash
# Define el nombre de la sesión de TMUX (debe ser el mismo que el otro script)
session="api_session"
VENV_DIR="venv"

echo "EJECUCIÓN API-WHISPER 'SI=s, NO=n'"
read SiNoWhisper
SiNoWhisper=$(echo "$SiNoWhisper" | tr '[:upper:]' '[:lower:]')

if [ "$SiNoWhisper" = "s" ]; then
    echo "Iniciando Servicio API-WHISPER"

    # Verifica si la sesión de TMUX ya existe
    tmux has-session -t $session 2>/dev/null

    if [ $? != 0 ]; then
        # La sesión no existe, la creamos
        echo "**** Creando nueva sesión TMUX: $session ****"
        tmux new-session -d -s $session
    else
        # La sesión ya existe
        echo "**** Usando sesión TMUX existente: $session ****"
    fi

    # Creamos una nueva ventana en la sesión
    tmux new-window -t $session -n 'API-WHISPER'

    # Entrar al directorio del proyecto (si es necesario) y preparar el entorno virtual
    tmux send-keys -t $session:'API-WHISPER' 'cd API-WHISPER' # Asegúrate de que este sea el nombre de la carpeta
    tmux send-keys -t $session:'API-WHISPER' Enter

    # Verificar si el entorno virtual ya existe en el directorio de la API
    tmux send-keys -t $session:'API-WHISPER' 'if [ ! -d "'"$VENV_DIR"'" ]; then echo "Creando entorno virtual..."; python3 -m venv "'"$VENV_DIR"'"; fi'
    tmux send-keys -t $session:'API-WHISPER' Enter

    # Activar el entorno virtual
    tmux send-keys -t $session:'API-WHISPER' 'source '"$VENV_DIR"'/bin/activate'
    tmux send-keys -t $session:'API-WHISPER' Enter

    # Instalar dependencias si no existen (asumiendo un archivo requirements.txt)
    tmux send-keys -t $session:'API-WHISPER' 'pip list -o > /dev/null || pip install -r requirements.txt'
    tmux send-keys -t $session:'API-WHISPER' Enter

    # Iniciar la API
    tmux send-keys -t $session:'API-WHISPER' 'fastapi run api.py'
    tmux send-keys -t $session:'API-WHISPER' Enter

    echo "API-WHISPER se está ejecutando en la ventana 'API-WHISPER' de la sesión '$session'."
    echo "Para adjuntarte a la sesión, usa: tmux attach -t $session"

fi