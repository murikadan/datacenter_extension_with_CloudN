
"""
Extend an On-Prem DC to AWS using CloudN
"""
import json
import requests

def setup_conn(ip):
    "set up an HTTP session with CloudN and return session_id (CID)"
    try:
        creds = open('acx_credentials.txt', 'r')
    except OSError:
        print('Unable to locate credentials for your aviatrix account')
        return 1
    else:
        username = (creds.readline()).rstrip('\n')
        password = (creds.readline()).rstrip('\n')
        creds.close()
    try:
        # SSL: Unable to verify CN as carmelosystems!!
        session_info = requests.get("https://" + ip + "/v1/api?action=login&username=" + username + "&password=" + password, verify=False)
        session_id = (json.loads(session_info.text))['CID']
    except requests.exceptions.RequestException as HTTPException:
        print("Failed to connect to CloudN! - ERROR: ", HTTPException)
        return -1
    return session_id

def setup_license(ip):
    "call this function once to set up license"
    session_id = setup_conn(ip)
    try:
        license = open('license.txt', 'r')
    except OSError:
        print('Unable to locate license no for your aviatrix account')
        return 1
    else:
        license_id = license.read()
        license.close()
    try:
        # SSL: Unable to verify CN as carmelosystems!!
        requests.get("https://" + ip + "/v1/api?CID=" + session_id + "&action=setup_customer_id&customer_id=" + license_id, verify=False)
    except requests.exceptions.RequestException as HTTPException:
        print("Failed to add license! - ERROR: ", HTTPException)
        return -1

def main():
    "main function!!"
    setup_license(IP)
    session_id = setup_conn(IP)
    try:
        creds = open('aws_credentials.txt', 'r')
    except OSError:
        print('Unable to locate credentials for your aws account')
        return 1
    else:
        aws_access_key = (creds.readline()).rstrip('\n')
        aws_secret_key = (creds.readline()).rstrip('\n')
        creds.close()
    try:
        vpc_info = requests.get("https://" + IP + "/v1/api?CID=" + session_id + "&action=setup_max_vpc_containers&vpc_num=" + VPC_NUM, verify=False)
        vpc_list = (vpc_info.json())['results']['cidr_list']
        # Set up a user account
        payload = {'CID': session_id, 'action': 'setup_account_profile',
                   'account_name' : 'new_user', 'account_password' : 'changeme', 'account_email': 'yasser.murikadan@live.com',
                   'cloud_type': '1', 
                   'aws_account_number': AWS_ACCOUNT_NUMBER, 'aws_access_key': aws_access_key, 'aws_secret_key': aws_secret_key}
        # SSL: Unable to verify CN as carmelosystems!!
        requests.post("https://" + IP + "/v1/api", data=payload, verify=False)
        # Create VPC for datacenter extension
        payload = {'CID': session_id, 'action': 'create_container', 'cloud_type': '1', 'account_name' : 'new_user',
                   'vpc_name': VPC_NAME, 'vpc_reg': VPC_REG, 'vpc_size': VPC_SIZE, 'vpc_net': vpc_list[0]}                   
        # SSL: Unable to verify CN as carmelosystems!!
        requests.post("https://" + IP + "/v1/api", data=payload, verify=False)
    except requests.exceptions.RequestException as HTTPException:
        print("HTTP request failed with ERROR: ", HTTPException)
        return -1

if __name__ == "__main__":
    IP = "13.126.28.162"
    VPC_NUM = "4"
    AWS_ACCOUNT_NUMBER = "982805288348"
    VPC_NAME = "dc1-us-west-1"
    VPC_REG = "us-west-2"
    VPC_SIZE = "t2.micro"
    main()
