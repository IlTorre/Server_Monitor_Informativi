# Monitor_informativi_server
Monitor_informativi_server: un server per la gestione di monitor informativi di Marco Torreggiani

Software necessario per l'esecuzione del programma:


    -Python:
        sudo apt-get install python

    -Django 1.8 (LTS):
        pip install Django==1.8
        sudo pip install --upgrade Django==1.8

    -Pillow:
        https://pypi.python.org/pypi/Pillow


Come eseguire il programma:


    -Spostarsi nella cartella Monitor:informativi_server (dove è presente il file manage.py)
    -Digitare: python manage.py createsuperuser e seguire le indicazioni per creare un utente d'amministrazione
    -Digitare: python manage.py runserver
    -Da browser web accedere al sito http://127.0.0.1:8000/admin e effettuare il login con le credenziali precedentemente create
    -Creare il gruppo Revisore
    -Creare il gruppo Inserzionista


il sito è disponibile in locale all'url http://127.0.0.1:8000/
