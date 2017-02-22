from flask_script import Manager
import os
import ConfigParser
from twilio.rest.client import TwilioRestClient


twilio_config_file = os.path.join(os.getenv("HOME"), ".twilio", "credentials")
manager = Manager(usage="Twilio management tools")

twilio_account_manager = Manager(usage='Twilio Account Manager')
manager.add_command('account', twilio_account_manager)


def get_account_token(config_file, twilio_account_name):
    print("Using twilio credentials config file: %s" % config_file)
    try:
        configs = ConfigParser.ConfigParser()
        configs.read(config_file)
        print(configs.options(twilio_account_name))
        _twilio_account_id = configs.get(twilio_account_name, 'twilio_account_id')
        _twilio_token_id = configs.get(twilio_account_name, 'twilio_token_id')
        _twilio_sid_id = configs.get(twilio_account_name, 'twilio_sid_id')
    except ConfigParser.NoOptionError as no_option_error:
        raise no_option_error
    except Exception as e:
        raise e
    return (_twilio_account_id, _twilio_token_id, _twilio_sid_id)


@manager.option('-c', '--config', dest="config_file", help="location of aws config file", default=twilio_config_file)
@manager.option('-a', '--account', dest='twilio_account_name', default='pddevops')
@manager.option('-n', '--number', dest='phone_number', default='unchanged')
def update(username, config_file, twilio_account_name):
    try:
        print("Update phone number for: %s" % twilio_account_name)
        _twilio_account_id, _twilio_token_id, _twilio_sid_id = get_account_token(config_file, twilio_account_name)
        _twilio_client = TwilioRestClient(_twilio_account_id, _twilio_token_id)
        number = _twilio_client.phone_numbers.get(_twilio_sid_id)
        print(number.name.capitalize())
    except Exception as e:
        raise e


@twilio_account_manager.option('-n', '--name', dest='name', default='Account Friendly Name')
@twilio_account_manager.option('-c', '--config', dest="config_file", help="location of aws config file", default=twilio_config_file)
@twilio_account_manager.option('-a', '--account', dest='twilio_account_name', default='pddevops')
def create(name, config_file, twilio_account_name):
    try:
        print("Creating subaccount for: %s" % name)
        _twilio_account_id, _twilio_token_id, _twilio_sid_id = get_account_token(config_file, twilio_account_name)
        _twilio_client = TwilioRestClient(_twilio_account_id, _twilio_token_id)
        subaccount = _twilio_client.accounts.create(name=name)
        print(subaccount.name)
    except Exception as e:
        raise e


@twilio_account_manager.option('-s', '--sid', dest='suspend_account_sid', default='Suspend account SID')
@twilio_account_manager.option('-c', '--config', dest="config_file", help="location of aws config file", default=twilio_config_file)
@twilio_account_manager.option('-a', '--account', dest='twilio_account_name', default='pddevops')
def close(suspend_account_sid, config_file, twilio_account_name):
    try:
        print("Closing subaccount for: %s" % suspend_account_sid)
        _twilio_account_id, _twilio_token_id, _twilio_sid_id = get_account_token(config_file, twilio_account_name)
        _twilio_client = TwilioRestClient(_twilio_account_id, _twilio_token_id)
        subaccount = _twilio_client.accounts.get(suspend_account_sid)
        subaccount.suspend()
    except Exception as e:
        raise e


if __name__ == "__main__":
    create("Subaccount", twilio_config_file, "PDDEVOPS")