call ./env/Scripts/activate.bat

python core/manage.py makemigrations
python core/manage.py migrate

echo exec(open("core/create_records.py").read()) | python core/manage.py shell