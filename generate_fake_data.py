import pickle
import boto3
import random
from typing import Dict, Any
from faker import Faker
from faker.providers import BaseProvider


class AddressProvider(BaseProvider):
    def address(self) -> Dict[str, Any]:
        return {
            "street": self.generator.street_address(),
            "city": self.generator.city(),
            "state": self.generator.state(),
            "zip_code": self.generator.zipcode(),
        }

# a provider class to generate fake person data
class PersonProvider(BaseProvider):
    def person(self) -> Dict[str, Any]:
        return {
            "first_name": self.generator.first_name(),
            "last_name": self.generator.last_name(),
            "email": self.generator.email(),
            "phone_number": self.generator.phone_number(),
            "id": str(random.randint(1000000, 9999999)).zfill(9),  # Ensure person_id is a 7-digit string
        }
    
def generate_normal_household(fake: Faker) -> Dict[str, Any]:
    household = {"address": fake.address(), "members": []}
    num_people = random.randint(1, 4)  # 1 to 4 people
    shared_phone = fake.phone_number() if random.random() < 0.3 else None
    shared_email = fake.email() if random.random() < 0.3 else None

    for i in range(num_people):
        person = fake.person()
        # person['id'] = str(i).zfill(7)  # Ensure person_id is a 7-digit string
        if shared_phone and random.random() < 0.5:
            person["phone_number"] = shared_phone
        if shared_email and random.random() < 0.5:
            person["email"] = shared_email
        household["members"].append(person)

    # Add marriage logic
    if num_people > 1 and random.random() < 0.6:
        household["members"][0]["married_to"] = household["members"][1]["id"]

    return household

def generate_fraud_household(fake: Faker) -> Dict[str, Any]:
    household = {"address": fake.address(), "members": []}
    num_people = random.randint(1, 6)  # 1 to 6 people
    shared_phone = fake.phone_number() if random.random() < 0.75 else None
    shared_email = fake.email() if random.random() < 0.75 else None

    for i in range(num_people):
        person = fake.person()
        # person['id'] = str(i+90000).zfill(7)  # Ensure person_id is a 7-digit string
        if shared_phone and random.random() < 0.75:
            person["phone_number"] = shared_phone
        if shared_email and random.random() < 0.75:
            person["email"] = shared_email
        household["members"].append(person)

    # Add marriage logic
    if num_people > 2 and random.random() < 0.1:
        household["members"][0]["married_to"] = household["members"][1]["id"]

    return household
