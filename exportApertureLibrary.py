import os
import applexml
import datetime
import shutil

def main(libary_path, export_path):

    # Read xml file
    xml_file = os.path.join(libary_path, 'AlbumData.xml')
    xml_content = applexml.parse_xml(xml_file)

    # Make list of albums with path to pictures
    event_albums = [album for album in xml_content["List of Albums"] if  album["Album Type"] == "Event"]
    master_image_list = xml_content["Master Image List"]
    for album in event_albums:
        imageIDs = album["KeyList"] # get contained images in album
        album["ImageList"] = [] # add list with paths to images
        album["Date"] = convert_interval_to_datetime(album["ProjectEarliestDateAsTimerInterval"]) # add date field
        for id in imageIDs:
            image = master_image_list[str(id)]
            # If raw image, use original image, else image path and
            # replace iPhoto path with export path
            if "OriginalPath" in image:
                new_path = replace_path(image["OriginalPath"], libary_path)
            else:
                new_path = replace_path(image["ImagePath"], libary_path)
            album["ImageList"].append(new_path) # append path to image list of album
            album["Date"] = max(album["Date"], convert_interval_to_datetime(image['DateAsTimerInterval'])) # if image is older than all others, overwrite date stamp
        export_folder = album["Date"].strftime("%Y_%m_") + album["AlbumName"] # set album name in YYYY_mm_<Name> format
        export_folder = export_folder.replace(":", " -") # replace string conflicting with Windows paths
        export_folder = export_folder.replace("\"", "'") # replace string conflicting with Windows paths
        album["ExportPath"] = os.path.join(export_path, export_folder) # set export path

    # Copy images
    for album in event_albums:
        # Create album folder
        if not os.path.exists(album["ExportPath"]):
            os.makedirs(album["ExportPath"])
        # Loop over images and copy images
        for image in album["ImageList"]:
            name, extension = os.path.splitext(image)
            print("Copy " + image + " to " + album["ExportPath"])
            shutil.copy2(image, album["ExportPath"])

            # Code which could be used to convert raw images (not working)
            # if extension.lower() == ".cr2":
            #     print("Converting " + image + " to " + album["ExportPath"])
            #     raw_to_jpg(image, album["ExportPath"])
            # else:
            #     print("Copy " + image + " to " + album["ExportPath"])
            #     shutil.copy2(image, album["ExportPath"])

def replace_path(ImagePath, libary_path):
    image_path_original = os.path.normpath(ImagePath)
    path_from_iphoto_library = image_path_original.split("Bibliothek iPhoto")[1].strip("\\")
    photo_path_on_machine = os.path.join(libary_path, path_from_iphoto_library)
    return photo_path_on_machine

def convert_interval_to_datetime(interval):
    return datetime.datetime.fromtimestamp(interval + 978307200)

if __name__ == "__main__":

    # Set path of iPhoto/Aperture library
    libary_path = os.path.normpath("<iPhoto/Aperture Library>")

    # Set path to export to
    export_path = os.path.normpath("<Path for Export>")

    # Run main function
    main(libary_path, export_path)
