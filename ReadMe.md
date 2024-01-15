sudo apt-get install -y python3-venv
python3 -m venv df-env
source df-env/bin/activate
python3 -m pip install -q --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt

python3 -m pip install apache-beam[gcp]


python3 dataflow.py --runner=DataflowRunner --requirements_file=./requirements.txt --project playground-s-11-fa55bb12 --region us-central1 --experiments=use_runner_v2 
Ref: https://github.com/jccatrinck/dataflow-cloud-sql-python