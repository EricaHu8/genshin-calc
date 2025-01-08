from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# My own models, decorators, forms, and filters
from .filters import CharacterFilter
from genshincalc.models import (Talent, Ascension, Character,
                                SpecialMaterial, LocalSpeciality, Gem, NormalBoss, WeeklyBoss, TalentBook, RegularMob, EXP,
                                CharacterMapping, CharCalc, Profile)

from .decorators import  unauthenticated_user
from .forms import CharCalcForm, ProfileForm

# Create your views here --------------------------------------------------------------------------------------------- #
# Index page (exclusive to AnonymousUsers) --------------------------------------------------------------------------- #
def index(request):
    if request.user.is_authenticated:
        return redirect('userpage')
    else:
        return render(request, 'index.html', )

# User page (exclusive to authenticated users) ----------------------------------------------------------------------- #
# It is near identical to the index page + some user only features
@login_required(login_url='loginpage')
def userpage(request):
    # Profile picture form
    profile = Profile.objects.get(user=request.user)
    user = request.user.profile
    form = ProfileForm(instance=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

    # Recent calculations
    calcs = CharCalc.objects.filter(profile=profile).order_by('-time_accessed')

    num_calcs = len(calcs)
    if num_calcs > 5:
        num_calcs = 5

    recents = []

    for i in range(num_calcs):
        recents.append(calcs[i])

    return render(request, 'user.html', {'recents' : recents, 'form':form})

# Delete recent calculations history --------------------------------------------------------------------------------- #
# Exclusive to authenticated users
@login_required(login_url='loginpage')
def deletehistory(request):
    profile = Profile.objects.get(user=request.user)
    calcs = CharCalc.objects.filter(profile=profile)
    calcs.delete()
    return redirect('userpage')

# Login page (exclusive to AnonymousUsers) --------------------------------------------------------------------------- #
@unauthenticated_user
def loginpage(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username or password is incorrect')
        context = {}
        return render(request, 'login.html', context)

# Registration page (exclusive to AnonymousUsers) -------------------------------------------------------------------- #
@unauthenticated_user
def registerpage(request):
        form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                    user = form.save()
                    Profile.objects.create(
                        user=user,
                        name=user.username,
                    )
                    messages.success(request, 'Account has been created for ' + user.username)
                    return redirect('loginpage')

        context = {'form': form}
        return render(request, 'register.html', context)

# Logout page (exclusive to authenticated users) --------------------------------------------------------------------- #
@login_required(login_url='loginpage')
def logoutpage(request):
    logout(request)
    return redirect('loginpage')

# List of all the characters to select from -------------------------------------------------------------------------- #
@login_required(login_url='loginpage')
def charactercalc(request):
    characters = Character.objects.all().order_by('name')

    # Filters characters according to the user's input
    char_filter = CharacterFilter(request.GET, queryset=characters)
    characters = char_filter.qs

    return render(request, 'character-calc.html', {'characters': characters, 'char_filter': char_filter})

# Character calculation form ----------------------------------------------------------------------------------------- #
@login_required(login_url='loginpage')
def char(request, character_name):
    character = Character.objects.get(name=character_name)

    current = Profile.objects.get(user=request.user)
    charfilter = CharCalc.objects.filter(character_id=character, profile=current)
    proffilter = CharCalc.objects.filter(profile=current)
    match = False

    for i in charfilter:
        for j in proffilter:
            if i.id == j.id:
                match = True

    # If user has a previous calculation saved, the values will show up instead of the default
    if match:
        char_calc = CharCalc.objects.get(character_id=character, profile=current)
        initial_data = {
            "level" : char_calc.level,
            "level_from" : char_calc.level_from,
            "level_to" : char_calc.level_to,
            "na" : char_calc.na,
            "na_from" : char_calc.na_from,
            "na_to" : char_calc.na_to,
            "skill" : char_calc.skill,
            "skill_from" : char_calc.skill_from,
            "skill_to" : char_calc.skill_to,
            "burst" : char_calc.burst,
            "burst_from" : char_calc.burst_from,
            "burst_to" : char_calc.burst_to,
        }
        calc_form = CharCalcForm(initial=initial_data)
    else: # if there is no match in the database
        calc_form = CharCalcForm()

    return render(request, 'character.html', {'character':character, 'calc_form':calc_form})

# Calculation results ------------------------------------------------------------------------------------------------ #
@login_required(login_url='loginpage')
def calcresult(request, character_name):
    character = Character.objects.get(name=character_name)
    # NON-CHARACTER SPECIFIC MATERIALS -------------------------------------------------
    exps = EXP.objects.all()
    special_materials = SpecialMaterial.objects.all()
    talent_goals = Talent.objects.all()
    ascension_goals = Ascension.objects.all()

    # CHARACTER SPECIFIC MATERIALS -----------------------------------------------------
    # Sending in all the mapped material's information
    mapping = CharacterMapping.objects.get(character_id=character.id)

    specialty = LocalSpeciality.objects.get(id=mapping.specialty_id_id)
    boss = NormalBoss.objects.get(id=mapping.boss_id_id)
    weekly_boss = WeeklyBoss.objects.get(id=mapping.weekly_boss_id_id)

    # all 4 types of gems in a queryset
    gems = Gem.objects.filter(id__range=(mapping.gem_2_id_id, mapping.gem_2_id_id + 3))

    # all 3 types of talent books in a queryset
    talents = TalentBook.objects.filter(id__range=(mapping.talent_2_id_id, mapping.talent_2_id_id + 2))

    # all 3 types of regular mob drops in a queryset
    regular_mobs = RegularMob.objects.filter(id__range=(mapping.regular_mob_1_id_id, mapping.regular_mob_1_id_id + 2))

    # Form data -----------------------------------------------------------------------
    current = Profile.objects.get(user=request.user)

    charfilter = CharCalc.objects.filter(character_id=character, profile = current)
    proffilter = CharCalc.objects.filter(profile=current)
    match = False

    for i in charfilter:
        for j in proffilter:
            if i.id == j.id:
                match = True

    if match:
        char_calc = CharCalc.objects.get(character_id=character, profile=current)
    else:
        char_calc = CharCalc.objects.create(character_id=character, profile=current)

    calc_form = CharCalcForm(request.POST)
    if calc_form.is_valid():
        char_calc.level = calc_form.cleaned_data['level']
        char_calc.level_from = calc_form.cleaned_data['level_from']
        char_calc.level_to = calc_form.cleaned_data['level_to']
        char_calc.na = calc_form.cleaned_data['na']
        char_calc.na_from = calc_form.cleaned_data['na_from']
        char_calc.na_to = calc_form.cleaned_data['na_to']
        char_calc.skill = calc_form.cleaned_data['skill']
        char_calc.skill_from = calc_form.cleaned_data['skill_from']
        char_calc.skill_to = calc_form.cleaned_data['skill_to']
        char_calc.burst = calc_form.cleaned_data['burst']
        char_calc.burst_from = calc_form.cleaned_data['burst_from']
        char_calc.burst_to = calc_form.cleaned_data['burst_to']
        char_calc.character_id = character
        char_calc.time_accessed = timezone.now()
        char_calc.save()

        # Initializing variables -----------------------------------------------------------
        gem_2, gem_3, gem_4, gem_5, exp_2, exp_3, exp_4, num_boss, num_speciality = 0, 0, 0, 0, 0, 0, 0, 0, 0
        book_2, book_3, book_4, crown, talent_boss = 0, 0, 0, 0, 0
        item_1, item_2, item_3, mora = 0, 0, 0, 0

        # A lot of math
        if char_calc.level:
            _from = Ascension.objects.get(level=char_calc.level_from)
            _to = Ascension.objects.get(level=char_calc.level_to)
            gem_2 = _to.gem_2 - _from.gem_2
            gem_3 = _to.gem_3 - _from.gem_3
            gem_4 = _to.gem_4 - _from.gem_4
            gem_5 = _to.gem_5 - _from.gem_5
            exp_2 = _to.exp_2 - _from.exp_2
            exp_3 = _to.exp_3 - _from.exp_3
            exp_4 = _to.exp_4 - _from.exp_4
            num_boss = _to.boss - _from.boss
            num_speciality = _to.speciality - _from.speciality

            # Items that are used in the talent calculation as well (will be adding to these variables)
            item_1 += _to.item_1 - _from.item_1
            item_2 += _to.item_2 - _from.item_2
            item_3 += _to.item_3 - _from.item_3
            mora += _to.mora - _from.mora

        if char_calc.na:
            _from = Talent.objects.get(level=char_calc.na_from)
            _to = Talent.objects.get(level=char_calc.na_to)
            book_2 += _to.book_2 - _from.book_2
            book_3 += _to.book_3 - _from.book_3
            book_4 += _to.book_4 - _from.book_4
            item_1 += _to.item_1 - _from.item_1
            item_2 += _to.item_2 - _from.item_2
            item_3 += _to.item_3 - _from.item_3
            mora += _to.mora - _from.mora
            crown += _to.crown - _from.crown
            talent_boss += _to.talent_boss - _from.talent_boss

        if char_calc.skill:
            _from = Talent.objects.get(level=char_calc.skill_from)
            _to = Talent.objects.get(level=char_calc.skill_to)
            book_2 += _to.book_2 - _from.book_2
            book_3 += _to.book_3 - _from.book_3
            book_4 += _to.book_4 - _from.book_4
            item_1 += _to.item_1 - _from.item_1
            item_2 += _to.item_2 - _from.item_2
            item_3 += _to.item_3 - _from.item_3
            mora += _to.mora - _from.mora
            crown += _to.crown - _from.crown
            talent_boss += _to.talent_boss - _from.talent_boss

        if char_calc.burst:
            _from = Talent.objects.get(level=char_calc.burst_from)
            _to = Talent.objects.get(level=char_calc.burst_to)
            book_2 += _to.book_2 - _from.book_2
            book_3 += _to.book_3 - _from.book_3
            book_4 += _to.book_4 - _from.book_4
            item_1 += _to.item_1 - _from.item_1
            item_2 += _to.item_2 - _from.item_2
            item_3 += _to.item_3 - _from.item_3
            mora += _to.mora - _from.mora
            crown += _to.crown - _from.crown
            talent_boss += _to.talent_boss - _from.talent_boss

        return render(request, 'result.html', { 'character':character, 'char_calc':char_calc,
        'exps':exps, 'special_materials':special_materials,
        'talent_goals':talent_goals, 'ascension_goals':ascension_goals,
        'specialty': specialty, 'boss':boss, 'weekly_boss':weekly_boss,
        'gems':gems, 'talents':talents, 'regular_mobs':regular_mobs,
        # Passing in character ascension materials
        'gem_2':gem_2, 'gem_3':gem_3, 'gem_4':gem_4, 'gem_5':gem_5, 'item_1':item_1, 'item_2':item_2, 'item_3':item_3,
        'exp_2':exp_2, 'exp_3':exp_3, 'exp_4':exp_4, 'num_boss':num_boss, 'num_speciality':num_speciality, 'mora':mora,
        # Passing in talent materials
        'book_2':book_2, 'book_3':book_3, 'book_4':book_4, 'talent_boss':talent_boss})
    else:
        return render(request, 'character.html', {'character': character, 'calc_form': calc_form})
