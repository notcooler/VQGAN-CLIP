
fileRead = open("./run_me.py", 'r')
lines = fileRead.readlines()
lines[22] = "import generator\n"
fileWrite = open("./run_me.py", 'w')
fileWrite.writelines(lines)