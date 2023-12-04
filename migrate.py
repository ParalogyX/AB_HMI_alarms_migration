import pandas as pd
import xmltodict


def add_type(row):

    match row['trigger-value']:
        case '1': return 'HighHigh'
        case '2': return 'High'
        case '3': return 'Low'
        case '4': return 'LowLow'
        case '5': return 'Sensor Defect'
        case '6': return 'High Switch Alarm'
        case other: return 'EXCEPTION'

def add_trip(row):
    match row['trigger-value']:
        case '1': return 'TRIP'
        case '2': return 'HI'
        case '3': return 'LO'
        case '4': return 'TRIP'
        case '5': return 'TRIP'
        case other: return 'TRIP'

def new_exp(row):
    s = row['exp']
    tr = str(int(row['trigger-value'])-1)
    s = s[s.find(']')+1:-1] + '_' + tr
    return s





def orig_alarms_xls():

    with open("Original Voyageur Alarms.xml", 'rt') as f:
        xml_orig = f.read()


    my_dict = xmltodict.parse(xml_orig)
    trg_list_orig = my_dict['alarms']['alarm']['triggers']['trigger']
    msg_list_orig = my_dict['alarms']['alarm']['messages']['message']

    df_trg = pd.DataFrame(trg_list_orig)
    col_list = df_trg.columns.to_list()

    new_col_list = [s.replace('@', '') for s in col_list]
    df_trg.columns = new_col_list


    df_msg = pd.DataFrame(msg_list_orig)
    col_list = df_msg.columns.to_list()
    new_col_list = [s.replace('@', '') for s in col_list]
    df_msg.columns = new_col_list


    df_msg.trigger = df_msg.trigger.str.replace('#', '')

    df = pd.merge(df_trg, df_msg, left_on='id', right_on='trigger')

    df['type'] = df.apply(add_type, axis=1)
    df['cond'] = df.apply(add_trip, axis=1)

    df = df.drop(['ack-all-value', 'use-ack-all', 'ack-tag', 'message-tag', 'message-handshake-exp', 'message-notification-tag', 'identifier', 
                  'audio', 'display', 'print', 'message-to-tag', 'remote-ack-exp', 'remote-ack-handshake-tag', 'handshake-tag'], axis=1)
    
    df['new_exp'] = df.apply(new_exp, axis=1)

    return df

    #df.to_excel('combined_original.xlsx')

def new_alarms_xls():
    with open("Voyageur_Unit1_Alarmsexportfile2.xml", 'rt') as f:
        xml_orig = f.read()

    my_dict = xmltodict.parse(xml_orig)
    alm_list_new = my_dict['AlarmCollection']['Alarm']

    df_alm_new = pd.DataFrame(alm_list_new)
    col_list = df_alm_new.columns.to_list()
    new_col_list = [s.replace('@', '') for s in col_list]
    df_alm_new.columns = new_col_list

    cols_to_drop = ['Expression', 'Limit', 'TargetTag', 'OnDelay', 'OffDelay', 'Deadband', 'Severity', 'AssocTag1', 'AssocTag2', 'AssocTag3', 'AssocTag4', 
                    'ShelveDuration', 'MaxShelveDuration', 'EvaluationPeriod', 'Latched', 'AckRequired', 'AlarmSetRollupIncluded', 'AlarmSetOperIncluded', 
                    'Lang', 'AlarmDefinition', 'AlarmClass', 'HMIGroup', 'HMICmd']
    
    #df_alm_new = df_alm_new.drop(cols_to_drop, axis=1)
    df_alm_new.to_excel('new_alarms.xlsx')


def get_alarm_from_dict(row):
    #print(row.Name)
    s = f'\t<Alarm Name="{row.Name}" ConditionType="{row.ConditionType}" Input="{row.Input}" Expression="= 1" Limit="0" TargetTag="" OnDelay="0" OffDelay="0" Deadband="0" Severity="500" AssocTag1="" AssocTag2="" AssocTag3="" AssocTag4="" ShelveDuration="0" MaxShelveDuration="0" EvaluationPeriod="500" Latched="False" AckRequired="True" AlarmSetRollupIncluded="True" AlarmSetOperIncluded="True" Lang="" Use="True" AlarmDefinition="">\n'
    s += f'\t\t<Message><![CDATA[{row.Message}]]></Message>\n\t\t<AlarmClass><![CDATA[]]></AlarmClass>\n\t\t<HMIGroup><![CDATA[]]></HMIGroup>\n\t\t<HMICmd><![CDATA[]]></HMICmd>\n\t</Alarm>\n'
    return s




def new_alarms_from_old(df):

    name = ['Turbine'] * len(df)
    condition_type = df.cond
    input_f = df.new_exp
    expression = ['=1'] * len(df)
    limit = [0] * len(df)
    target_tag = [''] * len(df)
    on_delay = [0] * len(df)
    off_delay = [0] * len(df)
    deadband = [0] * len(df)
    severity = [500] * len(df)
    AssocTag1 = [''] * len(df)
    AssocTag2 = [''] * len(df)
    AssocTag3 = [''] * len(df)
    AssocTag4 = [''] * len(df)
    ShelveDuration = [0] * len(df)
    MaxShelveDuration =	[0] * len(df)
    EvaluationPeriod = [500] * len(df)
    Latched	= [False] * len(df)
    AckRequired = [True]  * len(df)
    AlarmSetRollupIncluded = [True]  * len(df)
    AlarmSetOperIncluded = [True]  * len(df)
    Lang = [''] * len(df)
    Use	= [True]  * len(df)
    AlarmDefinition = [''] * len(df)
    Message = df.text
    AlarmClass = [None] * len(df)
    HMIGroup = [None] * len(df)
    HMICmd = [None] * len(df)

    new_alarms_full = pd.DataFrame({'Name': name, 'ConditionType': condition_type, 'Input': input_f, 'Expression': expression, 'Limit': limit, 'TargetTag': target_tag,
                                'OnDelay': on_delay, 'OffDelay': off_delay, 'Deadband': deadband, 'Severity': severity, 'AssocTag1': AssocTag1, 'AssocTag2': AssocTag2, 
                                'AssocTag3': AssocTag3, 'AssocTag4': AssocTag4, 'ShelveDuration': ShelveDuration, 'MaxShelveDuration': MaxShelveDuration,
                                'EvaluationPeriod': EvaluationPeriod, 'Latched': Latched, 'AckRequired': AckRequired, 'AlarmSetRollupIncluded': AlarmSetRollupIncluded,
                                'AlarmSetOperIncluded': AlarmSetOperIncluded, 'Lang': Lang, 'Use': Use, 'AlarmDefinition': AlarmDefinition, 'Message': Message,
                                'AlarmClass': AlarmClass, 'HMIGroup': HMIGroup, 'HMICmd': HMICmd})
    
    
   
    # Make xml as text

    s = '<?xml version="1.0" encoding="utf-8"?>\n'
    s += '<AlarmCollection xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n'
    
    s1 = list(new_alarms_full.apply(get_alarm_from_dict, axis=1))
    s1.insert(0, s)
    s1.append('</AlarmCollection>')
    
    with open('new_alarms_generated.xml', 'wt') as f:
        f.writelines( s1)
    
    return new_alarms_full

    # new_alarms_full.to_excel('new_alarms_full.xlsx')


def main():
    df = orig_alarms_xls()
    #df_new = new_alarms_from_old(df)

    new_alarms_from_old(df)

    #new_alarms_xls()


if __name__=='__main__':
    main()