from datetime import datetime

def translate_source_to_target(source_data):
    try:
        # Mapping fields based on the rules defined above
        target_data = {
            'identifier': int(source_data['id']),
            'full_name': source_data['name'],
            'years_old': source_data['age'],
            'location': {
                'address_line': source_data['address']['street'],
                'city_name': source_data['address']['city'],
                'postal_code': source_data['address']['zipcode']
            },
            'signup_date': datetime.fromisoformat(source_data['registered_at']).date().isoformat()
        }
        
        return target_data
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

# Source data provided
source_data = {
    'id': '789',
    'name': 'Michael Bird',
    'age': 41,
    'address': {'street': '789 Maple Blvd', 'city': 'Lakeside', 'zipcode': '54321'},
    'registered_at': '2021-11-10T14:20:00'
}

# Translate source data to target data
target_data = translate_source_to_target(source_data)

# Print the translated target data
print(target_data)