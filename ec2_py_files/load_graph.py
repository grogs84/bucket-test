import boto3
import logging

# logger should write to cypher.log
logger = logging.getLogger(__name__)
handler = logging.FileHandler("cypher.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    neptune = boto3.client("neptunedata", "us-east-1", endpoint_url="https://db-grapplegraph-1.cluster-c072qy8ounfy.us-east-1.neptune.amazonaws.com:8182")
    print(neptune.get_engine_status())

    # open the cypher file and execute one line at a time
    for query_file in ["cmain_cypher_query.cypher", "cmarried_cypher_query.cypher", "cassociated_cypher_query.cypher"]:
        with open(query_file, "r") as f:
            # iterate through the lines in the file
            for line in f:
                # remove leading and trailing whitespace
                cypher_query = line.strip()
                # check if the line is not empty
                if cypher_query:
                    print(cypher_query)
                    # execute the cypher query
                    response = neptune.execute_open_cypher_query(
                        openCypherQuery=cypher_query,
                    )
                    # send response to logger file cypher.log
                    logger.info(f"Response: {response['results']}")


if __name__ == "__main__":
    main()