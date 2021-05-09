import pandas as pd
import spotipy

#Allows to access spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="7dbc3e0b536a4dc8aff8f0e09a6a2014",
                                               client_secret="c3c5287f124d4621ae3383a3c307fad7",
                                               redirect_uri="https://www.google.com/",
                                               scope="user-library-read playlist-modify-public"))

def search(listnames,output):
    #dataset 
    d = {
    'artist': [], 
    'album': [], 
    'track': [], 
    'id': [], 
    'energy': [], 
    'liveness': [], 
    'tempo': [], 
    'speechiness': [], 
    'acousticness': [], 
    'instrumentalness': [], 
    'time_signature': [], 
    'danceability': [], 
    'key': [], 
    'duration_ms': [], 
    'loudness':[], 
    'valence': []
    }
    #list of columns name to create datatset
    columns = [
        'artist', 
        'album', 
        'track', 
        'id', 
        'energy', 
        'liveness', 
        'tempo', 
        'speechiness', 
        'acousticness', 
        'instrumentalness', 
        'time_signature', 
        'danceability', 
        'key', 
        'duration_ms', 
        'loudness', 
        'valence'
    ]

    artists = listnames

    for artist in artists:

        #Search artist in spotify
        results = sp.search(artist,1, 0, "artist")
        #Artist Name
        artist_name = artist

        #Get artist URI
        uri = results['artists']['items'][0]['uri'].encode('utf-8') 

        #Get albums using artist URI
        results = sp.artist_albums(uri,album_type = 'album', country='US', limit=1)
        albums = results['items']

        #Get all albums due to spotify count limit
        while results['next']:
            results = sp.next(results)
            albums.extend(results['items'])

        #Get singles using artist URI
        results = sp.artist_albums(uri,album_type = 'single', country='US', limit=1)
        singles = results['items']

        #Get all singles due to spotify count limit
        while results['next']:
            results = sp.next(results)
            singles.extend(results['items'])
        
        albums+=singles

        #Using album list look at each album
        for album in albums:
            #Avoids adding non explicit version as dupe
            if (album['name'] not in d['album']):
                #Album name
                album_name = album['name']
                #Album URI 
                uri = album['uri'].encode('utf-8')
                #Get all tracks using Album URI 
                results = sp.album_tracks(uri)
                tracks = results['items']

                #Using track list look at each track
                try:
                    for track in tracks:
                        #Song Name
                        song_name = track['name']
                        print(album_name+" - "+song_name+" - "+artist_name)
                        #Track URI
                        track_uri = track['id'].encode('utf-8')

                        #Get attributes of each song using track URI
                        attributes = sp.audio_features(track_uri)
            
                        #Add every info captured per song into database
                        d['track'].append(song_name)
                        d['id'].append(track_uri.encode('utf-8'))
                        d['artist'].append(artist_name)
                        d['album'].append(album_name)
                        d['energy'].append(attributes[0]["energy"])
                        d['liveness'].append(attributes[0]["liveness"])
                        d['tempo'].append(attributes[0]["tempo"])
                        d['speechiness'].append(attributes[0]["speechiness"])
                        d['acousticness'].append(attributes[0]["acousticness"])
                        d['instrumentalness'].append(attributes[0]["instrumentalness"])
                        d['time_signature'].append(attributes[0]["time_signature"])
                        d['danceability'].append(attributes[0]["danceability"])
                        d['key'].append(attributes[0]["key"])
                        d['duration_ms'].append(attributes[0]["duration_ms"])
                        d['loudness'].append(attributes[0]["loudness"])
                        d['valence'].append(attributes[0]["valence"])
                except TypeError:
                    print("attributes not foun")
 
    df = pd.DataFrame(d, columns = columns)
    df.to_csv(output, index = False)

