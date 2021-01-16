from chores.models import basic_chore

k = basic_chore.objects.all()

for i in k:
    print('Name: ' + i.name)
    print('Description: ' + i.description)
    print('Requirements: ' + i.requirements)
    print('Limitations: ' + i.limitations)
    print('Point Values: ' + i.pointValue)
    print('')
