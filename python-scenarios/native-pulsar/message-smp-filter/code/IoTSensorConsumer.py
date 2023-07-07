import os
import sys

from _pulsar import ConsumerType
from pulsar.schema import JsonSchema

script_dir = os.path.dirname(__file__)
util_module_dir: str = os.path.abspath(os.path.join(script_dir, '../../..', 'base-code'))
sys.path.insert(0, util_module_dir)

import PulsarWorshopUtils as PwUtil
import PulsarWorkShopPoJo as PwPojo


def get_subscription_type(type_str):
    if (type_str is None):
        return ConsumerType.Exclusive
    else:
        type_str_upper = type_str.upper()

        if type_str_upper == 'EXCLUSIVE':
            return ConsumerType.Exclusive
        elif type_str_upper == 'SHARED':
            return ConsumerType.Shared
        elif type_str_upper == 'FAILOVER':
            return ConsumerType.Failover
        elif type_str_upper == 'KEY_SHARED':
            return ConsumerType.KeyShared
        else:
            print(f"Unrecognized subscription type: {type_str}. Use default \"EXCLUSIVE\" type!")
            return ConsumerType.Exclusive

class IoTSensorConsumer(PwUtil.PulsarWorkshopCmdApp):
    def __init__(self):
        self.sub_type = ConsumerType.Exclusive
        self.sub_name = None
        self.consumer = None
        self.topic_schema = JsonSchema(PwPojo.IoTSensorDataRaw)

        super().__init__()

        self.parser.add_argument("-sbt", "--subType", help="Pulsar subscription type.")
        self.parser.add_argument("-sbn", "--subName", help="Pulsar subscription name.")

    def process_extended_input_params(self):
        self.sub_name = self.args.subName
        if self.sub_name is None or self.sub_name.isspace():
            self.sub_name = PwUtil.random_alpha_numeric(15)

        self.sub_type = get_subscription_type(self.args.subType)

    def execute(self):
        super().execute()

        if self.consumer is None:
            self.consumer = self.pulsar_client.subscribe(self.topic_name,
                                                         self.sub_name,
                                                         self.sub_type,
                                                         schema=self.topic_schema)

        msg_recv = 0
        while True:
            if msg_recv < self.num_msg_to_proc or self.num_msg_to_proc == -1:
                msg = self.consumer.receive()
                try:
                    print("Acknowledge the received message '{}' id='{}'".format(msg.data(), msg.message_id()))
                    self.consumer.acknowledge(msg)
                except Exception:
                    print("Failed to receive the message; un-acknowledge it!")
                    self.consumer.negative_acknowledge(msg)
                msg_recv = msg_recv + 1
            else:
                break

    def term_cmd_app(self):
        if self.consumer is not None:
            self.consumer.close()

        super().term_cmd_app()


if __name__ == '__main__':
    consumer_app = IoTSensorConsumer()
    consumer_app.run_cmd_app()
