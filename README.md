Hi, these are the instructions to execute the program

1. Install python `3.10.0` from https://www.python.org/downloads/release/python-3100/ 
    and make sure to check the box that says "Add Python 3.10 to PATH" while installing.

2. Open the project folder in Command Prompt (by typing cmd in the folder path) and run the following command to install the required python packages.
```pip install -r requirements.txt```

3. for extracting SKUs you can run the following command and wait for the script to finish.
```python sku_extractor.py```

4. for main script you can run the following command.
```python main.py```

5. script will ask for the city name, enter the name and hit enter.

6. Script will store done SKUs in the `done_sku.txt` file. if you want to run the script from scratch, delete the data from `done_sku.txt` file.

7. if you want to terminate the process press Ctrl + c couple of times in the cmd.

**How to run 6 scripts in parallel**: after following the above steps, you can run the scripts in the following order:

1. make folders(as per the number of cities) and place all the files in each folder.

2. Open each folder in Command Prompt (by typing cmd in the folder path)
 
3. Now you can run the scripts in the following order(make sure the SKUs are pre-fetched):
`python main.py`


_feel free to ask any question if you have any._
```Hassaan Mughal```
```Email: hassaanmughal143@gmail.com```
```Phone: +923203650954```
