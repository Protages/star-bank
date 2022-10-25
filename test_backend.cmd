call ./env/Scripts/activate.bat

cd core/

echo "Run tests for models"
python manage.py test bank.tests.test_models

echo "Run tests for serializers"
python manage.py test bank.tests.test_serializers

echo "Run tests for views"
python manage.py test bank.tests.test_views