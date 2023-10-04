Sample readme for develop branch placeholder





steps to run :



1.create a conda env
2.actiavte conda env
3.conda install pip in order to rectify pip
4.conda install nodejs in order to rectify npm
5.pip install -r requirements.txt
6. run python main.py from ic_visualai_dataprocessing_service or python -m uvicorn main:app




test the service by using the below query:

{"query":"population volume",
"filter":{
    "claim_completion_month_adj":"'July','May'"
}
}


