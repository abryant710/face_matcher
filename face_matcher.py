import face_recognition as fr
import time  # to measure operation time

"""
    FaceMatcher can 
        - find a face in an image, returning a tuple showing location
        - find a faces in a batch of images as above, returning a list of locations
        - perform a single match between two images (1:1)
        - cross match a single image with a list of other images (1:N)
        - cross match a list of images with another list of images (N:N)
        - write a csv file of results to a text file
"""


class FaceMatcher:

    #  Method to initialise the class
    def __init__(self, tolerance=0.7):
        self.tolerance = tolerance  # This is acctually unused

    # Find faces in a single image
    #     image, Image file path
    #     match_model="cnn", mode of matching as per face_recogntion module spec
    def find_faces(self, image, match_model="cnn"):
        loaded_image = fr.load_image_file(image)
        face_locations = fr.face_locations(loaded_image, model=match_model)
        if face_locations:
            return face_locations
        return None

    # Find faces in a batch of images
    #     input_list, list of image file paths
    #     do_log=False, log each on processed
    #     track_progress=200, log message after every batch of this size completed
    #     match_model="cnn", mode of matching as per face_recogntion module spec
    def find_faces_batch(self, input_list, do_log=False, track_progress=200, match_model="cnn"):
        start = time.time()
        faces_found_col = []
        for num, image_path in enumerate(input_list, start=1):
            if(do_log):
                print("Processing...", image_path)
            face_found = self.find_faces(image_path, match_model)
            if(do_log):
                print("Faces found", face_found)
            if(num % track_progress == 0):
                print(num, "processed in", int(time.time() - start), "seconds")
            faces_found_col.append(face_found)
        finish_time = int(time.time() - start)
        print("All completed. Average processing time of",
              (finish_time / len(input_list)), "seconds per image")
        return faces_found_col

    # Create a biometric template of the face and return it
    #     image_path, path to image to load
    #     location, precalulated face location
    def create_template(self, image_path, location):  # This is like a single enrollment
        face_image = fr.load_image_file(image_path)
        location = tuple(map(lambda x: int(x), location))
        template = fr.face_encodings(
            face_image, known_face_locations=[location])
        return template

    # Create a dictionary of templates, acting as bulk enrollment
    #     enrollment_list, a list of tuples, (index, [image_path, location])
    def enroll_batch(self, enr_list):
        start = time.time()
        enrollment_dict = {}
        for item in enr_list:
            enrollment_dict[item[0]] = self.create_template(
                item[1][0], item[1][1])
            if(item[0] % 100 == 0):
                print("Enrolled...", item[0])
        print("Finished enrolling", len(enr_list),
              "in", int(time.time() - start), "seconds")
        return enrollment_dict

    # Single match on two images
    #     encoding_1
    #     encoding_2
    def single_match(self, encoding_1, encoding_2, threshold=0.6):
        # With the threshold we are inverting the score so higher thresholds mean harder to match
        # dissimilar pairs.
        return fr.compare_faces(encoding_1, encoding_2[0], tolerance=(1 - threshold))

    # Generate a score
    #     encoding_1
    #     encoding_2
    #     mate, tell the function that the ground truth says the two images are the same person
    #     This is a recursive function that calls itself until a match is made.
    #     Do not give kwarg new_threshold on first iteration, but do say whether mate=True/False initially
    def generate_score(self, encoding_1, encoding_2, mate=True, start=True, new_threshold=1.0, logging=False):
        # When the threshold returns it represents the score where the images match
        if(mate):
            threshold = new_threshold if new_threshold else 1.0
            if(logging):
                print("testing threshold...", "%.2f" % threshold)
            match = self.single_match(encoding_1, encoding_2, threshold)[0]
            if(match):
                return "%.2f" % new_threshold
            threshold -= 0.01
            return self.generate_score(encoding_1, encoding_2, new_threshold=threshold, mate=mate, start=False, logging=logging)
        else:
            threshold = new_threshold if new_threshold else 0.0
            if(logging):
                print("testing threshold...", "%.2f" % threshold)
            match = self.single_match(encoding_1, encoding_2, threshold)[0]
            if not (match):
                return "%.2f" % new_threshold
            threshold += 0.01
            return self.generate_score(encoding_1, encoding_2, new_threshold=threshold, mate=mate, start=False, logging=logging)

    # Mini function to generate a CSV file of results
    def create_csv_file(self, file_name, arr):
        with open(file_name, 'w') as f:
            for item in arr:
                f.write("%s\n" % item)

    # Cross match a batch of images by id
    #     enrollments, dictionary of all enrollment with id as key and value as biometric template
    #     pairs, list of lists of pairs of ids
    #     csv_output, CSV file to write results to after job completed
    def cross_match_pairs(self, enrollments, pairs, csv_output):
        start = time.time()
        scores = []
        scores.append("subject_id_1,subject_id_2,score")
        for count, pair in enumerate(pairs):
            score = self.generate_score(
                enrollments[pair[0]], enrollments[pair[1]], mate=True, logging=False, new_threshold=False)
            scores.append(str(pair[0]) + "," + str(pair[1]) + "," + str(score))
            if(count % 5000 == 0):
                print(count, "matches completed")
        print("Finished matching pairs in", int(
            time.time() - start), "seconds")
        self.create_csv_file(csv_output, scores)
