def cloud_upload(blob_name, content, bucket_name):
    from google.cloud import storage

    """ Upload data to a bucket"""

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'C:/Users/wuala/Documents/Google_key/pragmatic-cat-345714-2221156cd8c7.json')

    #print(buckets = list(storage_client.list_buckets())

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    # blob.upload_from_filename(path_to_file)
    blob.upload_from_string(content)

    #returns a public url
    return blob.public_url

def cloud_delete():
    from google.cloud import storage

    my_storage = storage.Client()
    bucket = my_storage.get_bucket('meeting_stt_temp')
    blobs = bucket.list_blobs()
    print("blobs", blobs)
    for blob in blobs:
        print(blob)
        blob.delete()



if __name__ == "__main__":
    # print(cloud_upload("audio", "C:/Users/wuala/Documents/Final/src/python_back/test_file.txt", "meeting_stt_temp"))
    cloud_delete()