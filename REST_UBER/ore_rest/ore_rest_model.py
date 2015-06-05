from collections import OrderedDict
import json
import OreCalculator

def ore(inputs, query_result_list):

    ore_class_list = []
    class_inputs = exp_duration_handler(inputs)

    for query in query_result_list:
        # print query.keys()  #  SQLite query (row_factory.Row)

        # NonCancerInputs
        activity = query['Activity']
        formulation = query['Formulation']
        app_equip = query['AppEquip']
        app_type = query['AppType']
        crop_target = query['Category']
        app_rate = inputs['app_rate']['app_rate_' + query['Formulation']]
        app_rate_unit = query['AppRateUnit']
        area_treated = query['TreatedVal']
        area_treated_unit = query['TreatedUnit']

        # DermalNonCancer specific inputs
        abs_frac_dermal = class_inputs['dermal']['abs_frac']
        bw_dermal = class_inputs['dermal']['bw_adult']
        pod_dermal = class_inputs['dermal']['nc_POD']
        loc_dermal = class_inputs['dermal']['nc_LOC']
        # Dermal PPE (personal protection equipment)
        dermal_unit_exp_sl_no_G = query['DUESLNoG']
        dermal_unit_exp_sl_G = query['DUESLG']
        dermal_unit_exp_dl_g = query['DUEDLG']
        dermal_unit_exp_sl_G_crh = query['DUESLGCRH']
        dermal_unit_exp_dl_G_crh = query['DUEDLGCRH']
        dermal_unit_exp_ec = query['DUEEC']

        # InhalNonCancer specific inputs
        abs_frac_inhal = class_inputs['inhal']['abs_frac']
        bw_inhal = class_inputs['inhal']['bw_adult']
        pod_inhal = class_inputs['inhal']['nc_POD']
        loc_inhal = class_inputs['inhal']['nc_LOC']
        #Inhalation PPE (personal protection equipment)
        inhal_unit_exp_no_r = query['IUENoR']
        inhal_unit_exp_pf5r = query['IUEPF5R']
        inhal_unit_exp_pf10r = query['IUEPF10R']
        inhal_unit_exp_ec = query['IUEEC']

        # Create DermalNonCancer class instance
        dermal = OreCalculator.DermalNonCancer(
                activity, crop_target, app_rate, app_rate_unit,
                loc_dermal, loc_inhal, area_treated, area_treated_unit,
                formulation, app_equip, app_type,
                abs_frac_dermal, bw_dermal, pod_dermal,
                dermal_unit_exp_sl_no_G, dermal_unit_exp_sl_G, dermal_unit_exp_dl_g,
                dermal_unit_exp_sl_G_crh, dermal_unit_exp_dl_G_crh, dermal_unit_exp_ec
        )

        # Create InhalNonCancer class instance
        inhal = OreCalculator.InhalNonCancer(
                activity, crop_target, app_rate, app_rate_unit,
                loc_dermal, loc_inhal, area_treated, area_treated_unit,
                formulation, app_equip, app_type,
                abs_frac_inhal, bw_inhal, pod_inhal,
                inhal_unit_exp_no_r, inhal_unit_exp_pf5r, inhal_unit_exp_pf10r, inhal_unit_exp_ec
        )

        # Combined results?
        if True in [inputs['expComboType_2'], inputs['expComboType_3'], inputs['expComboType_4']]:
            if inputs['expComboType_2']:  # Combined: Additive Dose
                # combined = OreCalculator.combined_dose(dermal, inhal)
                pass
            if inputs['expComboType_3']:  # Combined: 1/MOE Approach
                # combined = OreCalculator.combined_moe(dermal, inhal)
                pass
            if inputs['expComboType_4']:  # Aggregate Risk Index
                # combined = OreCalculator.ari(dermal, inhal)
                pass


        ore_class_list.append( (dermal, inhal) )


    ore_output = OreOutputFormatter(ore_class_list)
    output_dict = ore_output.get_output_dict()
    # print output_dict

    return output_dict


def exp_duration_handler(inputs):
    """
    Helper method to handle the Short, Intermediate, and Long term options

    ONLY SHORT TERM IS CURRENTLY ALLOWED ON THE FRONTEND

    :param inputs: dict
    :return: float
    """

    class_inputs = { 'dermal': {}, 'inhal': {} }
    type = '_st'
    if inputs['expDurationType_st']:
        print "Short term"
        type = '_st'
    if inputs['expDurationType_it']:
        print "Intermediate term"
        type = '_it'
    if inputs['expDurationType_lt']:
        print "Long term"
        type = '_lt'


    class_inputs['dermal']['abs_frac'] = float(inputs['dermal_abs_frac' + type]) / 100.
    class_inputs['dermal']['bw_adult'] = inputs['bw_dermal_NC' + type]
    class_inputs['dermal']['nc_POD'] = inputs['dermal_NC_POD' + type]
    class_inputs['dermal']['nc_LOC'] = inputs['dermal_NC_LOC' + type]

    class_inputs['inhal']['abs_frac'] = float(inputs['inhalation_abs_frac' + type]) / 100.
    class_inputs['inhal']['bw_adult'] = inputs['bw_inhalation_NC' + type]
    class_inputs['inhal']['nc_POD'] = inputs['inhalation_NC_POD' + type]
    class_inputs['inhal']['nc_LOC'] = inputs['inhalation_NC_LOC' + type]

    return class_inputs



