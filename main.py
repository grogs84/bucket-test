import argparse
import pickle
import boto3
import random
from typing import Dict, Any
from faker import Faker
from faker.providers import BaseProvider

from utils import generate_normal_household, generate_fraud_household
from utils import AddressProvider, PersonProvider
from generate_cypher import generate_cypher, generate_married_relationships, generate_associated_with_relationships


def generate_fake_data(normal, fraud):
    """
    Generate fake household data and save it to a pickle file.
    """
    fake = Faker()
    fake.add_provider(AddressProvider)
    fake.add_provider(PersonProvider)
    Faker.seed(0)

    households = []
    for _ in range(10):
        households.append(generate_normal_household(fake))
    for _ in range(10):
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
    bucket_name = "grapplegraph-bucket"  # replace with your bucket name
    s3.upload_file(pickle_file, bucket_name, pickle_file)
    print(f"Uploaded {pickle_file} to S3 bucket {bucket_name}")
    return households



def main(normal, fraud):
    """
    Main function to generate fake data and upload to S3.
    """
    all_cypher_queries = []
    households = generate_fake_data(normal, fraud)
    # Save the households to a pickle file
    with open("fake_households.pkl", "wb") as f:
        pickle.dump(households, f)
    print(f"Generated {len(households)} households and saved to fake_households.pkl")

    cypher_queries, members_list = generate_cypher(households)
    all_cypher_queries.extend(cypher_queries)

    married_relationships = generate_married_relationships(members_list)
    all_cypher_queries.append(married_relationships)

    associated_with_relationships = generate_associated_with_relationships(members_list)
    all_cypher_queries.append(associated_with_relationships)

    cypher_file = "fake_households.cypher"
    with open(cypher_file, "w") as f:
        f.write("\n".join(all_cypher_queries))
    print(f"Generated Cypher queries and saved to {cypher_file}")


if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Generate fake household data.")
    parser.add_argument("num_normal", type=int, help="Number of normal households")
    parser.add_argument("num_fraud", type=int, help="Number of fraud households")
    args = parser.parse_args()

    num_normal = args.num_normal
    num_fraud = args.num_fraud

    main(num_normal, num_fraud)