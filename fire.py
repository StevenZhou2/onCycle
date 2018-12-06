from firebase import firebase
firebase = firebase.FirebaseApplication('https://oncycle-4654b.firebaseio.com', None)
result = firebase.get('/data', None)
print result
