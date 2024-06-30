# vehicle-identification-bun-api

## Setup venv

### install venv
```
pip install virtualenv
```

### setup venv

```
cd Vehicle-Identification-flask-api
virtualenv venv
```

### Note:
if you get this error 
.\venv\Scripts\activate : File G:\Projects\NGT\vehicle-identification-flask-api\venv\Scripts\activate.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at 
https:/go.microsoft.com/fwlink/?LinkID=135170.
At line:1 char:1

then run 
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```


### activate venv
```
.\venv\Scripts\activate 
```

### install requirements

```
pip install -r requirements.txt # install required pacakages
```

### Run server
```
python app.py
```

# deactivate venv
```
deacticate
```