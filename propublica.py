import requests, json
endpoint = ""
data = {"ip":"1.1.2.3"}
headers = {"X-API-Key":"qom0aa5YNf4MYMfnleCIr6jCZMRcjAVW888qEM6b"}

'''===================================================================================='''
# GET RECENT BILLS

# GET REQUEST: https://api.propublica.org/congress/v1/{congress}/{chamber}/bills/{type}.json

# URL PARAMETERS 
# --------------
# congress | 105-115
# chamber | house, senate or both (for passed only)
# type | introduced, updated, passed or major
'''===================================================================================='''
#recentBills("https://api.propublica.org/congress/v1/115/house/bills/introduced.json")
def recentBills(congress, chamber, type):
	url = "https://api.propublica.org/congress/v1/"
	url += str(congress)
	url += "/"
	url += str(chamber)
	url += "/bills/"
	url += str(type)
	d = requests.get(url, headers=headers).json()

	LIST = [ bill['number'] for bill in d['results'][0]['bills'] ]
        return LIST

'''===================================================================================='''
# GET RECENT BILLS BY A SPECIFIC MEMBER

# GET REQUEST: https://api.propublica.org/congress/v1/members/{member-id}/bills/{type}.json

# URL PARAMETERS 
# --------------
# member-id | The ID of the member to retrieve; it is assigned by the Biographical Directory of the United States Congress or can be retrieved from a member list request.
# type | introduced or updated
'''===================================================================================='''
#specificMembersRecentBills("https://api.propublica.org/congress/v1/members/L000287/bills/introduced.json")
def specificMembersRecentBills(member_id, type):
        url = "https://api.propublica.org/congress/v1/members/%s/bills/%s"%(member_id, type)
        d = requests.get( url, headers=headers).json()

        LIST = [ bill['number'] for bill in d['results'][0]['bills']]
        return LIST

'''===================================================================================='''
# GET A SPECIFIC BILL

# GET REQUEST: https://api.propublica.org/congress/v1/{congress}/bills/{bill-id}.json

# URL PARAMETERS 
# --------------
# congress | 105-115
# bill-id | ex: hr4881
'''===================================================================================='''
def specificBills(congress,billID):
	url = "https://api.propublica.org/congress/v1/"
	url += str(congress)
	url += "/bills/"
	url += str(billID)
	d = requests.get(url, headers=headers).json()
	
	DICT = {}
	DICT['title'] = d['results'][0]['title']
	DICT['bill_id'] = d['results'][0]['bill_id']
	DICT['bill'] = d['results'][0]['bill']
	DICT['bill_uri'] = d['results'][0]['bill_uri']
	DICT['bill_type'] = d['results'][0]['bill_type']
	DICT['number'] = d['results'][0]['number']
	DICT['sponsor'] = d['results'][0]['sponsor']
	DICT['sponsor_uri'] = d['results'][0]['sponsor_uri']
	DICT['sponsor_party'] = d['results'][0]['sponsor_party']
	DICT['sponsor_state'] = d['results'][0]['sponsor_state']
	DICT['gpo_pdf_uri'] = d['results'][0]['gpo_pdf_uri']
	DICT['congressdotgov_url'] = d['results'][0]['congressdotgov_url']
	DICT['govtrack_url'] = d['results'][0]['govtrack_url']
	DICT['introduced_date'] = d['results'][0]['introduced_date']
	DICT['active'] = d['results'][0]['active']
	DICT['house_passage'] = d['results'][0]['house_passage']
	DICT['senate_passage'] = d['results'][0]['senate_passage']
	DICT['cosponsors'] = d['results'][0]['cosponsors']
	DICT['primary_subject'] = d['results'][0]['primary_subject'] #IMPORTANT
	DICT['committees'] = d['results'][0]['committees']
	DICT['latest_major_action_date'] = d['results'][0]['latest_major_action_date']
	DICT['latest_major_action'] = d['results'][0]['latest_major_action']
	DICT['last_vote_date'] = d['results'][0]['last_vote_date']
	DICT['house_passage_vote'] = d['results'][0]['house_passage_vote']
	DICT['senate_passage_vote'] = d['results'][0]['senate_passage_vote']
	DICT['summary_short'] = d['results'][0]['summary_short']

	DICT['actions_latest_datetime'] = d['results'][0]['actions'][0][datetime]
	DICT['actions_latest_description'] = d['results'][0]['actions'][0][description]

	DICT['chamber'] = d['votes'][0]['chamber']
	DICT['date'] = d['votes'][0]['date']
	DICT['time'] = d['votes'][0]['time']
	DICT['roll_call'] = d['votes'][0]['roll_call']
	DICT['question'] = d['votes'][0]['question']
	DICT['total_yes'] = d['votes'][0]['total_yes']
	DICT['total_no'] = d['votes'][0]['total_no']
	DICT['api_url'] = d['votes'][0]['api_url']
	return DICT


'''===================================================================================='''
# GET A SUBJECTS, AMENDMENTS AND RELATED BILLS FOR A SPECIFIC BILL

# GET REQUEST: https://api.propublica.org/congress/v1/{congress}/bills/{bill-id}/{type}.json

# URL PARAMETERS 
# --------------
# congress | 105-115
# bill-id | ex: hr4881
# type | subjects, amendments or related
'''===================================================================================='''
#subjectsForBills("https://api.propublica.org/congress/v1/114/bills/hr2393/subjects.json") 
def relatedForBills(congress, billID):
        url = "https://api.propublica.org/congress/v1/%s/bills/%s/related"%(congress, billID)
        d = requests.get(url, headers=headers).json()
        LIST = [ bill['bill'] for bill in d['results'][0]['related_bills']] 
        return LIST




#subjects = [ item['content'] for item in requests.get("https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D'https%3A%2F%2Fwww.congress.gov%2Fbrowse%2Flegislative-subject-terms%2F115th-congress'%20and%20xpath%3D'%2F%2Ful%5Bcontains(%40class%2C%22plain%20margin7%22)%5D%2F%2Fli%5Bcontains(%40href%2C%22%22)%5D%2F*'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys").json()['query']['results']['a'] ]

#for subject in subjects:
#        print subject

'''
def subjectsForBills(endpoint):
	d = requests.get(endpoint, headers=headers).json()
	with open('subjectsForBills.txt', 'w') as outfile:
		json.dump(d, outfile)
'''
