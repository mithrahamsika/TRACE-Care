
# TRACE-Care Recommendation Engine
# Transparent barrier-to-action rules


def recommend_action(barrier):

    recommendations = {

        "Transport Difficulty": {
            "action": "Navigator-assisted transport support",
            "reason": "The patient may be unable to attend follow-up due to transport access difficulties."
        },

        "Financial Difficulty": {
            "action": "Refer to financial assistance support",
            "reason": "Financial constraints may prevent the patient from completing follow-up care."
        },

        "Language Barrier": {
            "action": "Arrange language assistance or an interpreter",
            "reason": "Language support can help the patient understand follow-up instructions."
        },

        "Appointment Unavailable": {
            "action": "Find an alternative appointment or provider",
            "reason": "The patient needs an accessible appointment to continue the care pathway."
        },

        "Unable to Contact Patient": {
            "action": "Verify contact details and try an approved alternative channel",
            "reason": "The patient could not be reached through the existing contact method."
        },

        "Unclear Instructions": {
            "action": "Arrange staff-assisted clarification",
            "reason": "The patient may need clearer information about the next follow-up step."
        },

        "Fear or Anxiety": {
            "action": "Arrange a supportive patient navigator conversation",
            "reason": "A supportive conversation may help address concerns about attending follow-up care."
        },

        "Other / Unknown": {
            "action": "Refer for manual staff review",
            "reason": "More information is needed before selecting an appropriate intervention."
        }
    }

    return recommendations.get(
        barrier,
        {
            "action": "Manual staff review required",
            "reason": "No matching barrier rule was found."
        }
    )
