import pickle
import random

def create_cypher_node(label, properties):
    props = ", ".join([f"{key}: '{value}'" for key, value in properties.items()])
    return f"MERGE (:{label} {{{props}}})"

def create_cypher_relationship(label1, id1, label2, id2, relationship):
    return f""" \
    MATCH (a:{label1} {{id: '{id1}'}}), (b:{label2} {{id: '{id2}'}}) \
    MERGE (a)-[:{relationship}]->(b) \
    """

def generate_cypher(households):
    members_list = []
    cypher_queries = []

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
        household_properties = {
            "id": household_id,
            "street": street,
            "city": city,
            "state": state,
            "zip_code": zip_code
        }
        cypher_queries.append(create_cypher_node("Household", household_properties))

        for member in enumerate(members):
            # Ensure member is a dictionary
            if not isinstance(member, dict):
                raise ValueError(f"Expected a dictionary for member, got {type(member)}")

            members_list.append(member)
            first_name = member.get("first_name")
            last_name = member.get("last_name")
            member_id = member.get("id")

            # Create a node for the member
            member_properties = {
                "id": member_id,
                "first_name": first_name,
                "last_name": last_name
            }
            cypher_queries.append(create_cypher_node("Member", member_properties))

            # Email and Member relationship
            email = member.get("email")
            email_properties = {"email": email}
            cypher_queries.append(create_cypher_node("Email", email_properties))
            cypher_queries.append(create_cypher_relationship("Member", member_id, "Email", email, "HAS_EMAIL"))

            # Phone number and Member relationship
            phone_number = member.get("phone_number")
            phone_properties = {"phone_number": phone_number}
            cypher_queries.append(create_cypher_node("Phone", phone_properties))
            cypher_queries.append(create_cypher_relationship("Member", member_id, "Phone", phone_number, "HAS_PHONE"))

            # Household and Member relationship
            cypher_queries.append(create_cypher_relationship("Member", member_id, "Household", household_id, "HAS_ADDRESS"))


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

