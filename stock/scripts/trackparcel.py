import requests

#url = "https://tracking.dtdc.com/ctbs-tracking/customerInterface.tr?" \
#     "submitName=showCITrackingDetails&cnNo={trackingid}&cType=Consignment"

url = "https://ebookingbackend.shipsy.in/trackConsignment?reference_number={trackingid}"

def getcourierdetails(trackingid):
    if trackingid == 'nan':
        return "Not Shipped"
    print(trackingid)
    headers = {"accept": "application/json, text/javascript, text/html, application/xml, text/xml, */*"}
    print(url.format(trackingid=trackingid))
    try:
        resp = requests.get(url.format(trackingid=trackingid), headers=headers)
        data = resp.json()
        return data['data']['status_external']
    except Exception as e:
        print(e)
        return "NotFound"


#getcourierdetails("NaN")