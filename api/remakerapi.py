import requests
import time
import base64
# def remakerswapfaceapi(img1,img2):
#     url = 'https://developer.remaker.ai/api/remaker/v1/face-swap/create-job'
#     headers = {
#         'accept': 'application/json',
#         'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTU2NTg4NTMsInByb2R1Y3RfY29kZSI6IjA2NzAwMyIsInRpbWUiOjE3MzQ4ODY3OTZ9.0VfNf5o5M_9lXbg5VT6Ezhh4G6wpiqT-4pjei5D6abE',
#     }
#     files = {
#         'target_image': img1,
#         'swap_image': img2,
#     }
#     print("sending request")
#     response = requests.post(url, headers=headers, files=files)
#     # print(response.data)
#     responsedata = response.json()
#     print(responsedata)
#     time.sleep(3)
#     url  = 'https://developer.remaker.ai/api/remaker/v1/face-swap/' + responsedata['result']['job_id']
#     response = requests.get(url, headers=headers)
#     responsedata = response.json()
#     return responsedata['result']['output_image_url']
import requests
def remakerswapfaceapi(img1,img2_base64):

    url = "https://faceswap-image-transformation-api.p.rapidapi.com/faceswapgroupbase64onetoall"

    payload = {
        "MatchGender": True,
        "MaximumFaceSwapNumber": 5,
    "TargetImageBase64Data": base64.b64encode(img1.read()).decode('utf-8'),
    "SourceImageBase64Data": img2_base64
    # "SourceImageBase64Data": base64.b64encode(img2.read()).decode('utf-8')
    }
    headers = {
        "x-rapidapi-key": "cdf2111ec9msh807d34b748a828dp157047jsn7125270e8f92",
        "x-rapidapi-host": "faceswap-image-transformation-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    responsedata = response.json()
    print(responsedata)
    return responsedata['ResultImageUrl']