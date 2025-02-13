from datetime import datetime

# Source Data to be translated
source_data = {
    'id': '789',
    'name': 'Michael Bird',
    'age': 41,
    'address': {
        'street': '789 Maple Blvd',
        'city': 'Lakeside',
        'zipcode': '54321'
    },
    'registered_at': '2021-11-10T14:20:00'
}

# Transform the source data to target data
target_data = {
    'identifier': int(source_data['id']),
    'full_name': source_data['name'],
    'years_old': source_data['age'],
    'location': {
        'address_line': source_data['address']['street'],
        'city_name': source_data['address']['city'],
        'postal_code': source_data['address']['zipcode']
    },
    'signup_date': datetime.strptime(source_data['registered_at'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
}

print(target_data)