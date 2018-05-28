import requests

__USERID = ''
__AUTHTOKEN = ''

def loggedIn():
    return __USERID != ''

def hasToken():
    return __AUTHTOKEN != ''

def getAuthToken():
    return __AUTHTOKEN

def getUserID():
    return __USERID


def login(username, password, onsuccess, onfailed, onerror):
    url = "http://17chuchu.pythonanywhere.com/SystemArt/login/"

    data = {}
    data['username'] = username
    data['password'] = password

    print('logging in . . . ')
    response = requests.post(url, json=data)

    if response.ok:
        print('login result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']     # act as token when success

        if tag == 0:
            global __USERID
            global __AUTHTOKEN
            __USERID = result['id']
            __AUTHTOKEN = comment
            onsuccess()
        else:
            onfailed(tag, comment)
    else:
        onerror()


def createCreator(name, username, password, email, onsuccess, onfailed, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/register/'

    data = {}
    data['name'] = name
    data['username'] = username
    data['password'] = password
    data['email'] = email

    print('creating creator . . . ')
    response = requests.post(url, json=data)

    if response.ok:
        print('create creator result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']

        if tag == 0:
            onsuccess()
        else:
            onfailed(tag, comment)
    else:
        onerror()

def createAdmin(name, username, password, email, onsuccess, onfailed, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/registeradmin/'

    data = {}
    data['authtoken'] = getAuthToken()
    data['name'] = name
    data['username'] = username
    data['password'] = password
    data['email'] = email

    print('creating admin . . . ')
    response = requests.post(url, json=data)

    if response.ok:
        print('create admin result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']

        if tag == 0:
            onsuccess()
        else:
            onfailed(tag, comment)
    else:
        onerror()

def getCreatorList(onreceive, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/listallartist/'
    data = {}
    data['authtoken'] = getAuthToken()

    print('getting creator list . . .')
    response = requests.post(url, json=data)

    if response.ok:
        print('get creator list result:', response.text)
        onreceive(response.json())
    else:
        onerror()

# add file
def addFile(name, path, onsuccess, onfailed, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/addfile/'
    data = {}
    data['authtoken'] = getAuthToken()
    data['name'] = name
    data['path'] = path

    print('add file . . .')
    response = requests.post(url, json=data)

    if response.ok:
        print('add file result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']

        if tag == 0:
            onsuccess(comment[-32:])
        else:
            onfailed(tag, comment)
    else:
        onerror()

# add file version
def addVersion(fileid, version, filetype, onsuccess, onfailed, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/addversion/'
    data = {}
    data['authtoken'] = getAuthToken()
    data['fileid'] = fileid
    data['version'] = version
    data['filetype'] = filetype

    print('add version . . .')
    response = requests.post(url, json=data)

    if response.ok:
        print('add version result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']

        if tag == 0:
            onsuccess(comment[-32:])
        else:
            onfailed(tag, comment)
    else:
        print(response.text)
        onerror()

# remove file
def deleteFile(fileid, onsuccess, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/removefile/'
    data = {}
    data['authtoken'] = getAuthToken()
    data['id'] = fileid

    print('delete file . . .')
    response = requests.post(url, json=data)

    if response.ok:
        print('delete file result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']

        onsuccess()
    else:
        print(response.text)
        onerror()

# list all file [ DONE ]
def getFileList(onreceive, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/listallfile/'
    data = {}
    data['authtoken'] = getAuthToken()

    print('getting file list . . .')
    response = requests.post(url, json=data)

    if response.ok:
        print('get file list result:', response.text)
        fileDict = response.json()
        fileList = [ fileDict[k] for k in fileDict ]
        for f, i in zip(fileList, fileDict.keys()): f['id'] = i
        onreceive(fileList)
    else:
        onerror()

# list all version of a file

if __name__ == '__main__':
    def onsuccess():
        print("success")

    def onfailed(tag, comment):
        print("login failed:", tag, comment)

    def onerror():
        print("error:")

    login('admin', '1234', onsuccess, onfailed, onerror)

    # createCreator('saitama', 'sait3do*!*o', '', 'sai3.com', onsuccess, onfailed, onerror)

    # createAdmin(getAuthToken(), 'Tawan Thampipattanakul', 'tawan', '1234', 'tawan.tpptnk@gmail.com', onsuccess, onfailed, onerror)

    def onreceive(result):
        print('receive:', result)

    # getCreatorList(onreceive, onerror)

    deleteFile("bbdf054b455c4ddaa2c2b2510cf69ebd", onsuccess, onerror)
    # deleteFile("bc926034601e43e1805e5573fd9fb2c8", onsuccess, onerror)
    getFileList(onreceive, onerror)

    def onsuccess(fileid):
        print("success add file", fileid)

    # addFile("folder 1", "1-0-folder 1", onsuccess, onfailed, onerror)
    addFile("folder 2", "2-1-folder 2", onsuccess, onfailed, onerror)
    # addFile("c.png", "3-1-c.png", onsuccess, onfailed, onerror)
    # addFile("d.png", "4-2-d.png", onsuccess, onfailed, onerror)
    # addFile("e.png", "5-0-e.png", onsuccess, onfailed, onerror)
    # addFile("f.png", "6-0-f.png", onsuccess, onfailed, onerror)

    # addVersion("7edf103680424da39a69ee6e9760152b", "1.1", ".png", onsuccess, onfailed, onerror)

