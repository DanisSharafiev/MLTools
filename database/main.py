from aiobotocore.session import get_session

class S3Client:
        def __init__(
                self,
                access_key: str,
                secret_key: str,
                endpoint_url: str,
                bucket_name: str,):
                self.config = {
                        "aws_access_key_id": access_key,
                        "aws_secret_access_key": secret_key,
                        "endpoint_url": endpoint_url,
                        "bucket_name": bucket_name,
                }
                self.bucket_name = bucket_name
                self.session = get_session()
        async def get_client(self):
                async with self.session.create_client(
                        "s3",
                        **self.config,
                ) as client:
                        yield client
        async def upload_file(
                        self,
                        file_path: str,
        ):
                object_name = file_path.split("/")[-1]
                async with self.get_client() as client:
                        with open(file_path, "rb") as file:
                                await client.put_object(
                                        Body = file,
                                        Bucket = self.bucket_name,
                                        Key = object_name,
                                )

async def main():
        client = S3Client(
                access_key = "mockadmin",
                secret_key= "mockadmin",
                endpoint_url= "http://mock.ru:9000",
                bucket_name= "mock",
        )