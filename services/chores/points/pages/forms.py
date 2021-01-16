from django import forms
from datetime import date

from chores.models import basic_chore


PersonChoice = [
	('Brandon', 'Brandon'),
	('Jennifer', 'Jennifer'),
	('Pandora', 'Pandora'),
        ('Violet', 'Violet')
    ]

chore_list = [
    ]

rewards_list = [

    ]

class RawProductForm(forms.Form):
    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder':'Sauce to find'}))


class PointSubmissionForm(forms.Form):
    name = forms.CharField(label='Name',widget= forms.Select(choices=PersonChoice),required='false')
    chore = forms.CharField(label='Chore',widget= forms.Select(choices=chore_list),required='false')

class RewardSubmissionForm(forms.Form):
    name = forms.CharField(label='Name',widget= forms.Select(choices=PersonChoice),required='false')
    reward = forms.CharField(label='Reward',widget= forms.Select(choices=rewards_list),required='false')
