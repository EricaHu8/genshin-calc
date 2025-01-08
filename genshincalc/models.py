from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
# User profile ------------------------------------------------------------------------------------------------------- #
class Profile(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
       return self.name

# Character you can select ------------------------------------------------------------------------------------------- #
ELEMENTS = (
    ('Anemo', 'Anemo'),
    ('Cryo', 'Cryo'),
    ('Dendro', 'Dendro'),
    ('Electro', 'Electro'),
    ('Geo', 'Geo'),
    ('Hydro', 'Hydro'),
    ('Pyro', 'Pyro'),
)

RARITY = (
    (4, '★★★★'),
    (5, '★★★★★')
)

WEAPONS = (
    ('Bow', 'Bow'),
    ('Catalyst', 'Catalyst'),
    ('Claymore', 'Claymore'),
    ('Polearm', 'Polearm'),
    ('Sword', 'Sword')
)

class Character(models.Model):
    name = models.CharField(max_length=100)
    element = models.CharField(choices=ELEMENTS, max_length=100)
    rarity = models.IntegerField(choices=RARITY)
    weapon_type = models.CharField(choices=WEAPONS, max_length=100)

    def __str__(self):
        return self.name

# Form model (character calculation) --------------------------------------------------------------------------------- #
LEVEL_CHOICES_FROM = (
    (1, 1),
    (20, 20),
    (40, 40),
    (50, 50),
    (60, 60),
    (70, 70),
    (80, 80),
)

LEVEL_CHOICES_TO = (
    (20, 20),
    (40, 40),
    (50, 50),
    (60, 60),
    (70, 70),
    (80, 80),
    (90, 90),
)

TALENT_CHOICES_FROM = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
)

TALENT_CHOICES_TO = (
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)

class CharCalc(models.Model):
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    time_accessed = models.DateTimeField(default=timezone.now)

    level = models.BooleanField(default=True)
    level_from = models.IntegerField(choices=LEVEL_CHOICES_FROM, default=1)
    level_to = models.IntegerField(choices=LEVEL_CHOICES_TO, default=90)

    na = models.BooleanField(default=True)
    na_from = models.IntegerField(choices=TALENT_CHOICES_FROM, default=1)
    na_to = models.IntegerField(choices=TALENT_CHOICES_TO, default=10)

    skill = models.BooleanField(default=True)
    skill_from = models.IntegerField(choices=TALENT_CHOICES_FROM, default=1)
    skill_to = models.IntegerField(choices=TALENT_CHOICES_TO, default=10)

    burst = models.BooleanField(default=True)
    burst_from = models.IntegerField(choices=TALENT_CHOICES_FROM, default=1)
    burst_to = models.IntegerField(choices=TALENT_CHOICES_TO, default=10)

    def __str__ (self):
        return self.character_id.name

# Number of materials needed to reach each talent level --------------------------------------------------------------- #
class Talent(models.Model):
    # level of the talent (from 1 to 10), level 1 requires 0 materials
    level = models.IntegerField(primary_key=True)

    # book refers to talent books, number refers to rarity (in stars)
    book_2 = models.IntegerField()
    book_3 = models.IntegerField()
    book_4 = models.IntegerField()

    # item refers to common mob drops, number refers to rarity (in stars)
    item_1 = models.IntegerField()
    item_2 = models.IntegerField()
    item_3 = models.IntegerField()

    # special kinds of materials (no rarity)
    talent_boss = models.IntegerField()
    mora = models.IntegerField()
    crown = models.IntegerField()

# Number of materials needed to reach each ascension level ----------------------------------------------------------- #
class Ascension(models.Model):
    # level goals for ascension (20, 40, 50, 60, 70, 80, 90)
    level = models.IntegerField(primary_key=True)

    # gem refers to ascension gems, number refers to rarity (in stars)
    gem_2 = models.IntegerField()
    gem_3 = models.IntegerField()
    gem_4 = models.IntegerField()
    gem_5 = models.IntegerField()

    # item refers to common mob drops, number refers to rarity (in stars)
    item_1 = models.IntegerField()
    item_2 = models.IntegerField()
    item_3 = models.IntegerField()

    # exp refers to exp books, number refers to rarity (in stars)
    exp_2 = models.IntegerField()
    exp_3 = models.IntegerField()
    exp_4 = models.IntegerField()

    # special kinds of materials (no rarity)
    boss = models.IntegerField()
    speciality = models.IntegerField()
    mora = models.IntegerField()

# Level Up Materials ------------------------------------------------------------------------------------------------- #
# EXP (Character Books and Weapon Ores)
class EXP(models.Model):
    name = models.CharField(max_length=100)
    exp = models.IntegerField()

    def __str__(self):
        return self.name

# Special Materials (Mora and Crown of Insight)
class SpecialMaterial(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Local Specialities
class LocalSpeciality(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Ascension Gems
class Gem(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Boss Drops
class NormalBoss(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Weekly Boss Drops
class WeeklyBoss(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Talent Books
class TalentBook(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Regular Mob Drops
class RegularMob(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# End of Level Up Materials ------------------------------------------------------------------------------------------ #

# Junction Tables
class CharacterMapping(models.Model):
    character_id= models.OneToOneField(Character, on_delete=models.CASCADE ,primary_key=True)
    specialty_id = models.ForeignKey(LocalSpeciality, on_delete=models.CASCADE)
    boss_id = models.ForeignKey(NormalBoss, on_delete=models.CASCADE)
    weekly_boss_id = models.ForeignKey(WeeklyBoss, on_delete=models.CASCADE)
    gem_2_id = models.ForeignKey(Gem, on_delete=models.CASCADE)
    talent_2_id = models.ForeignKey(TalentBook, on_delete=models.CASCADE)
    regular_mob_1_id = models.ForeignKey(RegularMob, on_delete=models.CASCADE)

    def __str__(self):
        return self.character_id.name