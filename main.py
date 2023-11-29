import requests, json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Rrrrr is for request :D
r = requests.session()

debug = False

oopsies = []
yes = {'yes','y', 'ye'}
no = {'no','n'}

# Grab them json files boi
config = json.loads(open("config.json", "r").read())
items = json.loads(open("items.json", "r").read())

# Just a visual aid
if debug:
    print("Access Token: " + config['access_token']);
    print("Refresh Token: " + config['refresh_token']);
    print("User ID: " + config['userId']);


entitlementUrl = "https://nebula.starbreeze.com/platform/public/namespaces/pd3/users/" + config['userId'] + "/entitlements?limit=2147483647"

oopsUrl = "https://nebula.starbreeze.com/platform/public/namespaces/pd3/users/" + config['userId'] + "/entitlements/"

# Header is needed for GET and PUT (GET Entitlement and PUT Decrement)
headers = {
    "Host": "nebula.starbreeze.com",
    "Accept-Encoding": "deflate, gzip",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {config['access_token']}",
    "Namespace": "pd3",
    "Game-Client-Version": "1.0.0.0",
    "AccelByte-SDK-Version": "21.0.3",
    "AccelByte-OSS-Version": "0.8.11",
    "User-Agent": "PAYDAY3/++UE4+Release-4.27-CL-0 Windows/10.0.22621.1.256.64bit"
}

# Body is only used during the PUT 
body = {
	"useCount": 1,
	"options": []
}

# Have to add in the cookies for proper auth (IDK why it doesn't work without it, seems redundant)
r.cookies.set("access_token", config["access_token"]) 
r.cookies.set("refresh_token", config["refresh_token"]) 

# Let's see if you put in the proper tokens...
try:
    entitlements = requests.get(entitlementUrl, headers=headers, verify=False).json()["data"]
except requests.exceptions.HTTPError as errh:
    print ("HTTP Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting: ", errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error: ", errt)
except requests.exceptions.RequestException as err:
    print ("Request Exception: ", err)

if debug:
    print(entitlements)

# Let's check for your oopsies
for entitlement in entitlements:
    #print("Entitlement: " + entitlement["name"] + "  -  ID: " + entitlement["itemId"].upper())
    for item in items["items"]:
        #print("Item: " + item["name"] + "  -  ID: " + item["itemId"])
        if item["enabled"] == True and entitlement["itemId"].upper() == item["itemId"]:
            print("Found Item  -  NAME: " + item["name"] + "  -  ID: " + entitlement["itemId"] + "  -  SLOT: " + entitlement["id"])
            choice = input('Remove it? [Y/n] \n')
            if choice.lower() in yes:
                print("Queuing item to be removed...")
                oopsies.append(entitlement["id"])
            elif choice.lower() in no:
                print("Skipping item...")
            else:
                print("Invalid choice, skipping item...")

for oops in oopsies:
    # Let's see if you put in the proper tokens...
    try:
        choice = input('Are you sure you want to remove the item below? \nID: ' + oops + ' - [Y/n] ')
        if choice.lower() in yes:
            removed = requests.put(oopsUrl + oops +"/decrement", headers=headers, json=body, verify=False).json()
            print("Oopsies Removed: " + str(removed));
        elif choice.lower() in no:
            print("Skipping item...")
        else:
            print("Invalid choice, skipping item...")
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting: ", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error: ", errt)
    except requests.exceptions.RequestException as err:
        print ("Request Exception: ", err)