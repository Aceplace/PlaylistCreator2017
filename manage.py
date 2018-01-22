import sys
import os
from songlistlibrary.playlist_creator import *
from songlistlibrary.songlist_library import *

#type in the directories here and then run the script
#library_directory = r"C:\Users\Mike\Dropbox\FB\PlaylistCreator\tests"
#library_path = r"C:\Users\Mike\Dropbox\FB\PlaylistCreator\tests\testlibrary.xml"
#creator_options = r"C:\Users\Mike\Dropbox\FB\PlaylistCreator\tests\creatoroptions.xml"
#repeat_data = r"C:\Users\Mike\Dropbox\FB\PlaylistCreator\tests\repeatlist.dat"
#output_directory = r"C:\Users\Mike\Dropbox\FB\PlaylistCreator\output"

library_directory = r"C:\Users\Mike\Documents\Football\Judge\2017\JudgePlaylists2017\Library"
library_path = r"C:\Users\Mike\Documents\Football\Judge\2017\JudgePlaylists2017\Library\judgesonglibrary.xml"
creator_options = r"C:\Users\Mike\Documents\Football\Judge\2017\JudgePlaylists2017\Library\creatoroptions.xml"
repeat_data = r"C:\Users\Mike\Documents\Football\Judge\2017\JudgePlaylists2017\Library\repeatlist.dat"
output_directory = r"C:\Users\Mike\Documents\Football\Judge\2017\JudgePlaylists2017\output"

if sys.argv[1] == "createlibrary":
    print("library directory\t\t", library_directory)
    print("library output\t\t", os.path.join(library_directory, library_path))
    print("repeat file\t\t",os.path.join(repeat_data))
    Create_Library_From_Directory(library_directory, os.path.join(library_directory, library_path), sys.argv[2])
    Save_Repeat_Dict(Create_New_Repeat_Dict(Load_Library(library_path)), repeat_data)
    print("library created!")

if sys.argv[1] == "updatelibrary":
    Update_Library(library_directory, os.path.join(library_directory, library_path))
    Save_Repeat_Dict(Update_Repeat_Dict(Open_Repeat_Dict(repeat_data),Load_Library(library_path)), repeat_data)
    print("library updated!")


if sys.argv[1] == "createplaylist":
    library = Load_Library(library_path)
    options = Load_Creator(creator_options)[sys.argv[2]]
    repeatlist = Open_Repeat_Dict(repeat_data)
    playlist = Create_Playlist_Repeats(library, options, repeatlist)
    Output_Playlist(playlist, output_directory)
    Save_Repeat_Dict(repeatlist,repeat_data)
    print("playlist created in \t\t",output_directory)


if sys.argv[1] == "resetrepeatdata":
    Save_Repeat_Dict(Create_New_Repeat_Dict(Load_Library(library_path)), repeat_data)
    print("repeat data reset")

if sys.argv[1] == "viewrepeatdata":
    library = Load_Library(library_path)
    repeatlist = Open_Repeat_Dict(repeat_data)

    #print out results
    f = open(os.path.join(output_directory,"repeatlistdata.txt"),'w')
    #for key in repeatlist.keys():
    #    f.write(str(key) + " " + str(repeatlist[key]) + "\n")
    #f.close()
    #print("library test in created in librarytest.txt")

    for category in library.keys():
        f.write(category + "\n----------------------------\n\n")
        for song in library[category]:
            f.write(song['artist'] + ' ' + song['songname'] + ' ' + str(repeatlist[(song['artist'],song['songname'])]) + '\n')
        f.write('\n\n\n')
    f.close()
    print("repeatlist data created in " + str(os.path.join(output_directory,"repeatlistdata.txt")))

if sys.argv[1] == "testlibrary":
    library = Load_Library(library_path)
    options = Load_Creator(creator_options)[sys.argv[2]]
    repeatlist = Create_New_Repeat_Dict(Load_Library(library_path))

    for num in range(int(sys.argv[3])):
        playlist = Create_Playlist_Repeats(library, options, repeatlist)
        print("Playlist ",num," / ",sys.argv[3],"created")

    #print out results
    f = open(os.path.join(output_directory,"librarytest.txt"),'w')
    #for key in repeatlist.keys():
    #    f.write(str(key) + " " + str(repeatlist[key]) + "\n")
    #f.close()
    #print("library test in created in librarytest.txt")

    for category in library.keys():
        f.write(category + "\n----------------------------\n\n")
        for song in library[category]:
            f.write(song['artist'] + ' ' + song['songname'] + ' ' + str(repeatlist[(song['artist'],song['songname'])]) + '\n')
        f.write('\n\n\n')
    f.close()
    print("library test in created in " + str(os.path.join(output_directory,"librarytest.txt")))
