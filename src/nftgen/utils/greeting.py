def greet():
    _title()
    _info()


def _title():
    print("""\
         __ _                          
        / _| |                         
  _ __ | |_| |_ ______ __ _  ___ _ __  
 | '_ \|  _| __|______/ _` |/ _ \ '_ \ 
 | | | | | | |_      | (_| |  __/ | | |
 |_| |_|_|  \__|      \__, |\___|_| |_|
                       __/ |           
                      |___/            \
""")


def _info():
    print("""\
Enter "?" to get the list of available commands.\
""")
