from bank.tests.model_mixins import FullSetUpMixin


# Get-Content hehe.py | python manage.py shell
# https://stackoverflow.com/questions/16853649/how-to-execute-a-python-script-from-the-django-shell


print('Start create records...')

a = FullSetUpMixin()
a.setUp()

print('Records was creaded.')