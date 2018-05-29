import pyrebase

config = {
        "apiKey": "AIzaSyD6C98peZHQUyzB2bhpJjZ3Y_sARMsrZH0",
        "authDomain": "airimage-79957.firebaseapp.com",
        "databaseURL": "https://airimage-79957.firebaseio.com",
        "storageBucket": "airimage-79957.appspot.com",
        "serviceAccount": "airimage-79957-firebase-adminsdk-b2ye5-ac8a8778e4.json"
        # "serviceAccount": "/Users/admin/Documents/Project_Mine/asset-manager-admin-pyqt/assetcollection-998d1-firebase-adminsdk-bw43v-aaf7b10ac6.json"
    }

firebase = None
storage = None

def init():
    global firebase
    global storage

    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

def upload(firebasepath, localpath):
    storage.child(firebasepath).put(localpath)

def download(firebasepath, localpath):
    storage.child(firebasepath).download(localpath)


if __name__ == '__main__':
    init()
    # upload('2159f1a2d7f048dfa186b44b32b77d28/3.png', 'img/artist-icon.png')
    # download('2159f1a2d7f048dfa186b44b32b77d28/3.png', 'try.png')
