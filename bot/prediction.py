import zmq.asyncio
import logging
import sys
from constants import ZMQ_PORT

try:
    context = zmq.asyncio.Context()
    print("Connecting to model server...")
    socket = context.socket(zmq.DEALER)
    socket.connect("tcp://localhost:" + ZMQ_PORT)
except ConnectionError:
    print("You must start the model server in toxicity/main.py")
    sys.exit(1)


async def predict_text_prob(model_id: int, text: str):
    await socket.send(b"", zmq.SNDMORE)
    await socket.send_pyobj({"model": model_id, "text": text})
    await socket.recv()
    res = await socket.recv_pyobj()
    if res['type'] == 0:
        return res['prob'], res['cutoff']
    else:
        logging.error("INVALID RESPONSE FROM MODEL SERVER")
        return False


async def predict_text(model_id: int, text: str):
    t, c = await predict_text_prob(model_id, text)
    return t > c
