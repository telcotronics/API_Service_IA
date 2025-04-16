#!/bin/bash
session="servidor-API"
VENV_DIR="venv"
#EXEC_CMD="fastapi run api.py "


echo "EJECUCIÓN INICIAL 'SI=S, NO=n'"
read SiNo

SiNo=$(echo "$SiNo" | tr '[:upper:]' '[:lower:]')

# Verificar si el entorno virtual ya existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv "$VENV_DIR"
fi

# Activar el entorno virtual
source "$VENV_DIR/bin/activate"

if [ "$SiNo" = "s" ]; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
    exit 0
else
    echo "Iniciando Servicio WHISPER API"
    echo "**** iniciado TMUX ****"

    tmux new-session -d -s $session
    tmux new-window -t $session:$term0 -n 'API-WHISPER'

    tmux send-keys -t $session:$term0 Enter
    tmux send-keys -t $session:$term0 'npython3 -m venv api_env'
    tmux send-keys -t $session:$term0 Enter
    tmux send-keys -t $session:$term0 'source api_env/bin/activate'
    tmux send-keys -t $session:$term0 Enter
    tmux send-keys -t $session:$term0 'pip install whisper'
    tmux send-keys -t $session:$term0 Enter
    tmux send-keys -t $session:$term0 'pip install "fastapi[standard]"'
    tmux send-keys -t $session:$term0 Enter
    tmux send-keys -t $session:$term0 'fastapi run api.py'
    tmux send-keys -t $session:$term0 Enter
fi