from faker import Faker
import random
import json

fake = Faker()


def generate_user_data():
    return {
        "email": fake.email(),
        "name": fake.first_name(),
        "phone_number": fake.phone_number() if random.choice([True, False]) else None,
        "support_level": random.choice(["Bronze", "Silver", "Gold"]),
        "gender": random.choice(["male", "female"]),
        "surname": fake.last_name(),
        "age": random.randint(18, 70),
        "user_id": fake.random_int(min=1, max=10000),
        "login": fake.user_name(),
        "timestamp": None,
        "patronymic": fake.first_name() if random.choice([True, False]) else None,
        "birth_date": fake.date_of_birth().isoformat(),
        "message": fake.sentence()
    }


user_data = [generate_user_data() for _ in range(150)]


with open('user_data.json', 'w') as f:
    json.dump(user_data, f, indent=4)