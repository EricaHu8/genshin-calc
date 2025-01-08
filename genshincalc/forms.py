from .models import CharCalc, Profile
from django import forms
from django.core.exceptions import ValidationError

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']

class CharCalcForm(forms.ModelForm):
    class Meta:
        model = CharCalc
        fields = ['level',
                  'level_from',
                  'level_to',
                  'na',
                  'na_from',
                  'na_to',
                  'skill',
                  'skill_from',
                  'skill_to',
                  'burst',
                  'burst_from',
                  'burst_to']

    def clean(self):
        cleaned_data = super().clean()

        # Validation to ensure that the "from" level is less than "to" level
        # User can't go backwards in level
        level_from = cleaned_data.get('level_from')
        level_to = cleaned_data.get('level_to')

        na_from = cleaned_data.get('na_from')
        na_to = cleaned_data.get('na_to')

        skill_from = cleaned_data.get('skill_from')
        skill_to = cleaned_data.get('skill_to')

        burst_from = cleaned_data.get('burst_from')
        burst_to = cleaned_data.get('burst_to')

        # Checking if at least one of the boolean fields is checked off
        level = cleaned_data.get('level')
        na = cleaned_data.get('na')
        skill = cleaned_data.get('skill')
        burst = cleaned_data.get('burst')

        if level and level_from > level_to:
            raise ValidationError("Starting level needs to be less than level goal")

        if na and na_from > na_to:
            raise ValidationError("Starting normal attack level needs to be less than normal attack goal")

        if skill and skill_from > skill_to:
            raise ValidationError("Starting skill level needs to be less than skill goal")

        if burst and burst_from > burst_to:
            raise ValidationError("Starting burst level needs to be less than burst goal")

        if not level and not na and not skill and not burst:
            raise ValidationError("You need at least one box ticked to calculate materials needed")

        return cleaned_data