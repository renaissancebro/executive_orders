## Create a tracker for new policies from whitehouse.gov

local, staging, production modes for behaviour


## FLOW ##
1. Inputs: listings on executive order website section
2. Transformation: Check whether first update is same as one stored in sqlite last time
3. Outputs: Alerter, slack/emailer with short message to recipiant with name of order and date

Data = nouns
functions = verbs

Latest policy -> New Policy -> meta data, title date, name -> email template as output -> delivered alert 

Verbs/functions,
1. check_last_policy()
2. grab_meta_data()
3. make_email()
4. send_mail()
