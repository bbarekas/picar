#!/usr/bin/python3
import cv2
from picamera2 import Picamera2, Preview
from libcamera import Transform, controls
from AlphaBot2 import AlphaBot2
import numpy as np
import os
import time

##
## Μεταβλητές και παράμετροι
##

# Font για την παρουσίαση του κειμένου. 
font = cv2.FONT_HERSHEY_SIMPLEX
# id για το πρόσωπο που θα παρακολουθεί το robot.
target_face_id = 0
# id του προσώπου που αναγνωρίστηκε.
id = 0
# Ονόματα των προσώπου που περιέχει το μοντέλο αναγνώρισης προσώπου.
names = ['None', 'Maria', 'Iris', 'Kostas']
# Μέγεθός του προσώπου που αναγνωρίστηκε, σε pixels
size = 0
# Κανονικό μέγέθος προσώπου, σε pixels.
normal_size = 250
# Flag που δείχνει ότι το πρόσωπο που θέλουμε έχει βρεθεί. 
found = False
# Διάνυσμα που κρατάει τα n τελευταία μεγέθη προσώπου - χρησιμοποιείται για την μέτρηαη του μέσου όρου του μεγέθους.
n = 2
last_sizes = np.zeros(n, dtype=int)
count = 0


##
## Έναρξη του προγράμματος
##

# Αρχικοποίηση του robot.
abot = AlphaBot2()

# Ρώτησε τον χρήστη να δώσει το id του χρήστη που θέλουμε να παρακολουθεί το robot. 
target_face_id_str = input('\n * Enter user id to follow and press <return> ==> ')
target_face_id = int(target_face_id_str)

print("\n [INFO] Έναρξη αναγνώρισης προσώπου. Κοίτα στην κάμερα και περίμενε ...")

# Φόρτωση του προ-εκπαιδευμένου μοντέλου αναγνώρισης προσώπου LBPH από το αρχείο.
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

# Αρχικοποίηση του ανιχνευτή προσώπου.
face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

# Αρχικοποίηση της κάμερας.
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
time.sleep(0.5)
picam2.start_preview(Preview.DRM)
picam2.start()

print(" [INFO] > Looking for face: {0}".format(target_face_id))

# Έναρξη του κύριου βρόχου αναζητώντας το επιθυμητό πρόσωπο.  
while True:
    found = False   

    # Λήξη στιγμιότυπου σπό την κάμερα. 
    im = picam2.capture_array()
    # Μετατροπή σε ασπρόμαυρο. 
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # Εκτέλεση του αν προσώπων πάνω στο ασπρόμαυρο στιγμιότυπο.
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(24, 24),
    )

    # Επεξεργασία όλων των προσώπων που ανιχνεύτηκαν.
    for (x, y, w, h) in faces:
        # Εμφάνισε ένα πράσινο τετραγώνο γύρω απο το πρόσωπο.
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Εκτέλεση του μοντέλου αναγνώρισης προσώπου πάνω στο ανιχνευμένο πρόσωπο.
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # If target face found then update the last_sizes vector. 
        # Αν είναι το ζητούμενο πρόσωπο τότε ανανέωσε το διάνυσμα με τα μεγέθη και το flag.
        if (id == target_face_id) and (confidence < 100) :
            print(" [INFO] > Found: {0} p:{1}".format(id, confidence))
            found = True
            last_sizes[count%n] = w
            count = count + 1

        # Βρές το όνομα και τo επίπεδο σιγουριάς για αυτό το πρόσωπο.
        if (confidence < 100):
            id = "{0} {1}x{2}".format(names[id], w, h)
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        # Εμφάνισε το όνομα και τo επίπεδο σιγουριάς για αυτό το πρόσωπο.
        cv2.putText(im, str(id), (x + 5, y - 5), font, 0.7, (255, 255, 255), 2)
        cv2.putText(im, str(confidence), (x + 5, y + h - 5), font, 0.4, (255, 255, 0), 1)
    # τέλος for 

    # Βρές το μέσο όρο των μεγεθών στο διάνυσμα.
    size = last_sizes.mean()
    if found:
        # Αν έχει βρεθεί το ζητούμενο πρόσωπο.
        if size < normal_size*0.9:
            # Αν το μέγεθος του προσώπου είναι μικρότερο απο το 90% του μέγεθος αναφοράς, τότε κινήσου εμπρός. 
            print(" [INFO] > Forward ... {0}".format(size))
            abot.forward()
            time.sleep(0.2)
            abot.stop()
            
        elif size > normal_size*1.1:
            # Αν το μέγεθος του προσώπου είναι μεγαλύτερο απο το 110% του μέγεθος αναφοράς, τότε κινήσου πίσω. 
            print(" [INFO] > Backward ... {0}".format(size))
            abot.backward()
            time.sleep(0.2)
            abot.stop()
            
        else:
            # Αλλιων το μέγέθος του προσώπου είναι στα ότι του μέγέθος αναφοράς, μην κινήσε.
            print(" [INFO] > Still ... {0}".format(size))
            abot.stop()

        # Έλεγξε το θέση του προσώπου στον οριζόντιο άξονα x.
        if x < 150:
            # Αν η θέση του προσώπου βρίσκεται στο αριστερό άκρο, τότε στρίψε αριστερά.
            print(" [INFO] > << Left ... {0}".format(x))
            abot.left()
            time.sleep(0.01)
            abot.stop()
        elif x+w > 640-150:
            # Αν η θέση του προσώπου βρίσκεται στο δεξιό άκρο, τότε στρίψε δεξιά.
            print(" [INFO] > {0} ... Right >>".format(x+w))
            abot.right()
            time.sleep(0.01)
            abot.stop()
            
    else:
        # Αν δεν έχει βρεθεί το ζητούμενο πρόσωπο αρχικοποιήσε το διάνυσμα μεγεθών.
        print(" [INFO] > ... Stop ... {0}".format(size))
        last_sizes = np.zeros(n, dtype=int)
        count = 0
        abot.stop()

    # Εμφάνισε το τελικό στιγμιότυπο (εικονα + τετραγώνα + κείμενο) στην οθόνη. 
    cv2.imshow('camera', im)


    # Αν έχει πατηθεί το πλήκτρο ESC ολοκλήρωσε τον βρόχο.
    k = cv2.waitKey(10) & 0xff  
    if k == 27:
        break


# Τέλος και εκκαθάριση.
print("\n [INFO] Ολοκλήρωση προγράμματος.")
picam2.stop()
cv2.destroyAllWindows()
