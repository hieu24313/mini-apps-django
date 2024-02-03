from django.shortcuts import render
import base64
import requests
from urllib3 import request


# Create your views here.


def get_access_token():
    client_id = "ATeJhyrm4L9RkGnHbVTbQfoxt35cm6PnaZB0kyssykdb4_bBy6nXqsM_Syf1iav4SAnyKiF-oPVPEr3K"
    secret_key = "EBNvOxTCHVYDctjMVkxWBYBxrqcxZadIOrNq3il-yD7cJaBSCOqlSrmyJfLuWQ16nAKmwpT4Nx71tM-1"

    # Thông tin API OAuth 2.0 của PayPal
    oauth_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    auth_header = f"{client_id}:{secret_key}"

    # Bảo mật Base64 của thông tin xác thực
    base64_auth = base64.b64encode(auth_header.encode("utf-8")).decode("utf-8")

    # Yêu cầu mã xác thực (Authorization Code)
    auth_response = requests.post(
        oauth_url,
        headers={
            "Authorization": f"Basic {base64_auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data="grant_type=client_credentials",
    )

    if auth_response.status_code == 200:
        access_token = auth_response.json()["access_token"]
        return access_token
        print(f"Access Token: {access_token}")
    else:
        print(f"Failed to get Access Token. Status code: {auth_response.status_code}")
        print(auth_response.text)


def create_payment(request):
    your_paypal_access_token = get_access_token()
    # Thực hiện các thao tác cần thiết để tạo thanh toán
    # ...

    # Gọi API PayPal để tạo thanh toán
    paypal_api_url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {your_paypal_access_token}",  # Thay thế bằng Access Token của bạn
    }

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "10.00",
                },
            }
        ],
        "application_context": {
            "return_url": "http://127.0.0.1:8000/paypal/capture_payment/",
            "cancel_url": "http://127.0.0.1:8000/paypal/capture_payment/",
        }
    }

    response = requests.post(paypal_api_url, json=payload, headers=headers)
    print(response)
    if response.status_code == 201:
        data = response.json()
        approval_url = next(link["href"] for link in data["links"] if link["rel"] == "approve")
        return render(request, "payment/redirect.html", {"approval_url": approval_url})
    else:
        return render(request, "payment/error.html")


def capture_payment(request):
    your_paypal_access_token = get_access_token()
    # Lấy thông tin từ query parameters
    order_id = request.GET.get("token")

    # Gọi API PayPal để xác nhận thanh toán
    capture_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {your_paypal_access_token}",  # Thay thế bằng Access Token của bạn
    }

    response = requests.post(capture_url, headers=headers)
    print(response)
    if response.status_code == 201:

        # Thanh toán thành công, thực hiện các thao tác cần thiết
        # ...
        return render(request, "payment/success.html")
    else:
        return render(request, "payment/error.html")


