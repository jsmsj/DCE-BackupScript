import requests,os,json,time,config


guild_id = config.server_id

files_save_location = config.location_for_exported_files_to_be_saved
dll_file_location = config.location_of_folder_containing_dce_dl_file

url_active = f"https://discord.com/api/v10/guilds/{guild_id}/threads/active"

bot_token = config.bot_token


minimum_thread_messages = config.minimum_number_of_messages_for_a_thread_to_be_exported

headers = {
  'Authorization': f'Bot {bot_token}',
}

ignore_channels_id = config.ignore_channel_ids

allowed_channel_types = [0,2,5,10,13]


try:
    os.mkdir(files_save_location+'\\Threads')
except FileExistsError:
    pass

def get_threads(url):
    
    response = requests.request("GET", url, headers=headers)
    
    if response.status_code !=200:
        response = response.json()
        if response['code'] == 50024:
            return []
        elif response['code'] == 50001: # missing access
            return []
        else:
            print(url)
            print(response)
            print(response.json())
            print(response.text)
    response = response.json()
    return [(thread['id'],thread.get('last_message_id'),thread.get('parent_id')) for thread in response['threads'] if thread['message_count']>=minimum_thread_messages]


def get_thread_ids_all(channel_ids):
    thread_ids = []
    thread_ids.extend(get_threads(url_active))

    for channel_id,_ in channel_ids:
        url_ch_archived_pub = f"https://discord.com/api/v10/channels/{channel_id}/threads/archived/public"
        url_ch_archived_priv = f"https://discord.com/api/v10/channels/{channel_id}/threads/archived/private"

        thread_ids.extend(get_threads(url_ch_archived_pub))
        thread_ids.extend(get_threads(url_ch_archived_priv))

    return thread_ids

def get_all_channes():
    url = f'https://discord.com/api/v10/guilds/{guild_id}/channels'

    response = requests.request("GET", url, headers=headers).json()

    return [(channel['id'],channel.get('last_message_id')) for channel in response if channel.get('type') in allowed_channel_types and str(channel.get('id')) not in ignore_channels_id]


def get_channel_lastmsg_tuple(): 
    pairs = set()
    channel_ids = get_all_channes()
    files_at_location = os.listdir(files_save_location)
    for channel_id,recent_last_msg_id in channel_ids:
        # if recent_last_msg_id is None:
        #     continue
        added = False
        for _file in files_at_location:
            if channel_id in _file and 'after' not in _file:
                with open(f'{files_save_location}\\{_file}','r') as f:
                    data = json.load(f)
                    last_msg_id = data['messages'][-1]['id']

                    if not str(recent_last_msg_id) == str(last_msg_id) and not added:
                        pairs.add((channel_id,int(last_msg_id),'channel'))                        

                    added = True
            else:
                continue    
        
        if not added:
            pairs.add((channel_id,None,'channel'))

            added= True

    return pairs


def get_thread_lastmsg_tuple(files_save_location):
    pairs = set()
    channel_ids = get_all_channes()
    thread_ids = get_thread_ids_all(channel_ids)

    for thread_id,recent_last_msg_id,thread_channel_id in thread_ids:
        try:
            files_at_location = os.listdir(files_save_location+f'\\{thread_channel_id}')
        except FileNotFoundError:
            added = False
            files_at_location = []
        added = False
        if thread_id is None:
            continue
        for _file in files_at_location:
            if thread_id in _file and 'after' not in _file:
                with open(f'{files_save_location}\\{thread_channel_id}\\{_file}','r') as f:
                    data = json.load(f)
                    last_msg_id = data['messages'][-1]['id']

                    if not str(recent_last_msg_id) == str(last_msg_id) and not added:
                        pairs.add((thread_id,int(last_msg_id),'thread',thread_channel_id))

                    added = True
            else:
                continue
        if not added:
            pairs.add((thread_id,None,'thread',thread_channel_id))
            added = True

    return pairs


bash_cmd_only_chan = 'call dotnet DiscordChatExporter.Cli.dll export -c {} -f Json -t "{}" --markdown false -o "{}"\n'
bash_cmd_lastmsg_chan = 'call dotnet DiscordChatExporter.Cli.dll export -c {} --after {} -f Json -t "{}" --markdown false -o "{}"\n'

bash_cmd_only_thr = 'call dotnet DiscordChatExporter.Cli.dll export -c {} -f Json -t "{}" --markdown false -o "{}\{}"\n'
bash_cmd_lastmsg_thr = 'call dotnet DiscordChatExporter.Cli.dll export -c {} --after {} -f Json -t "{}" --markdown false -o "{}\{}"\n'

final_pairs_list = get_channel_lastmsg_tuple()
final_pairs_list.update(get_thread_lastmsg_tuple(files_save_location+'\\Threads'))

# final_pairs_list = get_thread_lastmsg_tuple(files_save_location+'\\Threads')

print(f"Found {len(final_pairs_list)} files to update, added them to batch script.")


locations_for_bat = ['',dll_file_location+'\\']
for location in locations_for_bat:
    with open(location+'my_cmd.bat','w') as f:
        f.write('@echo off\n')
        for i in final_pairs_list:
            if i[2] == 'channel':
                if i[1]:
                    f.write(bash_cmd_lastmsg_chan.format(i[0],i[1],bot_token,files_save_location))
                else:
                    f.write(bash_cmd_only_chan.format(i[0],bot_token,files_save_location))
            elif i[2] == 'thread':
                if i[1]:
                    f.write(bash_cmd_lastmsg_thr.format(i[0],i[1],bot_token,files_save_location+'\\Threads',str(i[3]))) #i[3] is the channel id in which thread is.
                else:
                    f.write(bash_cmd_only_thr.format(i[0],bot_token,files_save_location+'\\Threads',str(i[3])))

        f.write(r"""
set PYTHON_PATH=python
set FILE_3="{}stitch_json.py"

echo Stitching the json files: %FILE_3%
%PYTHON_PATH% %FILE_3%
if errorlevel 1 goto ERROR

echo All files have been processed. Press any key to exit.
pause > nul
exit /b 0

:ERROR
echo An error occurred while running one of the files.
pause > nul
exit /b 1
""".format(config.MAIN_PATH))
#         f.write("""\n
# echo.
# echo All files exported.
# pause > nul

# endlocal""")

if len(final_pairs_list) == 0:
    raise Exception('NO FILES TO UPDATE')
else:
    print('Batch Script Made.')
