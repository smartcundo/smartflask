from flask_script import Manager
import boto3
import botocore.exceptions
import os
import ConfigParser

import logging
logger = logging.getLogger()

aws_config_file = os.path.join(os.getenv("HOME"), ".aws", "credentials")
manager = Manager(usage="AWS management tools")
_aws_access_key_id = None
_aws_secret_access_key = None


def deactivate_access_keys(username):
    global _aws_access_key_id
    global _aws_secret_access_key
    try:
        _iam_client = boto3.client(
            'iam',
            aws_access_key_id=_aws_access_key_id,
            aws_secret_access_key=_aws_secret_access_key)
        access_key_metadata = _iam_client.list_access_keys(UserName=username)['AccessKeyMetadata']
        if len(access_key_metadata) > 0:
            print("Deactivating access keys for: %s" % username)
        else:
            print("%s does not have any access keys associated [OK]" % username)
        for access_key in access_key_metadata:
            access_key_id_to_deactivate = access_key['AccessKeyId']
            print("Deactivating access key: %s ..." % access_key_id_to_deactivate),
            response = _iam_client.update_access_key(
                UserName=username,
                AccessKeyId=access_key_id_to_deactivate,
                Status='Inactive',)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print("SUCCESS!")
            else:
                print("FAILED!")
    except NotImplemented as e:
        print(e.message)


def delete_password(username):
    global _aws_access_key_id
    global _aws_secret_access_key
    try:
        _iam_client = boto3.client(
            'iam',
            aws_access_key_id=_aws_access_key_id,
            aws_secret_access_key=_aws_secret_access_key)
        print("Deleting password for: %s ..." % username),
        response = _iam_client.delete_login_profile(UserName=username)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("SUCCESS!")
        else:
            print("FAILED!")

    except botocore.exceptions.ClientError as e:
        print("Login Profile for User %s does not have a password [OK]" % username)


@manager.option('-c', '--config', dest="config_file", help="location of aws config file", default=aws_config_file)
@manager.option('-u', '--user', dest='username', default='user')
@manager.option('-a', '--account', dest='aws_account', default='default')
@manager.option('-p', '--profiles', dest='all_profiles', action="store_true", default=False)
def disable(username, config_file, aws_account, all_profiles=False):
    try:
        global _aws_access_key_id
        global _aws_secret_access_key
        print("Disable user: %s" % username)
        print("Using AWS credentials config file: %s" % config_file)
        configs = ConfigParser.ConfigParser()
        configs.read(config_file)
        if all_profiles:
            profiles = configs.sections()
        else:
            profiles = [aws_account]

        for profile in profiles:
            try:
                _aws_access_key_id = configs.get(profile, 'aws_access_key_id')
                _aws_secret_access_key = configs.get(profile, 'aws_secret_access_key')
                print("[AWS Account %s]" % profile)
                delete_password(username)
                deactivate_access_keys(username)
            except ConfigParser.NoSectionError:
                msg = "Profile [%s] not found in %s" % (profile, config_file)
                logger.debug(msg)

    except NotImplementedError as e:
        print(e.message)


if __name__ == "__main__":
    disable("PatrickWilson", aws_config_file, "profile amp")