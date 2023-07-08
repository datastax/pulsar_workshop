import logging
import os
import sys
import fileinput

from pulsar.schema import JsonSchema

script_dir = os.path.dirname(__file__)
util_module_dir: str = os.path.abspath(os.path.join(script_dir, '../../..', 'base-code'))
sys.path.insert(0, util_module_dir)

import PulsarWorshopUtils as PwUtil
import PulsarWorkShopPoJo as PwPojo


class IoTSensorProducer(PwUtil.PulsarWorkshopCmdApp):
    def __init__(self):
        self.iot_csv_file = None
        self.producer = None
        self.topic_schema = JsonSchema(PwPojo.IoTSensorDataRaw)

        super().__init__()

        self.parser.add_argument("-csv", "--csvFile", help="IoT sensor data CSV file.")

    def process_extended_input_params(self):
        self.iot_csv_file = self.args.csvFile

        if self.iot_csv_file is None or self.iot_csv_file.isspace() or not os.path.isfile(self.iot_csv_file):
            raise PwUtil.InvalidArgumentError(
                "Invalid value \"{}\" of the input parameter \"-c\". "
                "It must point to a valid file path!".format(self.args.csvFile))

    def execute(self):
        super().execute()

        if self.producer is None:
            self.producer = self.pulsar_client.create_producer(self.topic_name, schema=self.topic_schema)

        msg_sent = 0
        first_line = True
        for line in fileinput.input([self.iot_csv_file]):
            if msg_sent < self.num_msg_to_proc or self.num_msg_to_proc == -1:
                if not first_line:
                    field_vals = line.strip().split(',')

                    msg_payload = PwPojo.IoTSensorDataRaw(
                        ts=PwUtil.dequote(field_vals[0]),
                        device=PwUtil.dequote(field_vals[1]),
                        co=float(PwUtil.dequote(field_vals[2])),
                        humidity=float(PwUtil.dequote(field_vals[3])),
                        light=PwUtil.str2bool(PwUtil.dequote(field_vals[4])),
                        lpg=float(PwUtil.dequote(field_vals[5])),
                        motion=PwUtil.str2bool(PwUtil.dequote(field_vals[6])),
                        smoke=float(PwUtil.dequote(field_vals[7])),
                        temp=float(PwUtil.dequote(field_vals[8]))
                    )
                    message_id = self.producer.send(msg_payload)
                    logging.debug(">>> successfully published the message '{}' id='{}'".format(msg_payload, message_id))
                    msg_sent = msg_sent + 1
                else:
                    first_line = False
            else:
                break

    def term_cmd_app(self):
        if self.producer is not None:
            self.producer.close()

        super().term_cmd_app()


if __name__ == '__main__':
    producer_app = IoTSensorProducer()
    producer_app.run_cmd_app()
