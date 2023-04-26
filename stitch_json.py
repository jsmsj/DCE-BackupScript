import os,json,config

files_save_location = config.location_for_exported_files_to_be_saved
import re

new_files_pattern = re.compile(r'\[(\d+)\] \(after \d{4}-\d{2}-\d{2}\)')

output_file_pattern = re.compile(r'\[(\d+)\].json')

def get_output_file_from_id(files_save_location,id:str):
    id = str(id)
    files = os.listdir(files_save_location)
    for f in files:
        matches = output_file_pattern.findall(f)
        if len(matches) == 0:
            continue
        if id == matches[0]:
            return f
    
    return Exception(f'Error: {files_save_location} | {id}')


def stitch_items(files_save_location,**kwargs):
    files = os.listdir(files_save_location)
    files_to_stitch = []
    for _file in files:
        matches = new_files_pattern.findall(_file)
        if len(matches) == 0:
            continue
        o_p_file = get_output_file_from_id(files_save_location,matches[0])
        files_to_stitch.append((_file,o_p_file))
    if kwargs.get('channels'):
        print(f'To stitch = {len(files_to_stitch)}')
    
    for input_file,output_file in files_to_stitch:
        print(f'stitching {input_file} with {output_file}')
        print()
        with open(f'{files_save_location}\\{input_file}') as inp:
            inp_data = json.load(inp)
            messages = inp_data['messages']
            message_count = inp_data['messageCount']
            del inp_data
        
        with open(f'{files_save_location}\\{output_file}') as out:
            out_data = json.load(out)
            already_msg_count = out_data['messageCount']

        out_data['messages'].extend(messages)
        del messages
        out_data['messageCount'] = message_count+already_msg_count

        with open(f'{files_save_location}\\{output_file}','w') as out_final:
            json.dump(out_data,out_final, indent=4)
        
        del out_data
        os.remove(f'{files_save_location}\\{input_file}')
        # print(f'{files_save_location}\\{input_file}')

chanids = os.listdir(files_save_location+'\\Threads')

for i in chanids:
    stitch_items(files_save_location+'\\Threads' + f'\\{i}')


stitch_items(files_save_location,channels = 1)

print('done stitching all')