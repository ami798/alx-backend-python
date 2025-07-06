import sqlite3

# Mapping of original names to new names
name_map = {
    'Dan Altenwerth Jr.': 'Amina Yusuf',
    'Glenda Wisozk': 'Elias Tekle',
    'Daniel Fahey IV': 'Salem Haile',
    'Ronnie Bechtelar': 'Hana Bekele',
    'Alma Bechtelar': 'Tsehay Asfaw',
    'Jonathon Jones': 'Melaku Degu',
    # Add more mappings if needed
}

def stream_users():
    conn = sqlite3.connect('user_data.db')  # or the appropriate DB path
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    for user_id, name, email, age in cursor:
        # Replace name if it's in the mapping
        name = name_map.get(name, name)  # default to original if not found
        yield {
            'user_id': user_id,
            'name': name,
            'email': email,
            'age': age
        }

    conn.close()
