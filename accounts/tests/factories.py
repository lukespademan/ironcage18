from accounts.models import User


email_ix = 0


def create_user(first_name='Alice', **kwargs):
    if 'email_addr' not in kwargs:
        global email_ix
        email_ix += 1
        kwargs['email_addr'] = f'{first_name.lower()}-{email_ix}@example.com'
    return User.objects.create_user(first_name=first_name, **kwargs)


def create_user_with_full_profile(first_name='Alice', email_addr=None):
    kwargs = {
        'last_name': 'In Wonderland',
        'year_of_birth': 1985,
        'gender': 'Female',
        'ethnicity': 'White and Black Caribbean',
        'nationality': 'British',
        'country_of_residence': 'United Kingdom',
        'dont_ask_demographics': False,
        'accessibility_reqs_yn': False,
        'accessibility_reqs': None,
        'childcare_reqs_yn': False,
        'childcare_reqs': None,
        'dietary_reqs_yn': True,
        'dietary_reqs': 'Vegan',
        'is_ukpa_member': True
    }
    if email_addr is not None:
        kwargs['email_addr'] = email_addr
    return create_user(first_name, **kwargs)


def create_user_with_dont_ask_demographics_set(first_name='Alice', **kwargs):
    return create_user(first_name, dont_ask_demographics=True, **kwargs)


def create_staff_user(**kwargs):
    return create_user(is_staff=True, **kwargs)
