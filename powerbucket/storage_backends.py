from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    default_acl='private'
    location = 'media'
    file_overwrite = False
    custom_domain = False
