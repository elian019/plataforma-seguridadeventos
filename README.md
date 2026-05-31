# plataforma-seguridadeventos

1- Crea un Entorno Virtual
Cuando empiezas a trabajar en un proyecto de Python por primera vez, crea un entorno virtual dentro de tu proyecto.
Solo necesitas hacer esto una vez por proyecto, no cada vez que trabajas.
Linux
python -m venv .venv

Windows PowerShell
.venv\Scripts\Activate.ps1

2- Activa el Entorno Virtual
Activa el nuevo entorno virtual para que cualquier comando de Python que ejecutes o paquete que instales lo utilicen.
Linux
source .venv/bin/activate

Windows PowerShell
.venv\Scripts\Activate.ps1

3-Revisa que el Entorno Virtual esté Activo
Revisa que el entorno virtual esté activo (el comando anterior funcionó).
Linux
which python

Windows PowerShell
Get-Command python

Si muestra el binario de python en .venv\Scripts\python, dentro de tu proyecto (en este caso awesome-project), entonces funcionó. 🎉

4-Actualiza pip
Normalmente harías esto una vez, justo después de crear el entorno virtual.
Asegúrate de que el entorno virtual esté activo (con el comando anterior) y luego ejecuta:
Bash
python -m pip install --upgrade pip

A veces, podrías obtener un error No module named pip al intentar actualizar pip.
Si esto pasa, instala y actualiza pip usando el siguiente comando:
Bash
python -m ensurepip --upgrade

5-Añade .gitignore
Si estás usando Git (deberías), añade un archivo .gitignore para excluir todo en tu .venv de Git.
Bash
echo "*" > .venv/.gitignore

6-Instala Paquetes
Después de activar el entorno, puedes instalar paquetes en él.
Bash
pip install "fastapi[standard]"

7-Ejecuta Tu Programa
Bash
python main.py