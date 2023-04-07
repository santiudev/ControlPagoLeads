import requests
import json

def get_hotmart_access_token(client_id, client_secret):
    url = "https://api-sec-vlc.hotmart.com/security/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic YTYzZjgwNmEtMjZhYy00NDFlLWE1NDItYmQ3MzQ0YTAxOTUyOjNjNzk1MTgzLTlmZWEtNGYwNC05MjlhLWY3YjYyYWFjYmQ5NA=="
    }
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print(f"Conectado con exito")
        return access_token
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None



def get_sales_history(access_token, product_id=None):
    url = "https://developers.hotmart.com/payments/api/v1/sales/history?transaction_status=BLOCKED,CHARGEBACK,NO_FUNDS,PRINTED_BILLET,PROTESTED,WAITING_PAYMENT"
    
    if product_id:
        url += f"&product_id={product_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        sales_history = response.json()
        return sales_history
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None



def main():
    client_id = "a63f806a-26ac-441e-a542-bd7344a01952"
    client_secret = "3c795183-9fea-4f04-929a-f7b62aacbd94"

    access_token = get_hotmart_access_token(client_id, client_secret)

    if access_token:
     
        hotmart_data = get_sales_history(access_token, product_id="")

        print(json.dumps(hotmart_data, indent=2))
    else:
        print("No se pudo obtener el token de acceso.")

if __name__ == "__main__":
    main()
