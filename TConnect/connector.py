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

def getAdminList(onreceive, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/listalladmin/'
    data = {}
    data['authtoken'] = getAuthToken()

    print('getting admin list . . .')
    response = requests.post(url, json=data)

    if response.ok:
        print('get admin list result:', response.text)
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
    print('json =', data)
    response = requests.post(url, json=data)

    if response.ok:
        print('add version result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']

        if tag == 0:
            onsuccess(comment.split('#')[1])
        else:
            onfailed(tag, comment)
    else:
        print(response.text)
        onerror()

def deleteUser(id, onsuccess, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/removeartist/'
    data = {}
    data['authtoken'] = getAuthToken()
    data['id'] = id

    print('delete user . . .')
    response = requests.post(url, json=data)

    if response.ok:
        print('delete user result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']

        onsuccess()
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
def getVersionList(fileid, onreceive, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/listallversionoffile/'
    data = {}
    data['authtoken'] = getAuthToken()
    data['fileid'] = fileid

    print('getting version list of ',fileid, '. . .')
    response = requests.post(url, json=data)

    if response.ok:
        print('get version list result:', response.text)
        versionDict = response.json()
        versionList = [ versionDict[k] for k in versionDict ]
        onreceive(versionList)
    else:
        onerror()

def editUser(id, name, username, password, email, onsuccess, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/edituserinfo/'
    data = {}
    data['authtoken'] = getAuthToken()
    data['id'] = id
    data['name'] = name
    data['username'] = username
    data['password'] = password
    data['email'] = email

    print('edit user . . .')
    print(data)
    response = requests.post(url, json=data)

    if response.ok:
        print('edit user result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']

        onsuccess()
    else:
        print(response.text)
        onerror()


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

    # getAdminList(onreceive, onerror)
    # getCreatorList(onreceive, onerror)

    # deleteFile("7edf103680424da39a69ee6e9760152b", onsuccess, onerror)
    # deleteFile("cc008eae97764193932d7fe930fceb35", onsuccess, onerror)
    getFileList(onreceive, onerror)

    def onsuccess(fileid):
        print("success add file", fileid)

    # addFile("folder 1", "1-0-folder 1", onsuccess, onfailed, onerror)
    # addFile("folder 2", "2-1-folder 2", onsuccess, onfailed, onerror)

    # addFile("c.png", "3-1-c.png", onsuccess, onfailed, onerror)
    # addFile("d.png", "4-2-d.png", onsuccess, onfailed, onerror)
    # addFile("e.png", "5-0-e.png", onsuccess, onfailed, onerror)
    # addFile("f.png", "6-0-f.png", onsuccess, onfailed, onerror)

    # addVersion("2159f1a2d7f048dfa186b44b32b77d28", "1", ".png", onsuccess, onfailed, onerror)
    # addVersion("2159f1a2d7f048dfa186b44b32b77d28", "2", ".png", onsuccess, onfailed, onerror)
    # addVersion("2159f1a2d7f048dfa186b44b32b77d28", "3", ".png", onsuccess, onfailed, onerror)
    # addVersion("2159f1a2d7f048dfa186b44b32b77d28", "4", ".png", onsuccess, onfailed, onerror)

    # getVersionList("2159f1a2d7f048dfa186b44b32b77d28", onreceive, onerror)
    # getVersionList("2986c86deae34f9eb498bdf040fa808c", onreceive, onerror)

