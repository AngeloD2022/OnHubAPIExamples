import requests
import OHAuth


def createWanSpeedTestOperation(token, systemId):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',

        'Authorization': f'Bearer {token}',
    }

    params = (
        ('prettyPrint', 'false'),
    )

    data = '{}'

    response = requests.post(f'https://googlehomefoyer-pa.googleapis.com/v2/groups/{systemId}/wanSpeedTest',
                             headers=headers, params=params, data=data)

    operationId = response.json()["operation"]["operationId"]

    return operationId


def checkOperation(token, operationId):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f'Bearer {token}',
    }

    params = (
        ('prettyPrint', 'false'),
    )

    response = requests.get(
        f'https://googlehomefoyer-pa.googleapis.com/v2/operations/{operationId}',
        headers=headers, params=params)

    return response.json()


def wlanSpeedTestResults(token, systemId, count):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',

        'Authorization': f'Bearer {token}',
    }

    params = (
        ('prettyPrint', 'false'),
        ('maxResultCount', count)
    )

    response = requests.get(f'https://googlehomefoyer-pa.googleapis.com/v2/groups/{systemId}/speedTestResults',
                            headers=headers, params=params)

    return response.json()["speedTestResults"]


if __name__ == '__main__':
    refresh = OHAuth.getRefreshToken()
    systemId = "INSERT_GROUP_ID_HERE"

    apitoken = OHAuth.getAPIToken(refresh)

    print("Starting test...")

    opId = createWanSpeedTestOperation(apitoken, systemId)

    status = checkOperation(apitoken, opId)["operationState"]

    print("The test has started. Please wait...")

    # Wait until operation complete...
    while status != "DONE":
        status = checkOperation(apitoken, opId)["operationState"]

    # Get latest test's results...
    results = wlanSpeedTestResults(apitoken, systemId, 1)[0]

    print("Test complete!")

    print("Upload bits/second: " + results["transmitWanSpeedBps"])
    print("Download bits/second: " + results["receiveWanSpeedBps"])
