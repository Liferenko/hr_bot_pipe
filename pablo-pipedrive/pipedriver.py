from pipedrive import Pipedrive

USERNAME = 'office@skills.events'
PASSWORD = 'TookieTookie'
lead_name = 'Pablo'
lead_phone = '+38-068-907-5520'
lead_email = 'liferenko@test.com'

pipedrive = Pipedrive(USERNAME, PASSWORD)
print('Login success. Keep going')

def create_new_person_plus_deal(lead_name, lead_phone, lead_email):
    pipedrive.persons({
        'name': lead_name,
        'org_id': 327,
        'email': lead_email,
        'phone': lead_phone,
        '1abdf0adad500f25d3375c625bcc2532c29980cd': 'найден hr_ботом на work.ua'
    }, method='POST')
    print('New person was created')

    pipedrive.deals({
        'stage_id': 45,
        'title': lead_name + '|' + lead_phone,
        'value': 1200000,
        'org_id': 327,
        'status': 'open'
    }, method='POST')
    print('New deal was created')
