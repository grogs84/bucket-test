import pickle
import random
def generate_cypher(households):
    members_list = []
    cypher_queries = []
    id = 0
    for i, household in enumerate(households):
        household_id = str(i+300).zfill(7)
        address = household.get("address")
        street = address.get("street")
        city = address.get("city")
        state = address.get("state")
        zip_code = address.get("zip_code")
        members = household.get("members", [])
        # Ensure members is a list
        if not isinstance(members, list):
            members = [members]

        # Create a node for the household
        cypher_queries.append(f"MERGE (h:Household {{id: '{household_id}', street: '{street}', city: '{city}', state: '{state}', zip_code: '{zip_code}'}})")

        for i, member in enumerate(members):
            # print(member)
            # Ensure member is a dictionary
            if not isinstance(member, dict):
                raise ValueError(f"Expected a dictionary for member, got {type(member)}")


            members_list.append(member)
            first_name = member.get("first_name")
            last_name = member.get("last_name")
            member_id = member.get("id")
            # a merge cypher query to add the member to the graph
            cypher = f"MERGE (m:Member {{id: '{member_id}', first_name: '{first_name}', last_name: '{last_name}'}})"
            cypher_queries.append(cypher)

            # Email and Member relationship
            email = member.get("email")
            cypher = f"MERGE (e:Email {{email: '{email}'}})"
            cypher_queries.append(cypher)
            cypher = f""" \
            MATCH (m:Member {{id: '{member_id}'}}), (e:Email {{email: '{email}'}}) \
            MERGE (m)-[:HAS_EMAIL]->(e) \
            """
            cypher_queries.append(cypher)

            # Phone number and Member relationship
            phone_number = member.get("phone_number")
            cypher = f"MERGE (p:Phone {{phone_number: '{member['phone_number']}'}})"
            cypher_queries.append(cypher)
            cypher = f""" \
            MATCH (m:Member {{id: '{member_id}'}}), (p:Phone {{phone_number: '{phone_number}'}}) \
            MERGE (m)-[:HAS_PHONE]->(p) \
            """
            cypher_queries.append(cypher)
            
            # House household and Member relationship
            cypher = f""" \
            MATCH (m:Member {{id: '{member_id}'}}), (h:Household {{id: '{household_id}'}}) \
            MERGE (m)-[:HAS_ADDRESS]->(h) \
            """
            cypher_queries.append(cypher)
            id += 1
    
    return "\n".join(cypher_queries), members_list

def generate_married_relationships(members):
    cypher_queries = []
    for i, member in enumerate(members):
        married_to = member.get("married_to", None)
        if married_to:
            cypher = f""" \
            MATCH (m:Member {{id: '{member['id']}'}}), (m2:Member {{id: '{married_to}'}}) \
            MERGE (m)-[:HAS_ASSOCIATION]->(a:Association {{from:'{member['id']}',to:'{married_to}'}})<-[:HAS_ASSOCIATION]-(m2) \
            MERGE (at:AsscType {{type: 'married'}}) \
            MERGE (a)-[:HAS_TYPE]->(at) \
            """
            cypher_queries.append(cypher)
    return "\n".join(cypher_queries)

def generate_associated_with_relationships(members):
    cypher_queries = []
    for i, member in enumerate(members):
        associate = member.get("associated_with_id", None)
        if associate is None:
            continue
        cypher = f""" \
        MATCH (m:Member {{id: '{member['id']}'}}), (m2:Member {{id: '{associate}'}}) \
        MERGE (m)-[:HAS_ASSOCIATION]->(a:Association {{from:'{member['id']}',to:'{associate}'}})<-[:HAS_ASSOCIATION]-(m2) \
        MERGE (at:AsscType {{type: 'friends'}}) \
        MERGE (a)-[:HAS_TYPE]->(at) \
        """
        cypher_queries.append(cypher)
    return "\n".join(cypher_queries)


if __name__ == "__main__":
    # read the fake_households.pkl file
    with open("fake_households.pkl", "rb") as f:
        households = pickle.load(f)

    cypher_query, members = generate_cypher(households)
    with open("cmain_cypher_query.cypher", "w") as f:
        f.write(cypher_query)
    print("Cypher query generated and saved to main_cypher_query.cypher")

    cypher_query = generate_married_relationships(members)
    with open("cmarried_cypher_query.cypher", "w") as f:
        f.write(cypher_query)
    print("Cypher query generated and saved to cypher_query.cypher_married")

    cypher_query = generate_associated_with_relationships(members)
    with open("cassociated_cypher_query.cypher", "w") as f:
        f.write(cypher_query)
    print("Cypher query generated and saved to cypher_query.cypher_associated")

