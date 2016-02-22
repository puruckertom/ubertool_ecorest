TAG_DESCRIPTION = "Rice Model"

SHORT_DESCRIPTION = 'The Tier I Rice Model (Version 1.0) is designed to estimate surface water exposure from the use ' \
                    'of pesticide in rice paddies. It is a screening level model that is based on the Interim Rice ' \
                    'Model, which has been used by the Environmental Fate and Effects Division for multiple years. ' \
                    'The model calculates a single, screening-level concentration that represents both short and ' \
                    'long term surface water exposures. The screening-level concentraion can be used for both ' \
                    'aquatic ecological risk assessments and drinking water exposure assessments for human health ' \
                    'risk assessment.'

CONSUMES = ["application/json"]

PRODUCES = ["application/json"]

PARAMETERS = [
    {
        "description": "Run Rice model",
        "required": True,
    }
]

RESPONSES = {
    "200": {
        "description": "Successful Operation",
    }
}