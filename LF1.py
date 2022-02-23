import json
import boto3  

# validate location
def is_valid_location(location):
    if location == None:
        return False
    elif location.lower() != "manhattan":
        return False
    else:
        return True


# validate cuisine
def is_valid_cuisine(cuisine):
    valid_cuisine = ["chinese", "korean", "thai", "japanese", "french", "mediterranean", "mexican", "italian", "greek", "american"]
    if cuisine == None:
        return False
    elif cuisine.lower() not in valid_cuisine:
        return False
    else:
        return True


# validate number_of_people
def is_valid_number_of_people(number_of_people):
    if number_of_people == None:
        return False
    else:
        return True


# validate dining_date
def is_valid_dining_date(dining_date):
    if dining_date == None:
        return False
    else:
        return True


# validate dining_time
def is_valid_dining_time(dining_time):
    if dining_time == None:
        return False
    else:
        return True


# validate phone_number
def is_valid_phone_number(phone_number):
    if phone_number == None:
        return False
    else:
        return True 


####################################################################################################################################################
# GENERATE RESPONSE TO LEX

# expect the user to provide a slot value
def elicit_slot(intent_name, slots_list, elicit_slot):
    return {
        "dialogAction" : {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots_list,
            "slotToElicit": elicit_slot,
        }
    }

####################################################################################################################################################

def lambda_handler(event, context):
    # TODO implement
    sqs = boto3.resource('sqs')
    queue = sqs.Queue('https://sqs.us-east-1.amazonaws.com/686660213986/DiningConcierge')
    
    slots = event["currentIntent"]["slots"]

    if is_valid_location(slots["Location"]) == False:
        slots["Location"] = None
        res = elicit_slot("DiningSuggestionsIntent", slots, "Location")
        return res
    
    if is_valid_cuisine(slots["Cuisine"]) == False:
        slots["Cuisine"] = None
        res = elicit_slot("DiningSuggestionsIntent", slots, "Cuisine")
        return res
    
    if is_valid_number_of_people(slots["NumberOfPeople"]) == False:
        slots["NumberOfPeople"] = None
        res = elicit_slot("DiningSuggestionsIntent", slots, "NumberOfPeople")
        return res
    
    if is_valid_dining_date(slots["DiningDate"]) == False:
        slots["DiningDate"] = None
        res = elicit_slot("DiningSuggestionsIntent", slots, "DiningDate")
        return res
    
    if is_valid_dining_time(slots["DiningTime"]) == False:
        slots["DiningTime"] = None
        res = elicit_slot("DiningSuggestionsIntent", slots, "DiningTime")
        return res
    
    if is_valid_phone_number(slots["PhoneNumber"]) == False:
        slots["PhoneNumber"] = None
        res = elicit_slot("DiningSuggestionsIntent", slots, "PhoneNumber")
        return res
    
    response = queue.send_message(MessageBody=json.dumps(slots))
    print(response)
    
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "PlainText",
              "content": "You’re all set. Expect my suggestions shortly! Have a good day."
            }
        }
    }
