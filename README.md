# BackEnd
cambios
Detalles:

Django 4.0.6
Python 3.10

orlandodemontero.pythonanywhere.com
Hola como estas ? 
prueba 2

```bash
Creacion de un Entorno Virtual

Linux
$ mkdir myproject
$ cd myproject
$ python3 -m venv .venv

En Windows
> mkdir myproject
> cd myproject
> py -3 -m venv .venv

si estas usando PowerShell Usar :

.\Scripts\Activate.ps1

si usas cmd :

Scripts\activate

si usas bash :

source Scripts/activate

NOTA: para desactivar el entorno escribir : deactivate
Como sabes que esta activado el entorno Virtual ? en la consola debe mostrarse .venv
```

Nota: Esperar a que el entorno se cre , veras una carpeta dentro de tu proyecto llamada .venv
Esta carpeta sea agregada al archivo de .gitignore ya que En Pythonanywhere tiene su propio entorno virtual
si no tienes tu entorno virtual en tu pc crealo si ya lo tienes creado entonces no te preocupes .

```bash
una ves instalado el entorno virtual en tu pc deberas activarlo y asi poder trabajar este paso lo debes realizar cada vez trabajaras en el proyecto.

Linux
$ . .venv/bin/activate

Windows
> .venv\Scripts\activate

```

```bash
Instalacion de python3.10 en 
Windows
pip install python==3.10

En Linux :
https://www.python.org/downloads/release/python-3100/

https://www.youtube.com/watch?v=RcHl_Jitg_g

```

## Django

se debe instlar los modulos de Django en tu entorno virtual:
pip install Django==4.0.6
Lo que no es necesario es crear el proyecto pues ya esta creado

Extesiones de VCode recomendadas :

* Djaneiro
* Python

Inicial servidor local:

python manager.py runserver

o

python3 manager.py runserver

## Procedimientos

manage.py startapp
error puerto ? => python manage.py runserver 3000

## Creacion de super usuario admin

```bash
python manage.py createsuperuser
Datos que te solicitara..
Username
Email
Password
Password
```
