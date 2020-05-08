import os
import re
import datetime
import itertools as it
import pandas as pd
import sys


def main(log_type, misc_other=False):
    """Tool for generating .csv file containing attribute metadata for well logs, skimmed from
    web/public/[log_type]/logs repository on Nickel. Output .csv can be used to update/overwrite web_asset table
    in PG subsurface database. Updated HTML search lists for legacy web portals are generated under subsurface
    internal views. Use this tool to update database assets and search lists in tandem.

    Args:
        log_type (str): web logs repository to catalog ('geothermal' or 'oilgas')
        misc_other (bool): handler for untagged files
                True: files that pass without gaining any 'assetcode' tags will be tagged as other
                False (default): unaffected files will have NULL 'assetcode' tag

    Returns:
        .csv in run path as web_asset_[log_type]_[timestamp].csv
    """

    if log_type == 'geothermal':
        asset_folder = r'\\nickel.unr.edu\Web\public\Geothermal\Logs'  # default asset folder path
        out_file = 'web_asset_geothermal_' + str(datetime.datetime.now().isoformat()[:10]).replace("-",
                                                                                                   "") + '.csv'  # default output filename
    elif log_type == 'oilgas':
        asset_folder = r'\\nickel.unr.edu\Web\public\OilGas\Logs'  # default asset folder path
        out_file = 'web_asset_oilgas_' + str(datetime.datetime.now().isoformat()[:10]).replace("-",
                                                                                               "") + '.csv'  # default output filename
    else:
        print('Invalid log type. Use \'geothermal\' or \'oilgas\'.')
        sys.exit()

    df_table = pd.DataFrame(columns=['apino', 'assetcode', 'filename', 'filetype', 'fileurl', 'papercopylocation',
                                     'toploggedinterval_m', 'bottomloggedinterval_m', 'logrundatetime',
                                     'metadatauri', 'notes'])  # init dataframe

    # dictionary of substrings (values in value list) to be labeled as keys if found in file name; append to as needed
    code_map = {
        'ANI': ['ANI', 'ANISOTROPIC'],
        'BOPE': ['BOPE'],
        'CAL': ['CAL', 'CALIPER', 'BOREHOLE', 'CP', 'BHP', 'SC', 'DMCAL'],
        'CCL': ['CCL', 'CASING', 'COLLAR'],
        'CEM': ['CEM', 'BOND', 'CBL', 'ABCL', 'ACBL', 'CEL'],
        'CFL': ['CFL', 'CAST'],
        'CHLOR': ['CHLOR', 'CHLORIDE', 'CHLORINILOG', 'SALINITY'],
        'CO': ['CO', 'CARBON'],
        'CON': ['CON', 'CONDUCTIVITY'],
        'CORE': ['CORE'],
        'CORR': ['CORR', 'CORRELATION'],
        'DAILY': ['DAILY', 'DR', 'DAL', 'DAILIES', 'DALIES', 'DAILES', 'DAILLIES', 'DALLIESE', 'DAILYS', 'DAILIESE'],
        'DEN': ['DEN', 'DENSITY', 'TDL', 'SDL', 'FDL', 'CD', 'FDC', 'VD', 'BD'],
        'DEPTH': ['DEPTH', 'SD', 'DEP', 'DD', 'PDC'],
        'DIP': ['DIP', 'DIPMETER', 'DP', 'DIPA', 'DM', 'SDM', 'DDM', 'SDDM', 'AP', 'DMML', 'DIPLOG'],
        'DIR': ['DIR', 'DIRECTIONAL', 'DL', 'DIRSUR', 'DEVIATION', 'DVS', 'BHDP'],
        'DRL': ['DRL', 'DRIL', 'DRILL', 'DRILLER', 'DRILLERS', 'DRILLING', 'DRILLRPRT', 'DST'],
        'DS': ['DS', 'SPACING'],
        'DT': ['DT', 'DECAY'],
        'EIS': ['EIS', 'ENVIRONMENTAL', 'EA'],
        'ELEC': ['ELEC', 'ELECTRIC', 'ELECTRICAL', 'DIEL', 'DIELECTRIC', 'IES', 'EM', 'MEL'],
        'EMP': ['EMP', 'ELECTROMAGNETIC'],
        'FLOW': ['FLOW', 'TRACERFLOW', 'TRACERFLOWTEST'],
        'FORM': ['FORM', 'FORMATION', 'FORMATIONS'],
        'FRAC': ['FRAC', 'FRACTURE', 'AFC', 'FIL', 'AFL'],
        'GEOCHEM': ['GEOCHEM', 'GEOCHEMISTRY', 'GEOCHEMICAL'],
        'GEOL': ['GEOL', 'GEOLOGY', 'GEOLOGIC', 'PLATE'],
        'GEOPHYS': ['GEOPHYS', 'GEOPHYSICS', 'GEOPHYSICAL'],
        'GR': ['GR', 'GAMMA', 'GRL', 'GRSL', 'DAGR'],
        'GRS': ['GRS', 'SPECTRAL', 'NGSL', 'SL'],
        'GTR': ['GTR', 'GEOTHERMOMETRY', 'GEOTHERMOMETER'],
        'GW': ['GW', 'GEOWEIGHT'],
        'HCARB': ['HCARB', 'HYDROCARBON'],
        'HEADER': ['HEADER'],
        'HRI': ['HRI'],
        'IMAGE': ['IMAGE'],
        'IND': ['IND', 'INDUCTION', 'DIL', 'DIFL', 'PHASORINDUCTION'],
        'INJ': ['INJ', 'INJECTION'],
        'LASER': ['LASER'],
        'LITH': ['LITH', 'LITHOLOGY', 'LITHOLOGIC', 'QLL'],
        'LL': ['LL', 'LATERAL', 'DLL', 'LATEROLOG'],
        'LLM': ['LLM', 'MICRO', 'MICROLOG'],
        'MAP': ['MAP'],
        'ML': ['ML', 'MINI', 'EMI'],
        'MON': ['MON', 'MONITOR', 'MONITORING'],
        'MRI': ['MRI', 'MAGNETIC', 'RESONANCE'],
        'MS': ['MS', 'MIGRATION', 'MIG'],
        'MUD': ['MUD', 'MUDLOG', 'MUDPGM'],
        'NEU': ['NEU', 'NEUTRON', 'NEUT', 'CNL', 'CNLD', 'NDP'],
        'NUCLEAR': ['NUCLEAR'],
        'OTHER': ['OTHER'],
        'PERMIT': ['PERMIT', 'PERMITS'],
        'PIPE': ['PIPE', 'PERFORATION'],
        'POR': ['POR', 'POROSITY', 'LACA'],
        'PRES': ['PRES', 'PRESSURE', 'PTS', 'PRESS'],
        'PROD': ['PROD', 'PRODUCTION', 'PROL'],
        'QL': ['QL', 'QUICKLOOK'],
        'RES': ['RES', 'RESISTIVITY', 'MRIL'],
        'RL': ['RL', 'RADIOACTIVITY'],
        'RPT': ['RPT', 'RPRT', 'REPORT', 'REPORTS', 'REPRT', 'GEORPT', 'GEORPRT', 'GEOPRTS', 'GEORPTS'],
        'RSV': ['RSV', 'RESERVES', 'GORL'],
        'RTL': ['RTL', 'RADIOACTIVE'],
        'SAMPLE': ['SAMPLE'],
        'SCHEM': ['SCHEM', 'SCHEMATIC'],
        'SEIS': ['SEIS', 'SEISMIC', 'SEISMOGRAM'],
        'SML': ['SML', 'STRATIGRAPHIC'],
        'SONIC': ['SONIC', 'BHCS', 'LSS', 'FWAL', 'FA', 'VDL'],
        'SP': ['SP', 'SPONTANEOUS'],
        'SPIN': ['SPIN', 'SPINNER'],
        'STATIC': ['STATIC'],
        'STREO': ['STREO', 'STEREO', 'STEREOPLOT'],
        'TD': ['TD', 'THERMAL'],
        'TEMP': ['TEMP', 'TEMPERATURE', 'DOWNTEMP', 'TGG'],
        'VEL': ['VEL', 'VELOCITY', 'VSQ'],
        'VERT': ['VERT', 'VERTILOG'],
        'WCR': ['WCR', 'WRC', 'WC', 'COMPLETION', 'WDR'],
        'WPR': ['WPR', 'PLUGGING']
    }

    def remove_prefix(text, prefix):
        return text[text.startswith(prefix) and len(prefix):]

    def label(string, key, vals):  # returns key if any substring from vals (substring list) is in string
        if any(substring in string for substring in vals):
            for v in vals:
                if (
                        not string[string.find(v) - 1].isalpha()
                        and not string[string.find(v) + len(v)].isalpha()
                ):  # if substring is surrounded by nonalphas
                    return key

    def camel_case_sep(string, sep):  # separates CamelCase -> Camel(sep)Case for further string processing
        str_list = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', string)).split()
        return sep.join(str_list)

    def get_codes(string):  # returns asset codes in reduced, alphabetized, hyphenated string (eg: 'PRES-SPIN-TEMP')
        string = camel_case_sep(string, '_')
        string = string.upper()
        string = '_' + string + '_'  # prefix and suffix string for further processing
        out_set = set()  # init empty set for appending values
        for key in code_map:  # iter through code_map
            out_set.add(label(string, key, code_map[key]))  # adds return of label function to out_set
        out_list = list(out_set)
        out_list.remove(None)
        out_list.sort()
        out_string = '-'.join(i for i in out_list)
        if misc_other:
            return out_string if out_set != set() else 'OTHER'  # return out_sting if not empty, 'OTHER' if empty
        else:
            return out_string if out_set != set() else None  # return out_sting if not empty, None if empty

    api_mask = re.compile("[0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9]")
    api_child_mask = re.compile("[0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9]-[A-Z0-9]")

    for root, dirs, files in os.walk(asset_folder):
        for name in files:
            file_path = os.path.join(root, name)
            sub_path = remove_prefix(file_path, asset_folder + os.path.sep)  # level 2 onward of full path
            api = re.match(api_mask,
                           sub_path)  # check if level 2 of asset file path is an api directory (if not, contents will be skipped)
            api_child = re.match(api_child_mask,
                                 sub_path[13:])  # check if level 3 of asset file path is a child api directory

            if api and name != 'Thumbs.db':
                apino = api.group(0)  # current api number from directory
                if api_child and len(sub_path) >= 27 and sub_path[27] == os.path.sep:
                    apino = api_child.group(0)  # assign child api if child well
                filename, filetype = os.path.splitext(name)
                fileurl = (file_path.replace(r'\\nickel.unr.edu\Web', r'http://data.nbmg.unr.edu')).replace(os.path.sep,
                                                                                                            '/')
                papercopylocation = 'GBSSRL' if filetype in ['.pdf', '.tif'] else None
                assetcode = get_codes(sub_path)

                df_table = df_table.append({
                    'apino': apino, 'assetcode': assetcode, 'filename': filename, 'filetype': filetype,
                    'fileurl': fileurl, 'papercopylocation': papercopylocation
                }, ignore_index=True)
                # append row to df

                # if assetcode == '':
                #     print('No asset codes recognized in filename: %s' %filename)  # test: print unlabeled files

    df_table.to_csv(out_file)


if __name__ == '__main__':
    main(input('Specify log repository: \'geothermal\' or \'oilgas\''))
