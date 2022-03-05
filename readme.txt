TO RUN PLS ensure all setup process belisted below are done

1.create python env
install python libaray/package in requirement.txt

2.this project use oracle db
import  oracle sql dump file in the project folder
goldBank/ACCOUNT_202203052157.sql

NOTE change the db config settings in settings.py as below example
###DB CONFIG
FIBERNOW_DB_CONFIG={
     
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'user',
        'USER': 'user',
        'PASSWORD': 'user',
        'HOST': 'db ip add',
        'PORT': '1539',
  
}
##### END DB CONFIG

3.run the project and to access swagger on local machine go to http://localhost:8000/

4. sample working app screen shot in 
c:/goldBank/swagger api test sample.png
c:/goldBank/swaggerPage.png