class OreOutputFormatter(object):
    def __init__(self, ore_class_list):
        """
        [
        (<ore_rest.OreCalculator.DermalNonCancer object at 0x000000000A6E0DD8>, <ore_rest.OreCalculator.InhalNonCancer object at 0x000000000A6E0FD0>),
        (<ore_rest.OreCalculator.DermalNonCancer object at 0x000000000A697128>, <ore_rest.OreCalculator.InhalNonCancer object at 0x000000000A697160>),
        (<ore_rest.OreCalculator.DermalNonCancer object at 0x000000000A6971D0>, <ore_rest.OreCalculator.InhalNonCancer object at 0x000000000A697278>)
        ]
        """
        self.dermal_class_list = []
        self.inhal_class_list = []

        for item in ore_class_list:
            self.dermal_class_list.append(item[0])
            self.inhal_class_list.append(item[1])

        self.output_dict = {}
        self.dermal_formatter()
        self.inhal_formatter()

    """
        'mix_loader': {
            'activity': "M/L",
            'app_equip': 'Aerial',
            'crop_target': "Corn[field crop, high acreage]",
            'loc': {'dermal': '100', 'inhal': '100'},
            'app_rate': '2',
            'app_rate_unit': 'lb ai/A',
            'area_treated': '1200',
            'area_treated_unit': 'acre',
            'dermal_unit_exp': ['220 [SL/No G]', '37.6 [SL/G]'],
            'inhal_unit_exp': ['0.219 [No-R]', '0.219 [No-R]'],
            'dermal_dose': ['1.65', '0.282'],
            'dermal_moe': ['30', '180'],
            'inhal_dose': ['0.00658', '0.00658'],
            'inhal_moe': ['3800', '3800']
        },
        'applicator': {
            'activity': "Aerial",
            'app_equip': 'Aerial',
            'crop_target': "Corn[field crop, high acreage]",
            'loc': {'dermal': '100', 'inhal': '100'},
            'app_rate': '2',
            'app_rate_unit': 'lb ai/A',
            'area_treated': '1200',
            'area_treated_unit': 'acre',
            'dermal_unit_exp': ['2.06 [EC]'],
            'inhal_unit_exp': ['0.043 [EC]'],
            'dermal_dose': ['0.0156'],
            'dermal_moe': ['3200'],
            'inhal_dose': ['0.000148'],
            'inhal_moe': ['170000']
        },
        'flagger': {
            'activity': "Flagger",
            'app_equip': 'Aerial',
            'crop_target': "Corn[field crop, high acreage]",
            'loc': {'dermal': '100', 'inhal': '100'},
            'app_rate': '2',
            'app_rate_unit': 'lb ai/A',
            'area_treated': '350',
            'area_treated_unit': 'acre',
            'dermal_unit_exp': ['11 [EC]'],
            'inhal_unit_exp': ['0.35 [No-R]'],
            'dermal_dose': ['0.0156'],
            'dermal_moe': ['3200'],
            'inhal_dose': ['0.000148'],
            'inhal_moe': ['170000']
        }
    """

    def get_output_dict(self):
        if len(self.output_dict) > 0:
            return self.output_dict
        else:
            self.dermal_formatter()
            self.inhal_formatter()

    def dermal_formatter(self):
        """
        Create shared inputs portion of output_dict for a row of results on Output page
        """
        # Loop over the DermalNonCancer instances
        for exp_scenario in self.dermal_class_list:  # Could be either class instances list, these are the shared inputs

            attr_dict = exp_scenario.ordered_dict()
            # print attr_dict.items()

            dermal_dict = {}

            dermal_unit_exp = []
            dermal_dose = []
            dermal_moe = []
            for k, v in attr_dict.items():

                if isinstance(attr_dict[k], OreCalculator.OreCalculator):
                    # Attributes have been ordered by PPE to match the logic of the calculator
                    # print k, attr_dict[k], attr_dict[k].moe
                    dermal_unit_exp.append(str(attr_dict[k].unit_exp) + " [" + k.upper() + "]")
                    dermal_dose.append(str(attr_dict[k].dose_conc))
                    dermal_moe.append(str(attr_dict[k].moe))
                elif attr_dict[k] != None and attr_dict[k] != "No Data":
                    # print k, attr_dict[k]
                    dermal_dict[k] = attr_dict[k]

            dermal_dict['dermal_unit_exp'] = dermal_unit_exp
            dermal_dict['dermal_dose'] = dermal_dose
            dermal_dict['dermal_moe'] = dermal_moe

            self.output_dict[exp_scenario.activity] = dermal_dict

    def inhal_formatter(self):

        # Loop over the InhalNonCancer instances
        for exp_scenario in self.inhal_class_list:

            attr_dict = exp_scenario.ordered_dict()
            # print attr_dict.items()

            inhal_dict = {}

            inhal_unit_exp = []
            inhal_dose = []
            inhal_moe = []
            for k, v in attr_dict.items():
                if isinstance(attr_dict[k], OreCalculator.OreCalculator):
                    # Attributes have been ordered by PPE to match the logic of the calculator
                    # print k, attr_dict[k], attr_dict[k].moe
                    inhal_unit_exp.append(str(attr_dict[k].unit_exp) + " [" + k.upper() + "]")
                    inhal_dose.append(str(attr_dict[k].dose_conc))
                    inhal_moe.append(str(attr_dict[k].moe))

            inhal_dict['inhal_unit_exp'] = inhal_unit_exp
            inhal_dict['inhal_dose'] = inhal_dose
            inhal_dict['inhal_moe'] = inhal_moe

            self.output_dict[exp_scenario.activity].update(inhal_dict)

        # print self.output_dict


# class OreOutputDjango(object):
#     def __init__(self, exp_scenario, output_list):
#         self.exp_scenario = exp_scenario
#         self.output_list = output_list
#
#     def to_JSON(self):
#         return json.dumps(self, default=lambda o: o.__dict__,
#             sort_keys=True, indent=4)