import argparse
import pickle
import boto3
import random
from typing import Dict, Any
from faker import Faker
from faker.providers import BaseProvider

# a provider class to generate fake address data
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

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Generate fake household data.")
    parser.add_argument("num_normal", type=int, help="Number of normal households")
    parser.add_argument("num_fraud", type=int, help="Number of fraud households")
    args = parser.parse_args()

    num_normal = args.num_normal
    num_fraud = args.num_fraud

    fake = Faker()
    fake.add_provider(AddressProvider)
    fake.add_provider(PersonProvider)
    Faker.seed(0)

    households = []
    for _ in range(num_normal):
        households.append(generate_normal_household(fake))
    for _ in range(num_fraud):
        households.append(generate_fraud_household(fake))

    # randomly generate an association between 25% of the members between households

    # generate 100 random associations between members of different households
    for _ in range(100):
        household1 = random.choice(households)
        household2 = random.choice(households)
        while household1 == household2:
            household2 = random.choice(households)
        member1 = random.choice(household1["members"])
        member2 = random.choice(household2["members"])
        member1["associated_with_id"] = member2["id"]

    pickle_file = "fake_households.pkl"
    with open(pickle_file, "wb") as f:
        pickle.dump(households, f)
    print(f"Generated {len(households)} households and saved to {pickle_file}")

    s3 = boto3.client("s3")
    bucket_name = "grapplegraph-bucket" # replace with your bucket name
    s3.upload_file(pickle_file, bucket_name, pickle_file)
    print(f"Uploaded {pickle_file} to S3 bucket {bucket_name}")
