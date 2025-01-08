from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (Talent, Ascension, Character,
                     EXP, SpecialMaterial, LocalSpeciality, Gem, NormalBoss, WeeklyBoss, TalentBook, RegularMob,
                     CharacterMapping, CharCalc, Profile)

admin.site.register(Talent)
admin.site.register(Ascension)
admin.site.register(Character)
admin.site.register(EXP)
admin.site.register(SpecialMaterial)
admin.site.register(LocalSpeciality)
admin.site.register(Gem)
admin.site.register(NormalBoss)
admin.site.register(WeeklyBoss)
admin.site.register(TalentBook)
admin.site.register(RegularMob)
admin.site.register(CharacterMapping)
admin.site.register(CharCalc)
admin.site.register(Profile)


