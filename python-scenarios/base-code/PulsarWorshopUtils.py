import argparse
import random
import re
import string
import traceback
from abc import ABC, abstractmethod

import pulsar
from jproperties import Properties

from PulsarWorkshopLog import *


class InvalidArgumentError(Exception):
    pass


class InvalidConfigError(Exception):
    pass


def get_prop_val(properties, key, default):
    prop_value = properties.get(key)
    return prop_value[0] or default


# Remove the leading and trailing quote
def de_quote(s):
    return re.sub(r'^"|"$', '', s)


def str2bool(s):
    return s.lower() in ['true', '1', 't', 'y', 'yes']


def random_alpha_numeric(length):
    return ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))


class PulsarWorkshopCmdApp(ABC):
    def __init__(self):
        setup_logging(filename=self.__class__.__name__, append_time=True)

        self.args = None
        self.unknown = None

        self.num_msg_to_proc = None
        self.topic_name = None
        self.conn_file_path = None
        self.use_astra_streaming = None

        self.client_conn_properties = None
        self.pulsar_client = None

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "-n", "--numMsg", help="Number of messages to process.", type=int, default=100)
        self.parser.add_argument(
            "-t", "--topic", help="Pulsar topic name.")
        self.parser.add_argument(
            "-c", "--connFile", help="Pulsar \"client.conf\" file path.")
        self.parser.add_argument(
            "-a", "--astra", help="Use Astra Streaming as the Pulsar cluster", action="store_true")

    @abstractmethod
    def process_extended_input_params(self):
        pass

    @abstractmethod
    def execute(self):
        logging.info(">>> Executing the required message processing task ...")

        if self.pulsar_client is None:
            service_url = get_prop_val(self.client_conn_properties, 'brokerServiceUrl', '')
            if service_url.isspace():
                raise InvalidConfigError("The specified broker service can't be empty!")

            auth_method = None
            auth_plugin_class_name = get_prop_val(self.client_conn_properties, 'authPlugin', '')
            auth_params = get_prop_val(self.client_conn_properties, 'authParams', '')

            if not (auth_plugin_class_name.isspace() or auth_params.isspace()):
                if auth_params.startswith('token:'):
                    token_val = auth_params[6:]
                else:
                    auth_token_file_path = auth_params[5:]
                    if not os.path.isfile(auth_token_file_path):
                        raise InvalidConfigError("The specified token file path is invalid!")
                    else:
                        with open(auth_token_file_path, 'r') as token_file:
                            token_val = token_file.read().strip()

                auth_method = pulsar.AuthenticationToken(token_val)

            if self.use_astra_streaming:
                self.pulsar_client = pulsar.Client(service_url, authentication=auth_method)
            else:
                trust_certs_file_path = \
                    get_prop_val(self.client_conn_properties, 'tlsTrustCertsFilePath', '')
                allow_insecure_connection = \
                    get_prop_val(self.client_conn_properties, 'tlsAllowInsecureConnection', False)
                enable_host_verification = \
                    get_prop_val(self.client_conn_properties, 'tlsEnableHostnameVerification', False)

                self.pulsar_client = \
                    pulsar.Client(service_url,
                                  authentication=auth_method,
                                  tls_trust_certs_file_path=trust_certs_file_path,
                                  tls_allow_insecure_connection=allow_insecure_connection,
                                  tls_validate_hostname=enable_host_verification)

    @abstractmethod
    def term_cmd_app(self):
        if self.pulsar_client is not None:
            self.pulsar_client.close()

    def process_input_params(self):
        logging.info(">>> Parsing input parameters ...")

        self.args, self.unknown = self.parser.parse_known_args()

        valid_num_msg = True
        try:
            self.num_msg_to_proc = int(self.args.numMsg)
            # -1 means to process all available messages
            if not (self.num_msg_to_proc > 0 or self.num_msg_to_proc == -1):
                valid_num_msg = False
        except ValueError:
            valid_num_msg = False
        if not valid_num_msg:
            raise InvalidArgumentError(
                "Invalid value \"{}\" of the input parameter \"-n\", which must be a positive integer"
                .format(self.args.numMsg))

        self.topic_name = self.args.topic
        if self.topic_name is None or self.topic_name.isspace():
            raise InvalidArgumentError(
                "The specified Pulsar topic name (input parameter \"-t\") can't be an empty string!")

        self.conn_file_path = self.args.connFile
        if self.conn_file_path is None or self.conn_file_path.isspace() or not os.path.isfile(self.conn_file_path):
            raise InvalidArgumentError(
                "Invalid value \"{}\" of the input parameter \"-c\". "
                "It must point to a valid file path!".format(self.args.connFile))
        else:
            self.client_conn_properties = Properties()
            with open(self.conn_file_path, 'rb') as prop_file:
                self.client_conn_properties.load(prop_file)

        self.use_astra_streaming = self.args.astra

        self.process_extended_input_params()

    def run_cmd_app(self):
        logging.info(">>> Start message processing application ...")

        try:
            self.process_input_params()
            self.execute()
        except InvalidArgumentError:
            logging.error("Invalid commandline input parameter error detected ...")
            traceback.print_exc()
        except InvalidConfigError:
            logging.error("Invalid config parameter error detected ...")
            traceback.print_exc()
        except SystemExit:
            pass
        except:
            logging.error("Unexpected errors detected ...")
            traceback.print_exc()
        finally:
            logging.info(">>> Terminate message processing application ...")
            self.term_cmd_app()
            sys.exit()
