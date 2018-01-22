import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
from mutagen.mp3 import MP3

def Load_Library(path):
    root = ET.parse(path).getroot()

    library = {}

    #create dictionary entry for each category
    #each category consists of a list of songs containing info about the song
    for category in root.findall('category'):
        song_list = []
        for song in category:
            song_dict = {}
            song_dict['artist']=song.attrib['artist']
            song_dict['length']=float(song.attrib['length'])
            song_dict['pathname']=song.attrib['pathname']
            song_dict['priority']=int(song.attrib['priority'])
            song_dict['songname']=song.attrib['songname']
            #song_dict['weight']=int(song.attrib['weight'])
            song_list.append(song_dict)
        library[category.attrib['name']]=song_list

    return library


def Create_Library_From_Directory(directory, output, default_priority=0):
    subdirectories = next(os.walk(directory))[1]

    #constructing a tree from scratch
    tree = ET.ElementTree()
    root = ET.Element('songlistlibrary')
    tree._setroot(root)

    #enter each sub directory and add mp3 files to category playlists
    for subdirectory in subdirectories:
        category = subdirectory
        #each subdirectory will automatically be considered a category
        category_element = ET.Element('category', {'name':category})
        current_directory = os.path.abspath(os.path.join(directory,subdirectory))
        file_names = next(os.walk(os.path.abspath(os.path.join(directory,subdirectory))))[2]

        for file_name in file_names:
            if os.path.splitext(file_name)[1] == ".mp3":
                artist = file_name.split('-')[0].strip()
                song_name = file_name.split('-')[1].split('.')[0].strip()
                path_name = os.path.join(current_directory, file_name)
                audio = MP3(os.path.join(current_directory, file_name))
                song_length = str(audio.info.length)
                ET.SubElement(category_element, "song", attrib={'artist':artist, 'songname':song_name, 'pathname':path_name, 'priority':str(default_priority), 'length':song_length})
        root.append(category_element)

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open(output, "w") as f:
        f.write(xmlstr)
    #tree.write(output, encoding="UTF-8", xml_declaration=True)

def Update_Library(directory, library_path):
    subdirectories = next(os.walk(directory))[1]

    #constructing a new tree from scratch
    tree = ET.ElementTree()
    root = ET.Element('songlistlibrary')
    tree._setroot(root)

    for subdirectory in subdirectories:
        category = subdirectory
        #each subdirectory will automatically be considered a category
        category_element = ET.Element('category', {'name':category})
        current_directory = os.path.abspath(os.path.join(directory,subdirectory))
        file_names = next(os.walk(os.path.abspath(os.path.join(directory,subdirectory))))[2]

        for file_name in file_names:
            if os.path.splitext(file_name)[1] == ".mp3":
                artist = file_name.split('-')[0].strip()
                song_name = file_name.split('-')[1].split('.')[0].strip()
                path_name = os.path.join(current_directory, file_name)
                audio = MP3(os.path.join(current_directory, file_name))
                song_length = str(audio.info.length)
                ET.SubElement(category_element, "song", attrib={'artist':artist, 'songname':song_name, 'pathname':path_name, 'priority':'0', 'length':song_length})
        root.append(category_element)

    #open up old tree and copy song attributes from old tree into new tree
    old_tree = ET.parse(library_path)
    old_root = old_tree.getroot()
    for old_song in old_root.findall(".//song"):
        #get old song info
        artist=old_song.attrib['artist']
        length=old_song.attrib['length']
        pathname=old_song.attrib['pathname']
        priority=old_song.attrib['priority']
        songname=old_song.attrib['songname']
        #weight=old_song.attrib['weight']

        #find song in new library with same artistname and songname...update it
        song_query_str = './/song[@songname="' + songname + '"][@artist="' + artist + '"]'
        new_song_element = root.find(song_query_str)
        if new_song_element != None:
            new_song_element.set('length', length)
            new_song_element.set('priority', priority)
            #new_song_element.set('weight', weight)

    old_tree.write(library_path+'(old)', encoding="UTF-8", xml_declaration=True)

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ",encoding="UTF-8")
    with open(library_path, "wb") as f:
        f.write(xmlstr)




if __name__ == "__main__":
    pass
