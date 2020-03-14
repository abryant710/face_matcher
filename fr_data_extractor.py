import os
import sys

"""
    This class assumes the following format fo the file data. 13 columns separated by underscores.
    The format of the filenames is A_B_C_D_E_F_G_H_I_J_K_L_M.jpg, where:
    A= subject ID (xxxx).
    B= image sequence number (xxxxx).
    C= gender (x); (m) for male images and (f) for female images.
    D= age (xx).
    E= lighting (x); (i) for indoor lighting and (o) for outdoor lighting.
    F= view (xx); (fr) for frontal images and (nf) for near-frontal images.
    G= cropped (xx); (cr) or not (nc).
    H= facial emotion (xx); (no) for normal, (hp) for happy, (sd) for sad/angry/disgusted, and
    (sr) for surprised/fearful.
    I= year (xxxx).
    J= part (x); (1) for part 1 of the dataset and (2) for part 2 of the dataset.
    K= occlusion (xx); (e0) for eye occlusion, which is the common in all images, (en) for eye
    and nose occlusion, and (em) for eye and mouth occlusion.
    L= image filters (xx); (nl) for normal images without any filters, (Gn) for images with
    Gaussian noise, (Gs) for images with Gaussian smooth, and (Ps) for posterized images.
    M= level of difficulty (x); (o) for original images, (e) for the easy level, (m) for the medium
    level, and (h) for the hard level of difficulty. 
    Additional column added: 
    N= relative file path of the image file from root dir of project
"""


class FrDataExtractor:

    #  Method to initialise the class
    def __init__(self, columns, image_path='.', image_type='jpg'):
        self.image_path = image_path
        self.image_type = image_type
        self.columns = columns

    # Line formatting specific to format of data accumulated
    def __set_column_names(self, delimiter):
        # Return each lines with specified column and delimit with inputted delimiting char
        # Also adding file_path as a column
        return delimiter.join(self.columns) + ",image_path"

    # Line formatting specific to spec
    def __format_line(self, line, delimiter):
        # First remove file path then replace all underscores with delimiting char
        # Checking that the length matches input of columns (or ignore line)
        if(len(line.split("_")) == len(self.columns)):
            return line.replace('.' + self.image_type, "").replace("_", delimiter)
        return None  # Ignore rows that don't conform to the defined standard

    #  Read in data from the images directory specified in class instantiation
    def __read_dir(self):
        try:
            path = self.image_path
            files = []
            # r=root, d=directories, f=files
            for r, d, f in os.walk(path):
                for file in f:
                    file_str = '.' + self.image_type
                    if file_str in file:
                        files.append(os.path.join(r, file).replace(
                            self.image_path + "/", ""))
            return files  # returns a list of file names in a dir of a certain file type
        except IOError as e:
            print("I/O error", e)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    # Generate CSV from list of file_names
    # Only method available to call externally. This class should be adapted for different formats of data
    def generate_csv(self, file_name, delimiter):
        try:
            f = open(file_name, "w")  # Open the file for writing
            try:
                f.write(self.__set_column_names(delimiter) + '\n')
                for line in self.__read_dir():
                    formatted_line = self.__format_line(line, delimiter)
                    #  line is the relative filepath of the file
                    if formatted_line:
                        f.write(formatted_line + delimiter +
                                self.image_path + "/" + line + '\n')
            finally:
                f.close()  # Close the file
        except IOError as e:
            print('Could not generate CSV file')
