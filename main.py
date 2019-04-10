import argparse, os, re
import xml.etree.ElementTree as ET

def main(Args, FeatureOption):
    '''
    Main function
    :param args: arguments acquired from command lines(refer to ParseArgs() for list of args)
    :param FeatureOption: False
    '''

    xml_tree = ET.parse(Args.config)
    config = xml_tree.getroot()

    for directory in config.findall('directory'):

        # Get what number the file starts at ex. 001 or 000 would be 1 or 0
        file_num_start = int(directory.get('first_file_num'))

        #do a try here
        # Get a list of files in the directory
        file_list = os.listdir(directory.get('path'))

        directory_file_numbers = []

        for file in file_list:
            #returns what is inbetween the naming_scheme and file_extention then converts into an int
            directory_file_numbers.append(int(find_between(file, directory.get('naming_scheme'), '.')))

        # Create a list of sequential integers that would correspond with all files if none were missing
        desired_file_numbers = list(range(file_num_start, int(directory.get('file_count'))+file_num_start))


        missing_files_list = list(set(desired_file_numbers) - set(directory_file_numbers))

        if missing_files_list:
            print(directory.get('name') + " is missing files", missing_files_list)
        else:
            print(directory.get('name') + " has all expected files")

def find_between(string, start, end):
  return ((string.split(start)[1]).split(end)[0])

def ParseArgs():
    Args =  argparse.ArgumentParser(description="Detection of missing sequentially numbered files")
    Args.add_argument("--config", default= "config.xml",
                      help= "Absolute path to the configuration xml")
    return Args.parse_args()

if __name__ == "__main__":
    main(ParseArgs(), True)
