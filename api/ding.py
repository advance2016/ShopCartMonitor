import time
from dingtalkchatbot.chatbot import DingtalkChatbot
from queue import Queue
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import Future
from functools import partial

from settings.default_settings import DING_WAIT_TIME
from settings.default_settings import LOOP_WAIT_TIME
from settings.default_settings import DING_ACCESS_TOKEN
from settings.default_settings import DING_SECRET_KEY

class WebHookAPI(object):
    def __init__(self, access_token, secret_key) -> None:
        self.webhookapi = 'https://oapi.dingtalk.com/robot/send?access_token={}'.format(
            access_token or DING_ACCESS_TOKEN)
        self.secret_key = secret_key or DING_SECRET_KEY
        self.ding_manager = DingtalkChatbot(
            self.webhookapi, secret=self.secret_key)
    def message(self, msg):
        print("****************",msg)
        if msg:
            res = self.ding_manager.send_text(msg)
            return res

    def send_loop(self, queue: Queue, tp: ThreadPoolExecutor):
        while True:
            print("*************************",queue.empty())
            if not queue.empty():
                msg = queue.get()
                tp.submit(self.message, msg).add_done_callback(partial(partial(self.process_send_result,queue),msg))
                time.sleep(DING_WAIT_TIME)
            time.sleep(LOOP_WAIT_TIME)

    def process_send_result(self,queue: Queue, msg: str, future: Future):
        resp_data = future.result()
        print("resp_data ===>",resp_data)
        if resp_data and resp_data.get("errcode"):
            queue.put(msg)
        else:
            print("send res:{}".format(resp_data))




