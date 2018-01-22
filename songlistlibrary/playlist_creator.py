from random import randint, choice
import xml.etree.ElementTree as ET
import os
import pickle
import logging
from shutil import copyfile

#logger for debugging
logging.basicConfig(level=logging.INFO, filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False

# create a file handler
#handler = logging.FileHandler('data.log','w')
#handler.setLevel(logging.DEBUG)
#logger.addHandler(handler)




def Load_Creator(path):
    root = ET.parse(path).getroot()

    playlistoptions = {}

    for options_element in root.findall('playlistoptions'):
        options = {}
        options['groups']=[]
        for group_element in options_element:
            group = {}
            group['numberofsongs']=int(group_element.attrib['numberofsongs'])
            group['priorityweights']=[]
            for priorityweight_element in group_element.find('priorityweights'):
                    group['priorityweights'].append(int(priorityweight_element.attrib['weight']))
            group['categories']=[]
            for category_element in group_element.findall('category'):
                group['categories'].append(category_element.attrib['name'])
            options['groups'].append(group)
        options_id=options_element.attrib['id']
        playlistoptions[options_id]=options

    return playlistoptions


"""
must be updated
def Create_Playlist(library, options):
    playlist = []
    for group in options['groups']:
        #join the categories togethers
        songs = []
        for category in group['categories']:
            songs.extend(library[category])
        #pick random songs by generating a random value based on the weights
        for num in range(group['numberofsongs']):
            selected_song = Get_Random_Song(songs, playlist)
            playlist.append(selected_song)

    return playlist

def Get_Random_Song(songs, playlist):
    weight_total = 0
    for song in songs:
        weight_total += song['weight']


    while True:
        random_number = randint(1,weight_total)
        current_weight_total = 0
        in_songlist = False
        for song in songs:
            current_weight_total += song['weight']
            if current_weight_total >= random_number:
                #check to make sure song is not already in playlist
                for playlist_song in playlist:
                    if playlist_song == song:
                        in_songlist = True
                if in_songlist == False:
                    return song
                else:
                    break
"""

def Create_Playlist_Repeats(library, options, repeat_dict):
    playlist = []
    for group in options['groups']:
        #join the categories togethers
        songs = []
        for category in group['categories']:
            songs.extend(library[category])
        #pick random songs by generating a random value based on the weights
        for num in range(group['numberofsongs']):
            selected_song = Get_Random_Song_Repeats(songs, playlist, repeat_dict, group['priorityweights'])
            repeat_dict[(selected_song['artist'], selected_song['songname'])] += 1
            playlist.append(selected_song)
    return playlist

"""
steps for picking a song
pick a priority that has at least one song not in playlist
get all songs with that priority
find the lowest number of repeats
create a list with the loweest number of repeats
pick a random song from that list
"""
def Get_Random_Song_Repeats(songs, playlist, repeat_dict, weights):
    logger.debug("----------------------------------------------------------\n\n\n\n")

    #pick a priority that has at least one song not in playlist
    weight_total = 0
    for weight in weights:
        weight_total += weight
    priority = None
    while priority == None:
        random_number = randint(1,weight_total)
        current_weight_total = 0
        logger.debug("Weight Total " + str(weight_total) + "\tRandom Number: " + str(random_number))
        for index in range(0, len(weights)):
            current_weight_total += weights[index]
            if current_weight_total >= random_number:
                logger.debug(index)
                logger.debug("songs with priority " + str(index) + "= " + str(list([(song["artist"],song["songname"],song["priority"])] for song in [song2 for song2 in songs if song2['priority'] == index])))
                logger.debug("current playlist= " + str(list([(song["artist"],song["songname"],song["priority"])] for song in playlist)))
                for song in songs:
                    if song['priority'] == index and song not in playlist:
                        priority = index
                        break
                break
    logger.debug(priority)

    #get all songs of the selected priority
    songs_with_same_priority = [song for song in songs if song['priority'] == priority]
    logger.debug("Songs With Same Priority = " + str([(song["artist"],song["songname"],song["priority"],repeat_dict[(song['artist'],song['songname'])]) for song in songs_with_same_priority]))

    #find lowest number of repeats
    lowest = repeat_dict[(songs_with_same_priority[0]['artist'],songs_with_same_priority[0]['songname'])]
    for song in songs_with_same_priority:
        if repeat_dict[(song['artist'],song['songname'])] < lowest:
            lowest = repeat_dict[(song['artist'],song['songname'])]
    logger.debug("Lowest repeat = " + str(lowest))

    #make a list containing lowest repeaters
    lowest_repeaters = [song for song in songs_with_same_priority if repeat_dict[(song['artist'],song['songname'])] == lowest]
    logger.debug("Lowest repeaters = " + str([(song["artist"],song["songname"],song["priority"],repeat_dict[(song['artist'],song['songname'])]) for song in lowest_repeaters]))

    selected_song = choice(lowest_repeaters)
    logger.debug("selected song = " + str(selected_song))
    return selected_song






    #get a random song not in current playlist
    """weight_total = 0
    for song in songs:
        weight_total += song['weight']
    logger.debug("Weight_Total1 = " + str(weight_total))
    selected_song = None
    while selected_song == None:
        random_number = randint(1,weight_total)
        logger.debug("Random Num 1 = " + str(random_number))
        current_weight_total = 0
        in_playlist = False
        for song in songs:
            current_weight_total += song['weight']
            if current_weight_total >= random_number:
                #check to make sure song is not already in playlist
                for playlist_song in playlist:
                    if playlist_song == song:
                        in_playlist = True
                if in_playlist == False:
                    selected_song = song
                    break

    logger.debug("Selected_Song = " + str(selected_song))

    #get all songs of same or higher repeat priority not on current playlist
    songs_with_same_priority = []
    for song in songs:
        if song[''] >= selected_song['']:
            if song not in playlist:
                songs_with_same_priority.append(song)
    logger.debug("Song With Same Priority = " + str([(song["artist"],song["songname"],song[""],repeat_dict[(song['artist'],song['songname'])]) for song in songs_with_same_priority]))

    #find lowest number of repeats
    lowest = repeat_dict[(selected_song['artist'],selected_song['songname'])]
    logger.debug("Lowest repeat = " + str(lowest))
    for song in songs_with_same_priority:
        if repeat_dict[(song['artist'],song['songname'])] < lowest:
            lowest = repeat_dict[(song['artist'],song['songname'])]
    logger.debug("Lowest repeat = " + str(lowest))
    #make a list containing lowest repeaters
    lowest_repeaters = [song for song in songs_with_same_priority if repeat_dict[(song['artist'],song['songname'])] == lowest]

    logger.debug("Lowest repeaters = " + str([(song["artist"],song["songname"],song[""],repeat_dict[(song['artist'],song['songname'])]) for song in lowest_repeaters]))
    #if the selected song is in the lowest_repeaters just pick it
    #else pick a random song from the lowest_repeaters
    if selected_song in lowest_repeaters:
        logger.debug("Selected song = " + str(selected_song))
        return selected_song

    weight_total = 0
    for song in lowest_repeaters:
        weight_total += song['weight']
    logger.debug("Weight total again = " + str(weight_total))
    random_number = randint(1,weight_total)
    logger.debug("Rand number 2 = " + str(random_number))
    current_weight_total = 0
    for song in lowest_repeaters:
        current_weight_total += song['weight']
        if current_weight_total >= random_number:
            logger.debug("Selected song = " + str(song))
            return song
    """

def Output_Playlist(playlist, output_directory):
    for song in playlist:
        copyfile(song['pathname'],os.path.join(output_directory,os.path.basename(song['pathname'])))




def Create_New_Repeat_Dict(library):
    repeat_dict = {}
    for category in library:
        for song in library[category]:
            repeat_dict[(song['artist'], song['songname'])] = 0
    return repeat_dict


def Update_Repeat_Dict(repeat_dict, library):
    new_repeat_dict = {}
    for category in library:
        for song in library[category]:
            if (song['artist'], song['songname']) in repeat_dict.keys():
                new_repeat_dict[(song['artist'], song['songname'])] = repeat_dict[(song['artist'], song['songname'])]
            else:
                new_repeat_dict[(song['artist'], song['songname'])] = 0
    return new_repeat_dict


def Save_Repeat_Dict(repeat_dict, path):
    with open(path, 'wb') as handle:
        pickle.dump(repeat_dict, handle)


def Open_Repeat_Dict(path):
    with open(path, 'rb') as handle:
        repeat_dict = pickle.load(handle)
        return repeat_dict
    return None



"""
old version of get random songs
def Get_Random_Song_Repeats(songs, playlist, repeat_dict):
    logger.debug("----------------------------------------------------------\n\n\n\n")
    #get a random song not in current playlist
    weight_total = 0
    for song in songs:
        weight_total += song['weight']
    logger.debug("Weight_Total1 = " + str(weight_total))
    selected_song = None
    while selected_song == None:
        random_number = randint(1,weight_total)
        logger.debug("Random Num 1 = " + str(random_number))
        current_weight_total = 0
        in_playlist = False
        for song in songs:
            current_weight_total += song['weight']
            if current_weight_total >= random_number:
                #check to make sure song is not already in playlist
                for playlist_song in playlist:
                    if playlist_song == song:
                        in_playlist = True
                if in_playlist == False:
                    selected_song = song
                    break

    logger.debug("Selected_Song = " + str(selected_song))

    #get all songs of same or higher repeat priority not on current playlist
    songs_with_same_priority = []
    for song in songs:
        if song[''] >= selected_song['']:
            if song not in playlist:
                songs_with_same_priority.append(song)
    logger.debug("Song With Same Priority = " + str([(song["artist"],song["songname"],song[""],repeat_dict[(song['artist'],song['songname'])]) for song in songs_with_same_priority]))

    #find lowest number of repeats
    lowest = repeat_dict[(selected_song['artist'],selected_song['songname'])]
    logger.debug("Lowest repeat = " + str(lowest))
    for song in songs_with_same_priority:
        if repeat_dict[(song['artist'],song['songname'])] < lowest:
            lowest = repeat_dict[(song['artist'],song['songname'])]
    logger.debug("Lowest repeat = " + str(lowest))
    #make a list containing lowest repeaters
    lowest_repeaters = [song for song in songs_with_same_priority if repeat_dict[(song['artist'],song['songname'])] == lowest]

    logger.debug("Lowest repeaters = " + str([(song["artist"],song["songname"],song[""],repeat_dict[(song['artist'],song['songname'])]) for song in lowest_repeaters]))
    #if the selected song is in the lowest_repeaters just pick it
    #else pick a random song from the lowest_repeaters
    if selected_song in lowest_repeaters:
        logger.debug("Selected song = " + str(selected_song))
        return selected_song

    weight_total = 0
    for song in lowest_repeaters:
        weight_total += song['weight']
    logger.debug("Weight total again = " + str(weight_total))
    random_number = randint(1,weight_total)
    logger.debug("Rand number 2 = " + str(random_number))
    current_weight_total = 0
    for song in lowest_repeaters:
        current_weight_total += song['weight']
        if current_weight_total >= random_number:
            logger.debug("Selected song = " + str(song))
            return song
"""


if __name__ == "__main__":
    pass
