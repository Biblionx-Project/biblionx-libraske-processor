from queues import queueconsume
from queues import queuepublisher
from utils import holistic_callback
from utils import holistic_pontuation
from utils import configreader
import json


class Worker:

    def __init__(self):


        self._rabbitcfg = configreader.load_configs("RabbitMQ")
        self.workercfg = configreader.load_configs("Worker")

        queueConf = self.workercfg.get("ReceiveQueue", "frame_receiver")
        hostConf = self._rabbitcfg.get("Host", "localhost")
        portConf = self._rabbitcfg.get("Port", "5672")
        userConf = self._rabbitcfg.get("Username", "Guest")
        pwdConf = self._rabbitcfg.get("Password", "Guest")
        print ("Queue, Host, Port, User, PWD = " + queueConf + " " + hostConf+ " " + portConf+ " " + userConf+ " " + pwdConf)


        self.__publisherconfigure = queuepublisher.RabbitmqConfigure(queue="frame_receiver",
                                                                     host=hostConf,
                                                                     port=portConf,
                                                                     user=userConf,
                                                                     password=pwdConf,
                                                                     routingKey="frame_receiver",
                                                                     exchange='')

        self.__consumerconfigure = queueconsume.RabbitMqServerConfigure(queue=queueConf,
                                                                        host=hostConf,
                                                                        port=portConf,
                                                                        user=userConf,
                                                                        password=pwdConf,
                                                                        persistent=True
                                                                        )

        self.__consumer = queueconsume.RabbitmqServer(self.__consumerconfigure)

        self.__score_eval = holistic_pontuation.GetScore()
        self.__holistic_process = holistic_callback.HolisticCallback.test_process

    def __publisher_message(self, msg):

        with queuepublisher.RabbitMq(self.__publisherconfigure) as rabbitmq:
            rabbitmq.publish(payload=msg)

    def __callback(self, _ch, _method, _properties, body):

        message = json.loads(body)

        if(len(message)>2):

            results, video_id, frame_id, session_id = self.__holistic_process(body)

            print(f"video-id: {video_id}")

            score = self.__score_eval.get_score(
                results, video_id, frame_id)
            try:
                score_float = float(score)
            except (ValueError, TypeError):
                score_float = 0.0

            if score_float > 0:
                score_str = f"{score_float:.2f}"
                score_decimals = 100 if score_float >= 1.0 else (int(score_str.split(".")[1][:2]) if "." in score_str else 0)
                final_score = (score_decimals + 50 * 2) // 3
            else:
                final_score = 0

            msg = {
                "idGameSession": session_id,
                "pontuation": final_score
            }

            payload = json.dumps(msg)

            self.__publisher_message(payload)

    def start(self, queue):

        self.__consumer.startserver(queue, self.__callback)


if __name__ == "__main__":

    workercfg = configreader.load_configs("Worker")
    
    worker = Worker()
    worker.start(workercfg.get("ReceiveQueue"))
