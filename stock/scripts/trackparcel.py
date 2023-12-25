import requests

url = "https://tracking.dtdc.com/ctbs-tracking/customerInterface.tr?" \
      "submitName=showCITrackingDetails&cnNo=H39396336&cType=Consignment"


def getcourierdetails(trackingid):
    print(trackingid)
    headers = {"accept": "application/json"}
    resp = requests.get(url, headers=headers)
    #print(resp)
    data = resp.text

    if 'Successfully Delivered' in data:
        print("Parcel Delivered")
        return 0
    else:
        print("Pending")
        return 1
