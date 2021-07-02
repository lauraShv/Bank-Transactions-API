import json
import requests
import http.client
import webbrowser

client_id = 'VpxC64Rh4FjolBzJEHk4'
client_secret = 'MyqmHnKuWxp1vcsA0LzC'
redirect_uri = 'https://locallhost.com/'
scope = ['psd2_accounts', 'psd2_payments']

def OAuth(client_id, client_secret, redirect_uri, scope):
    """
    Input: 
        client_id - aplication id
        client_secret - aplication secret
        redirect_uri - callback url used by the app
        scope - list of scope specific for an API
    Output:
        token - acess token
    """
    
    url = "https://api-sandbox.sebgroup.com/mga/sps/oauth/oauth20/authorize" 
    params =   {'client_id' : client_id,
                'scope' :  ' '.join(scope),
                'redirect_uri' : redirect_uri,
                'response_type' : 'code'}
    headers = { 'accept': "text/html" }
    response = requests.request("GET", url, params=params, headers=headers)
    
    # Interact with the user
    print('You are about to get redirected to the login page.\n \
           After you have logged in, copy the callback url here.')
    input('<PRESS ENTER TO LOG IN>')
    webbrowser.open(response.url)
    callback_url = input('Copy the callback link here:')
    idx = callback_url.find('code=')
    code = callback_url[idx+5:]
    
    # Retrieve the token
    conn = http.client.HTTPSConnection("api-sandbox.sebgroup.com")
    payload = f"client_id={client_id}&client_secret={client_secret}&code={code}&redirect_uri={redirect_uri}&grant_type=authorization_code"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json"
        }
    
    conn.request("POST", "/mga/sps/oauth/oauth20/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    token = data.decode("utf-8")
    token = json.loads(token)
    return token

returned = OAuth(client_id, client_secret, redirect_uri, scope)
access_token = returned['access_token']
print('Access token: ' + access_token)


# Function returns a list of a user´s accounts.
x_id = "123"
def accounts(x_request_id):

    conn = http.client.HTTPSConnection("api-sandbox.sebgroup.com")

    headers = {
        'accept': 'application/json',
        'X-Request-ID': x_request_id,
        'Authorization': f"Bearer {access_token}"
        }

    conn.request("GET", "/ais/v7/identified2/accounts", headers=headers)

    res = conn.getresponse()
    data = res.read()
    info = data.decode("utf-8")
    info = json.loads(info)
    return info

account_list = accounts(x_id)
print(account_list)

# From the account_list printed above, select a recourceId and copy&paste in the input.
user_id = input('Enter user_id:')

# Function returns detailed account information, potentially including balances for one 
# specific account.
def account_id(x_request_id, account):
    conn = http.client.HTTPSConnection("api-sandbox.sebgroup.com")

    headers = {
        'accept': 'application/json',
        'X-Request-ID': x_request_id,
        'Authorization': f"Bearer {access_token}"
        }

    conn.request("GET", f"/ais/v7/identified2/accounts/{account}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


# Function returns balances for a specific account
def account_balance(x_request_id, account):
    conn = http.client.HTTPSConnection("api-sandbox.sebgroup.com")
    headers = {
        'accept': 'application/json',
        'X-Request-ID': x_request_id,
        'Authorization': f"Bearer {access_token}"
        }

    conn.request("GET", f"/ais/v7/identified2/accounts/{account}/balances", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


# Function returns a list of transactions for one specific account.
def account_transactions(x_request_id, account):
    conn = http.client.HTTPSConnection("api-sandbox.sebgroup.com")

    headers = {
        'accept': 'application/json',
        'X-Request-ID': x_request_id,
        'Authorization': f"Bearer {access_token}"
        }

    conn.request("GET", f"/ais/v7/identified2/accounts/{account}/transactions?bookingStatus=booked", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


print(account_id(x_id, user_id))
print(account_balance(x_id, user_id))
print(account_transactions(x_id, user_id))
