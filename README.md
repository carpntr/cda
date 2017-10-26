# cda
crypto-data-aggregator


## Setup
Clone repo and setup venv.
```
git clone https://github.com/AndrewLCarpenter/cda
cd cda
python3.6 -m venv venv
source venv/bin/activate
```

Install requirements.
```
# Todo: add this to makefile
# Can't  install arctic without installing cython first.
pip install cython
pip install git+https://github.com/manahl/arctic.git
pip install -r requirements.txt
```

Make sure everything works, then start up mongo container -- you need docker-compose for this.
Installation instructions for that are here: https://docs.docker.com/compose/install/

```
make test
make mongo
```

Ok, so your database should be up and running and ready to accept data. To launch the 
Binance stream:

```

```