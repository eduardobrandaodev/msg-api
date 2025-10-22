import json
import urllib.request

def handler(request):
    instance_id = "3E91BAFCF8A981797EBC0E310151217F"
    token = "4C0A4A2331F861CA5DD02108"
    phone = "5521995425261"
    mensagem = "oii amorrr bom diaaaa so lembrando q eu te amo mais"

    url = f"https://api.z-api.io/instances/{instance_id}/token/{token}/send-messages"

    payload = json.dumps({
        "phone": phone,
        "message": mensagem
    }).encode('utf-8')

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        req = urllib.request.Request(url, data=payload, headers=headers)
        response = urllib.request.urlopen(req)
        result = response.read().decode()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "response": json.loads(result)
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": str(e)
            })
        }
