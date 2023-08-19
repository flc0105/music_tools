import os
from mutagen import File

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.flac')]

for file in files:
    flac = File(file)
    tags = flac.tags
    tags['ALBUM']       = tags['ALBUM']
    tags['TITLE']       = tags['TITLE']
    tags['TRACKNUMBER'] = tags['TRACKNUMBER']
    tags['TRACKTOTAL']  = tags['TRACKTOTAL']
    tags['DISCNUMBER']  = tags['DISCNUMBER']
    tags['DISCTOTAL']   = tags['DISCTOTAL']  
    tags['DATE']        = tags['DATE']       
    tags['GROUPING']    = tags['GROUPING']   
    tags['COPYRIGHT']   = tags['COPYRIGHT']  
    tags['GENRE']       = tags['GENRE']      
    tags['ALBUMARTIST'] = tags['ALBUMARTIST']
    tags['ARTIST']      = tags['ARTIST']     
    tags['DESCRIPTION'] = tags['DESCRIPTION']
    flac.pop('LYRICS')
    flac.save()