names = ['Post Malone', 'The Weeknd', 'Roddy Ricch', 'DaBaby', 'Drake', 'Juice WRLD', 'Lil Baby', 'Harry Styles', 'Taylor Swift', 
'Pop Smoke', 'Billie Eilish', 'Dua Lipa', 'Luke Combs', 'Lil Uzi Vert', 'Justin Bieber', 'Lewis Capaldi', 'YoungBoy Never Broke Again', 
'BTS', 'Bad Bunny', 'Megan Thee Stallion', 'Rod Wave', 'Doja Cat', 'Travis Scott', 'Morgan Wallen', 'Lizzo', 'Future', 'Ariana Grande', 
'Eminem', 'Maroon 5', 'Young Thug', 'Kane Brown', 'Chris Brown', 'Jonas Brothers', 'Maren Morris', 'Halsey', 'Gunna', 'Elton John', 
'Tones And I', 'Polo G', 'Ed Sheeran', 'Selena Gomez', 'Camila Cabello', 'Gabby Barrett', 'Lady Gaga', 'Khalid', 'Lil Mosey', 'SAINt JHN', 
'Trevor Daniel', 'Jack Harlow', 'Jhene Aiko', 'Jason Aldean', 'Summer Walker', 'Blake Shelton', 'Arizona Zervas', 'Queen', 'Cardi B', 
'A Boogie Wit da Hoodie', 'Dan + Shay', 'blackbear', 'Sam Hunt', 'Trippie Redd', 'Mustard', 'Lil Nas X', 'Moneybagg Yo', 'Mac Miller', 
'XXXTENTACION', 'Shawn Mendes', 'JACKBOYS', 'The Beatles', 'Celine Dion', 'Don Toliver', 'YNW Melly', 'Old Dominion', 'Luke Bryan', 
'Lil Durk', 'Fleetwood Mac', 'Thomas Rhett', 'Tory Lanez', 'NF', 'Kendrick Lamar', 'Mariah Carey', 'NLE Choppa', 'Lil Wayne', 'Lee Brice', 
'Eagles', 'U2', 'Surfaces', 'Trans-Siberian Orchestra', 'Lil Tecca', 'Lil Tjay', 'Jon Pardi', 'Miranda Lambert', 'Chris Stapleton', 'Michael Jackson', 
'SHAED', 'Marshmello', 'H.E.R.', 'Sam Smith', 'Kenny Chesney', 'Maddie & Tae', 'Panic! At The Disco', 'Meek Mill', 'P!nk', 'J. Cole', 'Imagine Dragons', 
'Kodak Black', '21 Savage', 'Swae Lee', 'The Rolling Stones', '5 Seconds Of Summer', 'Lauren Daigle', 'Metallica', 'Bruno Mars', 'Ella Mai', 'Bradley Cooper', 
'Michael Buble', 'Ava Max', 'Normani', 'Florida Georgia Line', 'twenty one pilots', 'Billy Ray Cyrus', 'Bastille', 'Offset', 'Tyler, The Creator', 'City Girls', 
'Blueface', 'Carrie Underwood', 'Kanye West', 'DJ Khaled', 'Billy Joel', 'Backstreet Boys', 'Paul McCartney', 'Bazzi', '6ix9ine', 'Sheck Wes', 'Migos', 
'Nipsey Hussle', 'Eric Church', 'benny blanco', 'Justin Timberlake', 'Nicki Minaj', 'Demi Lovato', 'Bebe Rexha', 'G-Eazy', 'Beyonce', 'Lil Pump', 'Logic', 
'JAY-Z', 'SZA', 'Charlie Puth', 'Rich The Kid', 'J Balvin', 'Ozuna', 'Brett Young', 'Childish Gambino', 'Portugal. The Man', 'Lil Skies', 'EXO', 'BlocBoy JB', 
'Lauv', 'Keith Urban', 'Metro Boomin', 'Pentatonix', 'Rihanna', 'The Carters', 'Ty Dolla $ign', 'Gucci Mane', 'Journey', 'Foo Fighters', 'The Chainsmokers', 
'Coldplay', 'Guns N Roses', 'Alessia Cara', 'Niall Horan', 'Rae Sremmurd', 'Big Sean', 'James Arthur', 'Adele', 'Katy Perry', 'Depeche Mode', 'Luis Fonsi', 
'Maluma', 'Miley Cyrus', 'French Montana', 'Daddy Yankee', 'Liam Payne', 'Calvin Harris', 'Zayn', 'Julia Michaels', 'Linkin Park', 'Chance The Rapper', 
'Bryson Tiller', 'Quavo', 'Red Hot Chili Peppers', 'Tom Petty And The Heartbreakers', 'Roger Waters', 'Playboi Carti', 'John Mayer', '2 Chainz', 'Zac Brown Band', 
'Kesha', 'Sia', 'Zedd', 'Bruce Springsteen', 'Meghan Trainor', 'Prince', 'Desiigner', 'Fetty Wap', 'One Direction', 'Fifth Harmony', 'Lukas Graham', 'Flo Rida', 
'Kevin Gates', 'DNCE', 'Mike Posner', 'Daya', 'Madonna', 'Major Lazer', 'Ellie Goulding', 'DJ Snake', 'James Bay', 'Troye Sivan', 'Jeremih', 'Wiz Khalifa', 
'X Ambassadors', 'Britney Spears', 'Elle King', 'Cole Swindell', 'David Bowie', 'Kiiara', 'Tim McGraw', 'Dierks Bentley', 'Disturbed', 'Jennifer Lopez', 
'Nick Jonas', 'gnash', 'D.R.A.M.', 'Mark Ronson', 'WALK THE MOON', 'Hozier', 'Fall Out Boy', 'Jason Derulo', 'Silento', 'OMI', 'Tove Lo', 'Rachel Platten', 
'Andy Grammer', 'Pitbull', 'David Guetta', 'Iggy Azalea', 'Little Big Town', 'Trey Songz', 'Shania Twain', 'AC/DC', 'Omarion', 'Ne-Yo', 'Vance Joy', 'Kid Ink', 
'Rich Homie Quan', 'Neil Diamond', 'Mumford & Sons', 'Lana Del Rey', 'A$AP Rocky', 'Usher', 'Grateful Dead', 'Garth Brooks', 'Kelly Clarkson', 'T-Wayne', 
'Enrique Iglesias', 'Pharrell Williams', 'Lorde', 'John Legend', 'OneRepublic', 'Avicii', 'MAGIC!', 'Charli XCX', 'Nico & Vinz', 'Shakira', 'Passenger', 
'Brantley Gilbert', 'Idina Menzel', 'Lady A', 'YG', 'American Authors', 'Juicy J', 'ScHoolboy Q', 'George Strait', 'Paramore', 'Austin Mahone', 'Snoop Dogg', 
'Aloe Blacc', 'Martin Garrix', 'Disclosure', 'Romeo Santos', 'A Great Big World', 'Lil Jon', 'Arctic Monkeys', 'Cher', 'Becky G', 'Bob Marley And The Wailers', 
'Rascal Flatts', 'MKTO', 'Sara Bareilles', 'Christina Aguilera', 'Macklemore & Ryan Lewis', 'Robin Thicke', 'The Lumineers', 'Baauer', 'Phillip Phillips', 
'Bon Jovi', 'Daft Punk', 'Hunter Hayes', 'Alicia Keys', 'fun.', 'PSY', 'Ke$ha', 'will.i.am', 'The Band Perry', 'Miguel', 'Darius Rucker', 'Anna Kendrick', 
'AWOLNATION', 'T.I.', 'Capital Cities', 'Of Monsters And Men', 'Rod Stewart', 'Swedish House Mafia', 'Wanz', 'Avril Lavigne', 'Brad Paisley', 'Wale', 'Muse', 
'Randy Houser', 'Icona Pop', 'LMFAO', 'Carly Rae Jepsen', 'Gotye', 'Whitney Houston', 'The Wanted', 'Skrillex', 'Toby Keith', 'Train', 'Tyga', 'The Black Keys',
'Selena Gomez & The Scene', 'Jason Mraz', 'Nickelback', 'Florence + The Machine', 'Gym Class Heroes', 'Foster The People', 'Neon Trees', 'Lionel Richie', 
'Jessie J', 'Van Halen', 'Alex Clare', 'Dave Matthews Band', 'Young Jeezy', 'Kimbra', 'Rick Ross', 'Mary J. Blige', 'Kip Moore', 'B.o.B', 'Andrea Bocelli', 
'Scotty McCreery', 'Gavin DeGraw', 'Glee Cast', 'The Black Eyed Peas', 'CeeLo Green', 'Take That', 'Susan Boyle', 'Akon', 'Lupe Fiasco', 'Nelly', 'Sugarland',
'Keri Hilson', '50 Cent', 'Bad Meets Evil', 'The Script', 'Kid Rock', 'Taio Cruz', 'Don Omar', 'Josh Groban', 'Waka Flocka Flame', 'Ludacris', 'Hot Chelle Rae', 
'Thompson Square', 'Far*East Movement', 'Christina Perri', 'Kelly Rowland', 'Diddy - Dirty Money', 'Chris Young', 'Billy Currington', 'Dr. Dre', 'Adam Lambert', 
'Young Money', 'Iyaz', 'Owl City', 'Jay Sean', 'Timbaland', 'Sade', 'Kings Of Leon', 'Daughtry', 'Kris Allen', 'La Roux', 'Travie McCoy', 'Monica', 
'Casting Crowns', 'Josh Turner', 'Colbie Caillat', '3OH!3', 'Jack Johnson', 'Orianthi', 'Easton Corbin', 'Norah Jones', 'Reba McEntire', 'Hayley Williams',
'Shinedown', 'Melanie Fiona', 'Shontelle', 'The Fray', 'Jamie Foxx', 'The All-American Rejects', 'Soulja Boy', 'David Cook', 'T-Pain', 'Green Day',
'Kid Cudi', 'Maxwell', 'Leona Lewis', 'Jordin Sparks', 'Fergie', 'Natasha Bedingfield', 'Keyshia Cole', 'Plies', 'The-Dream', 'Sean Kingston', 'Finger Eleven',
'Gwen Stefani', 'Nelly Furtado', 'Ciara', 'Hinder', 'Plain White Ts', 'Mims', 'Lloyd', 'Unk', 'Shop Boyz', 'My Chemical Romance', 'Amy Winehouse', 
'Bow Wow', 'R. Kelly', 'Sean Paul', 'The Pussycat Dolls', 'James Blunt', 'Daniel Powter', 'Gnarls Barkley', 'Yung Joc', 'Chamillionaire', 'Cassie', 
'Dem Franchize Boyz', 'KT Tunstall', 'Snow Patrol', 'D4L', 'Juelz Santana']