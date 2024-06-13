import pyrebase

config = {
    'apiKey': "AIzaSyARfKLsqISHQEv3ufLMngyuh5fcx0rEOmA",
  'authDomain': "soil-analysis-crop-reco.firebaseapp.com",
  'databaseURL': "https://soil-analysis-crop-reco-default-rtdb.firebaseio.com",
  'projectId': "soil-analysis-crop-reco",
  'storageBucket': "soil-analysis-crop-reco.appspot.com",
  'messagingSenderId': "288273313346",
  'appId': "1:288273313346:web:b1aa248878cc778799c7db"

}
firebase = pyrebase.initialize_app(config)
auth =firebase.auth()

email = 'Test@gmail.com'
password = '123456'