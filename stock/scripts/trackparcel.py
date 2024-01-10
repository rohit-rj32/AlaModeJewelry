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
    resp = requests.get(url.format(trackingid=trackingid), headers=headers)
    #print(resp)
    data = resp.json()
    print(data['data']['status_external'])
    return data['data']['status_external']

#getcourierdetails("NaN")