import requests

url = "https://tracking.dtdc.com/ctbs-tracking/customerInterface.tr?" \
      "submitName=showCITrackingDetails&cnNo={trackingid}&cType=Consignment"


def getcourierdetails(trackingid):
    print(trackingid)
    headers = {"accept": "application/json"}
    print(url.format(trackingid=trackingid))
    resp = requests.get(url.format(trackingid=trackingid), headers=headers)
    #print(resp)
    data = resp.text
    print(data)
    if 'Successfully Delivered' in data:
        print("Parcel Delivered")
        return 0
    else:
        print("Pending")
        return 1
