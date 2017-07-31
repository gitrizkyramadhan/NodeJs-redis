from post_reciever_message import PostReceiverMessage

post_receiver = PostReceiverMessage()

class NoIntent():

    def do(self, msisdn, ask, answer, first_name, socketid):
        post_receiver.sendMessageToCather(msisdn, socketid, answer, first_name)


