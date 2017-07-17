from pipedrive import Pipedrive

USERNAME = 'office@skills.events'
PASSWORD = 'TookieTookie'
lead_name = 'Pablo'
lead_phone = '+38-068-907-5520'
lead_email = 'liferenko@test.com'

pipedrive = Pipedrive(USERNAME, PASSWORD)
print('Login success. Keep going')

def create_new_person_plus_deal():
    pipedrive.persons({
        'name': lead_name,
        'org_id': 327,
        'email': lead_email,
        'phone': lead_phone,


    }, method='POST')

    pipedrive.deals({
        "id": 45,
        "order_nr": 1,
        "name": "Новые люди с work.ua",

        "deal_probability": 100,
        "pipeline_id": 11,
        "pipeline_name": "HR_bot: Новые люди",

        'title': lead_name + '|' + lead_phone,
        'value': 1000000,
        'org_id': 327,
        'status': 'open'
    }, method='GET')
    print('New deal was created')

create_new_person_plus_deal()