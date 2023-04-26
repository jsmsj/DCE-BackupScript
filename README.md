# The Backup Script which I use to backup servers.

## Features:

1. The first run takes a bit of time as it has to export the entire server.
2. Then subsequent runs are not as much time consuming as it exports after the last message exported per channel.

## How to ?

1. First of all get the latest version of Discord Chat Exporter **CLI** from [here](https://github.com/Tyrrrz/DiscordChatExporter/releases/latest)
2. Extract it in [DCE_CLI](./DCE_CLI/) folder.
3. Open [config.py](./config.py) and edit the config accordingly. 
4. Open [backup_server.bat](./backup_server.bat) file and edit the `MAIN_PATH` variable. Make sure it is the same as the `MAIN_PATH` variable in [config.py](./config.py). And make sure it ends with a backslash `\`
5. Run the [backup_server.bat](./backup_server.bat) and it will start backupping your server.

#### PRO Tip 1 : Send the [backup_server.bat](./backup_server.bat) file to desktop as shortcut and run it whenever you want to export

#### PRO Tip 2 : Set [backup_server.bat](./backup_server.bat) in windows task scheduler and it will run whenever you want automatically. ([Tutorial](https://helpdeskgeek.com/windows-11/how-to-schedule-a-batch-file-to-run-in-windows-11-10-using-task-scheduler/))

#### PRO Tip 3: You can conver these JSON Files to HTML via [DCE-JSONtoHTML](https://github.com/jsmsj/DCE-JSONtoHTML/)

## Recommendations:
1. Using the bot token with highest privileges is recommended
2. Please while running the script for large servers, do not use any other highly RAM dependent programs, as the script loads the entire json file while stitching. [This will be fixed by using `ijson` library which loads only a part of json file, but for my usecase json module works just fine.]



### How it works ?
Lets say i run the script for the first time today. The script will call the official discord api and do the following

1. Get all Channels and the id of the last message sent in them.
    - 1.1 Compare these ids with the last message id already exported files in [Exported Files](./Exported%20Files/) Directory [Empty if exporting for the first time]
    - 1.2 Then if the last message id doesnt match, it adds that channel id to be exported. (The messages after sent that last message will be exported)

2. Get all the threads in all the channels (Both archived and public).
    - Repeat the above process as of the channels again.

3. Then it makes another batch script which will be called for exporting via Discord Chat Exporter CLI. (Happens automatically)
   
4. Lastly it stitches the json files made.
    - More info on stitching:
    - The files exported by the script after the last sent message (step 1.2) are made into a separate file, so the script stitches those separate file with the original file.


#### Credits:
1. [Discord Chat Exporter by Tyrrrz](https://github.com/Tyrrrz/DiscordChatExporter)