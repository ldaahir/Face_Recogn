import os,random,face_recognition,pickle,numpy as np,cv2
# import pickle,random,cv2,face_recognition,pandas as pd,numpy as np
from pathlib import Path
import Face_Recogination.xog as xog
import os
from PIL import Image
pathka = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db=xog.Data()
db.create_table()

class Main:
    def __init__(self,
                 ddir=pathka + "/media/dataset/image/",data=pathka + "/media/dataset/data/",
                 test=pathka + "/media/dataset/test/",folder_path=pathka + "/media/dataset/check/"):
        self.image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # Add more extensions if needed
        self.ddir=ddir
        self.folder_path=folder_path
        self.data=data
        self.test=test





    def crop_face_and_neck(self,input_path, output_path):
     

        # Load the image file into a numpy array
        image = face_recognition.load_image_file(input_path)

        # Find all face locations in the image
        face_locations = face_recognition.face_locations(image)

        # Proceed if at least one face is detected
        if face_locations:
            top, right, bottom, left = face_locations[0]  # Get the first face

            # Adjust the bottom part to include the neck
            height = bottom - top
            new_bottom = int(bottom + 0.5 * height)  # Extend the crop by 50% of the face height downwards

            # Load the image with Pillow
            pil_image = Image.open(input_path)
            face_image = pil_image.crop((left, top, right, new_bottom))

            # Save the cropped image
            face_image.save(output_path)
            # face_image.show()
            print(f"Cropped image saved to {output_path}")
        else:
            print("No faces found in the image.")

    # Example usage
    # crop_face_and_neck("path_to_your_image.jpg", "path_to_save_cropped_image.jpg")

    def count_files_in_folder(self,folder_path):
        file_count = 0
        # Iterate over all files in the folder
        for _, _, files in os.walk(folder_path):
            file_count += len(files)

        return file_count

    def rename_files(self,folder_path=pathka + "/media/dataset/check/"):
        self.folder_path=folder_path
        if  os.path.exists(self.folder_path):
            try:
                os.makedirs(self.ddir)
                os.makedirs(self.data)
                os.makedirs(self.test)
            except:
                pass
        self.image_files = []
        for file_name in os.listdir(self.folder_path):
            if os.path.isfile(os.path.join(self.folder_path, file_name)):
                _, extension = os.path.splitext(file_name)
                if extension.lower() in self.image_extensions:
                    self.image_files.append(file_name)
        return len(self.image_files)



    def generate(self,):
        first_male = ["Liban", "khadar", "Abas", "suleyman", "Omar", "Abdullahi"]
        first_female = ["khadro", "sacdiyo", "xalimo", "caasho", "safiyo", "ruweydo"]
        second_names = ["Yaxye", "mohamed", "Axmed", "Maxmuud", "Abdiqaadir", "Da'ud"]
        last_names = ["Cali", "Geedi", "Yusuf", "Kaafi", "Abdulle", "Khaalid"]
        fasal = ["CA206", "CA207", "CA209", "CA201", "CA202", "CA205"]
        try:
            pickle_file_path = self.data+"encodings.pkl"
            with open(pickle_file_path, 'rb') as file:
                data = pickle.load(file)
            encode = data["encodings"]
            ID = data ["ID"]

        except:
            encode = []
            ID = []
        last_first_male_index = len(first_male) - 1
        last_second_names_index = len(second_names) - 1
        last_last_names_index = len(last_names) - 1
        DEFAULT_ENCODINGS_PATH = Path(self.data+"encodings.pkl")
        count_test=0
        count_remove=0
        count=0
        saved=0
        if db.count() == None:
            kii=1
        else:
            kii=int(db.count())
        for file_name in os.listdir(self.folder_path):
            if os.path.isfile(os.path.join(self.folder_path, file_name)):
                _, extension = os.path.splitext(file_name)
                if extension.lower() in self.image_extensions:
                    first = random.randint(0, last_first_male_index)
                    second = random.randint(0, last_second_names_index)
                    last = random.randint(0, last_last_names_index)
                    full_name = first_male[first] + " " + second_names[second] + " " + last_names[last]

                    file=self.folder_path + file_name
                    croped = self.test+file_name
                    self.crop_face_and_neck(file,croped)
                    image = face_recognition.load_image_file(croped)
                    face_encoding = face_recognition.face_encodings(image)
                    encode_test=np.array(encode)
                    if len(face_encoding) > 0 :
                        face_distances = face_recognition.face_distance(encode_test, face_encoding[0])
                        matches = face_distances < 0.1
                        face_distances_test = face_recognition.face_distance(encode_test, face_encoding[0])
                        matches_test = face_distances_test < 0.5
                        if np.any(matches):
                            count+=1
                        elif np.any(matches_test):
                            count_test+=1
                        else:
                            kii+=1
                            IDga = "C11800" + str(kii)
                            ID.append(IDga)
                            encode.append(face_encoding[0])
                            new_file = self.ddir+IDga+".jpg"
                            sawir = new_file.replace('/home/liban/Downloads/Group76', '')
                            print("sawir waa : ",sawir)
                            os.rename(croped,self.test+IDga+".jpg")
                            os.rename(self.folder_path+file_name,new_file)
                            db.insert_data(IDga,full_name,fasal[last],617653631,sawir)
                            saved+=1
                    else:
                        count_remove+=1
                    try:
                        os.remove(self.folder_path+file_name)
                        os.remove(croped)
                    except:
                        pass

        name_encodings = {"ID": ID, "encodings": encode}
        with DEFAULT_ENCODINGS_PATH.open(mode="wb") as f:
            pickle.dump(name_encodings, f)
        return "saved images : "+str(saved), "we catched duplicated images are :"+str(count)+"   ","Same person images are "+str(count_test),"remove images that was not found face are : "+str(count_remove)

    def load_data(self):
        # Read pickle data
        try:
            pickle_file_path = self.data+"encodings.pkl"
            with open(pickle_file_path, 'rb') as file:
                data = pickle.load(file)
            self.known_face_encodings = data["encodings"]
            self.known_face_names    = data["ID"]
            self.image_list = db.get_column("Image ")
        except:
            self.known_face_encodings = []
            self.known_face_names    = []
            self.image_list = db.get_column("Image ")

    def recognize_face(self,test_image_path, distance_threshold=0.5):
        self.load_data()
        distance_threshold=distance_threshold
        fileka=test_image_path.split("/")[-1:]
        fileka = self.test+fileka[0]
        print("_"*100,fileka,"\n_"*100)
        self.crop_face_and_neck(test_image_path,fileka)

        test_image = face_recognition.load_image_file(fileka)
        test_face_encodings = face_recognition.face_encodings(test_image)

        if len(test_face_encodings) == 0:
            return "No face found in the test image"

        face_distances = face_recognition.face_distance(self.known_face_encodings, test_face_encodings[0])
        matches = face_distances < distance_threshold
        if np.any(matches):
            matched_names = np.array(self.known_face_names)[matches].tolist()
            all = []
            for i in matched_names:
                x = db.search_data(i)
                all.append(x)
            return all
        elif distance_threshold<0.45:
            distance_threshold+=0.1
            x = self.recognize_face(test_image_path,distance_threshold)
            # os.remove(fileka)
            return x
        else:
            os.remove(fileka)
            return ("No match found for the test image.")

    

