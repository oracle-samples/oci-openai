1. Open openai-responses-api-samples as a Pycharm project or make it a current directory
2. Setup python venv `python3 -m venv venv`
3. Active venv `source venv/bin/activate`
4. install dependencies `pip install -r requirements.txt`
5. for session_token usage `oci session authenticate --region us-phoenix-1 --profile-name BoatOc1 --tenancy-name bmc_operator_access`
6. Set `export PYTHONPATH=.` in `openai-responses-api-sample` folder 
7. Now run the script from `openai-responses-api-sample` folder and it should use oci iam to make call