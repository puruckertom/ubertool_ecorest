TAG_DESCRIPTION = "Terrplant Model"

SHORT_DESCRIPTION = "TerrPLANT provides screening level estimates of exposure to terrestrial plants " \
                    "from single pesticide applications through runoff or drift. Monocots and dicots " \
                    "found in dry or semi-aquatic habitats can be evaluated using this model. Exposure " \
                    "estimates can be generated for both listed and non-listed species using TerrPLANT."

CONSUMES = ["application/json"]

PRODUCES = ["application/json"]

PARAMETERS = [
    {
        "description": "Run TerrPlant model",
        "required": True,
    }
]

RESPONSES = {
    "200": {
        "description": "Successful Operation",
    }
}
