# SimpleRNG_Microservice
RNG Microservice that uses ZMQ

This microservice generates a random number between 1 and 100000, using ZMQ for client and server transfer.

To run:
```
python3 -m venv myenv 
source myenv/bin/activate
pip install zmq     
```
Terminal 1:\
`python3 RNG.py`

Terminal 2:\
`python3 test_client.py`


