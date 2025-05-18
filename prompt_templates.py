# prompt_templates.py

prompt_templates = {
    "collect_city": {
        "objectives": "Collect the [[ property name or area or city ]] for which the customer is calling.",
        "instructions": "Could you please tell me which city you are calling regarding?",
        "prohibited_actions": [
            "Give a list of properties",
            "Fail to clarify if city is not found",
            "Give prices or amenities unprompted"
        ]
    },
    "collect_contact_information": {
        "steps": [
            "Could you please provide your name?",
            "Can you please provide your 10 digit phone number, reciting it clearly without stopping?",
            "So, {name}, your phone number is {phone}, correct?"
        ],
        "validate_tool": "validate_phone_number"
    },
    "master_collect": {
        "prompt": "Could you please provide your {entity_name}?",
        "confirm": "Just confirming, your {entity_name} is '{value}', right?"
    },
    "master_inform": {
        "template": "{what_to_inform}",
        "trigger_tool": "{tool_to_inform}",
        "next_step": "{next_step}"
    }
}