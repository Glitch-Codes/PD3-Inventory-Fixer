# PD3-Inventory-Fixer

Small Python script for removing items that may have been added to your Payday 3 inventory by accident using a "External Shop". 

You will need to sniff for your UserID, Access Token and Refresh Token. There are a few tutorials out there using Fiddler. 

![image](https://github.com/Glitch-Codes/PD3-Inventory-Fixer/assets/54895281/4c153471-0674-49f8-bbd4-166db013c12e)

Paste those values into the config.json then run the main.py file. It will automatically grab your inventory and scan for any items that could be cheated. 
You will get 2 chances to skip removing an item. I am not responsible if you remove a hard-earned Infamous Reward. 
You may disable certain items from being scanned by changing the "True" flag in the items.json file to "False" (Must be capitalized).

NOT ALL ITEMS CAN BE REMOVED. The way I remove items is by flagging them as consumed. This used to work fine at launch but they have slowly changed
some items to not be consumable anymore.

Requirements: Python 3.x

Libraries: requests, json

