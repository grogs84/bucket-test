import pandas as pd
import boto3

def main():

    # print("Hello from bucket-test!")
    # s3 = boto3.client("s3")
    # bucket_name = "grapplegraph-bucket"
    # file_name = "test.csv"
    # # Create a sample DataFrame
    # data = {
    #     "Name": ["Alice", "Bob", "Charlie"],
    #     "Age": [25, 30, 35],
    #     "City": ["New York", "Los Angeles", "Chicago"]
    # }
    # df = pd.DataFrame(data)
    # # Save the DataFrame to a CSV file
    # df.to_csv(file_name, index=False)
    # # Upload the CSV file to S3
    # s3.upload_file(file_name, bucket_name, file_name)
    # # List the objects in the S3 bucket
    # response = s3.list_objects_v2(Bucket=bucket_name)
    # if "Contents" in response:
    #     print("Objects in S3 bucket:")
    #     for obj in response["Contents"]:
    #         print(obj["Key"])
    # else:
    #     print("No objects found in the bucket.")
    # # Download the CSV file from S3
    # s3.download_file(bucket_name, file_name, "downloaded_" + file_name)
    # # Read the downloaded CSV file into a DataFrame
    # downloaded_df = pd.read_csv("downloaded_" + file_name)
    # print("Downloaded DataFrame:")
    # print(downloaded_df)
    # # Clean up the local files
    # import os
    # os.remove(file_name)
    # os.remove("downloaded_" + file_name)
    # # Clean up the S3 bucket
    # s3.delete_object(Bucket=bucket_name, Key=file_name)
    # print(f"Deleted {file_name} from S3 bucket {bucket_name}")

    def make_fake_neptune_data():
        # Create a sample DataFrame for Neptune
        person_nodes = {
            "fname": ["Matt", "Maggie", "Whit", "Lucy", "Herb", "Kathy"],
            "lname": ["Grogan", "Grogan", "Grogan", "Grogan", "Marquedant", "Marquedant"],
            "~id": [1, 2, 3, 4, 5, 6],
            "~label": ["Person", "Person", "Person", "Person", "Person", "Person"]
        }
        person_edges = {
            "~from": [1, 2, 3, 4, 5, 6],
            "~to": [2, 3, 4, 5, 6, 1],
            "~label": ["knows", "knows", "knows", "knows", "knows", "knows"],
            "~id": ["1-2", "2-3", "3-4", "4-5", "5-6", "6-1"]
        }
        person_nodes_df = pd.DataFrame(person_nodes)
        person_edges_df = pd.DataFrame(person_edges)

        node_file = "neptune_test_person_nodes.csv"
        edge_file = "neptune_test_person_edges.csv"
        person_nodes_df.to_csv(node_file, index=False)
        person_edges_df.to_csv(edge_file, index=False)
        print(f"Created {node_file} and {edge_file}")
        # Upload the CSV files to S3
        s3 = boto3.client("s3")
        bucket_name = "grapplegraph-bucket"
        s3.upload_file(node_file, bucket_name, node_file)
        s3.upload_file(edge_file, bucket_name, edge_file)
        print(f"Uploaded {node_file} and {edge_file} to S3 bucket {bucket_name}")
        # List the objects in the S3 bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        if "Contents" in response:
            print("Objects in S3 bucket:")
            for obj in response["Contents"]:
                print(obj["Key"])
        else:
            print("No objects found in the bucket.")
        bucket_name = "grapplegraph-bucket"
        cypher_file = "cypher_query.cypher_main"
        s3.download_file(bucket_name, cypher_file, "downloaded_" + cypher_file)
        # Upload the CSV file to S3:wq

    make_fake_neptune_data()

if __name__ == "__main__":
    main()

    # make_fake_neptune_data()
