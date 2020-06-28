from flask import Flask, request, render_template, redirect, session
import mysql.connector

mydb = mysql.connector.connect(
  host= 'localhost',
  user= 'root',
  password= 'anafen1996',
)

cursor = mydb.cursor()
cursor.execute("USE crud_db;")
mydb.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS listener(id INT AUTO_INCREMENT,\
                username VARCHAR(30) UNIQUE NOT NULL, email VARCHAR(30) UNIQUE NOT NULL,\
                PRIMARY KEY (id))")

cursor.execute("CREATE TABLE IF NOT EXISTS artist(id INT AUTO_INCREMENT,\
                name VARCHAR(30) NOT NULL, surname VARCHAR(30)  NOT NULL,\
                UNIQUE(name,surname),\
                PRIMARY KEY (id))")

cursor.execute("CREATE TABLE IF NOT EXISTS album(id INT AUTO_INCREMENT,\
                title VARCHAR(30) NOT NULL,\
                genre VARCHAR(30)  NOT NULL,\
                artistId INT NOT NULL,\
                FOREIGN KEY (artistId) REFERENCES artist(id),\
                PRIMARY KEY (id))")

cursor.execute("CREATE TABLE IF NOT EXISTS song(id INT AUTO_INCREMENT,\
                title VARCHAR(30) NOT NULL,\
                albumId INT NOT NULL,\
                FOREIGN KEY (albumId) REFERENCES album(id) ON DELETE CASCADE,\
                PRIMARY KEY (id))")

cursor.execute("CREATE TABLE IF NOT EXISTS like_song(id INT AUTO_INCREMENT,\
                likerId INT NOT NULL,\
                songId INT NOT NULL,\
                FOREIGN KEY (likerId) REFERENCES listener(id) ON DELETE CASCADE,\
                FOREIGN KEY (songId) REFERENCES song(id) ON DELETE CASCADE,\
                UNIQUE(likerId,songId),\
                PRIMARY KEY (id))")

cursor.execute("CREATE TABLE IF NOT EXISTS like_album(id INT AUTO_INCREMENT,\
                likerId INT NOT NULL,\
                albumId INT NOT NULL,\
                FOREIGN KEY (likerId) REFERENCES listener(id) ON DELETE CASCADE,\
                FOREIGN KEY (albumId) REFERENCES album(id) ON DELETE CASCADE,\
                UNIQUE(likerId,albumId),\
                PRIMARY KEY (id))")

cursor.execute("CREATE TABLE IF NOT EXISTS song_artist(id INT AUTO_INCREMENT,\
                songId INT NOT NULL,\
                artistId INT NOT NULL,\
                FOREIGN KEY (artistId) REFERENCES artist(id) ON DELETE CASCADE,\
                FOREIGN KEY (songId) REFERENCES song(id) ON DELETE CASCADE,\
                PRIMARY KEY (id))")

cursor.execute("DROP TRIGGER IF EXISTS crud_db.albumsong")

cursor.execute("CREATE TRIGGER albumsong BEFORE DELETE ON album FOR EACH ROW BEGIN DELETE FROM song WHERE albumId = old.id;END;")

cursor.execute("DROP TRIGGER IF EXISTS crud_db.albumlike")

cursor.execute("CREATE TRIGGER albumlike BEFORE INSERT ON like_album FOR EACH ROW BEGIN INSERT IGNORE INTO like_song (likerId,songId) SELECT NEW.likerId,id FROM song WHERE albumId = NEW.albumId;END;")

cursor.execute("DROP TRIGGER IF EXISTS crud_db.droplike")

cursor.execute("CREATE TRIGGER droplike AFTER DELETE ON song FOR EACH ROW BEGIN DELETE FROM like_song WHERE songId = old.id;END;")

cursor.execute("DROP PROCEDURE IF EXISTS crud_db.prc")

cursor.execute("CREATE PROCEDURE prc(IN artist_id INT ) BEGIN SELECT id,name,surname FROM artist WHERE id IN(SELECT DISTINCT artistId FROM song_artist WHERE songId IN (SELECT id FROM song WHERE albumId IN (SELECT albumId FROM song s INNER JOIN  album AS a ON a.id = s.albumId WHERE a.artistId = artist_id)) ) ORDER BY id;END;")

mydb.commit()

app = Flask(__name__)
app.secret_key = "hi"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/artist', methods=['GET', 'POST'])
def artist():
    if request.method == 'GET':
        cursor.execute("SELECT * FROM artist ORDER BY id;")
        artists = cursor.fetchall()
        return render_template('artist.html', artists = artists)

@app.route('/view-artist', methods=['GET', 'POST'])
def view_artist():
    if request.method == 'POST':
        form = request.form
        artist_id=form.get('artist_id')
        cursor.execute("SELECT * FROM album WHERE artistId = %s", (artist_id,))
        albums = cursor.fetchall()
        return render_template('view-albums.html', albums = albums, artist_id = artist_id)

@app.route('/view-contributors', methods=['GET', 'POST'])
def view_contributors():
    if request.method == 'POST':
        form = request.form
        artist_id=form.get('artist_id')
        cursor.execute("SELECT * FROM song INNER JOIN song_artist AS sa ON sa.songId = song.id WHERE sa.artistId = %s", (artist_id,))
        songs = cursor.fetchall()
        return render_template('view-contributors.html', songs = songs)

@app.route('/add-artists', methods=['GET', 'POST'])
def add_artists():
    if request.method == 'POST':
        form = request.form
        name = form.get('name')
        surname = form.get('surname')
        val = (name, surname)
        cursor.execute("INSERT INTO artist(name, surname) VALUES (%s, %s)", val)
        mydb.commit()
        return redirect('/artist') 

@app.route('/add-album', methods=['GET', 'POST'])
def add_albums():
    if request.method == 'POST':
        form = request.form
        album_id = form.get('id')
        album_title = form.get('title')
        album_genre = form.get('genre')
        artist_id = form.get('artist_id')
        val = (album_id, album_title, album_genre, artist_id)
        cursor.execute("INSERT INTO album(id, title, genre, artistId) VALUES (%s, %s, %s, %s)", val)
        mydb.commit()
        contributors = form.get('contributors')
        return render_template('add-album-songs.html', contributors = int(contributors),  album_id = album_id)

@app.route('/view-albums', methods=['GET', 'POST'])
def view_albums():
    if request.method == 'GET':
        cursor.execute("SELECT * FROM album;")
        albums = cursor.fetchall()
        return render_template('view-albums.html', albums = albums)        

@app.route('/edit-album-open', methods=['GET', 'POST'])
def edit_album_open():
    if request.method == 'POST':
        form = request.form
        album_id = form.get('album_id')
        artist_id = form.get('artist_id')
        return render_template('edit-album.html', album_id = album_id, artist_id = artist_id)

@app.route('/edit-album', methods=['GET', 'POST'])
def edit_album():
    if request.method == 'POST':
        form = request.form
        album_id = form.get('id')
        album_title = form.get('title')
        album_genre = form.get('genre')
        artist_id = form.get('artist_id')
        val = (album_title, album_genre, album_id)
        cursor.execute("UPDATE album SET title = %s, genre = %s WHERE id = %s ", val)
        mydb.commit()
        cursor.execute("SELECT * FROM album WHERE artistId = %s", (artist_id,))
        albums = cursor.fetchall()
        return render_template('view-albums.html', albums = albums, artist_id = artist_id)

@app.route('/delete-album', methods=['GET', 'POST'])
def delete_album():
    if request.method == 'POST':
        form = request.form
        album_id = form.get('album_id')
        artist_id = form.get('artist_id')
        cursor.execute("DELETE FROM album WHERE id = %s ", (album_id,))
        mydb.commit()
        cursor.execute("SELECT * FROM album WHERE artistId = %s", (artist_id,))
        albums = cursor.fetchall()
        return render_template('view-albums.html', albums = albums, artist_id = artist_id)

@app.route('/view-album-songs', methods=['GET', 'POST'])
def view_albums_song():
    if request.method == 'POST':
        form = request.form
        album_id=form.get('album_id')
        cursor.execute("SELECT * FROM song WHERE albumId = %s", (album_id, ))
        songs=cursor.fetchall()
        return render_template('view-album-songs.html', songs = songs, album_id = album_id)

@app.route('/add-album-songs-open', methods=['GET', 'POST'])
def add_album_songs_open():
    if request.method == 'POST':
        form = request.form
        contributors = form.get('contributors')
        album_id=form.get('album_id')
        return render_template('add-album-songs.html', contributors = int(contributors), album_id = album_id)

@app.route('/add-album-songs', methods=['GET', 'POST'])
def add_album_songs():
    if request.method == 'POST':
        form = request.form
        songId = form.get('id')
        title = form.get('title')
        album_id=form.get('album_id')
        val = (songId, title, album_id)
        cursor.execute("INSERT INTO song(id, title, albumId) VALUES (%s, %s, %s)", val)
        mydb.commit()
        contributors = int(form.get('contributors'))
        for i in range(contributors):
            name = form.get('contributor_name' + str(i))
            surname = form.get('contributor_surname' + str(i))
            cursor.execute("SELECT id FROM artist WHERE name = %s AND surname = %s", (name,surname, ))
            artist_id = cursor.fetchall()
            print(artist_id)
            artist_id = artist_id[0][0]
            val = (songId, artist_id)
            cursor.execute("INSERT INTO song_artist(songId, artistId) VALUES (%s, %s)", val)
        mydb.commit()
        cursor.execute("SELECT * FROM song WHERE albumId = %s", (album_id, ))
        songs=cursor.fetchall()
        return render_template('view-album-songs.html', songs = songs, album_id = album_id)

@app.route('/edit-album-songs-open', methods=['GET', 'POST'])
def edit_album_songs_open():
    if request.method == 'POST':
        form = request.form
        song_id = form.get('song_id')
        album_id=form.get('album_id')
        return render_template('edit-album-songs.html', song_id = song_id, album_id = album_id)

@app.route('/edit-album-songs', methods=['GET', 'POST'])
def edit_album_songs():
    if request.method == 'POST':
        form = request.form
        song_id = form.get('id')
        song_title = form.get('title')
        album_id=form.get('album_id')
        val = (song_title, song_id)
        cursor.execute("UPDATE song SET title = %s WHERE id = %s", val)
        mydb.commit()
        cursor.execute("SELECT * FROM song WHERE albumId = %s", (album_id, ))
        songs=cursor.fetchall()
        return render_template('view-album-songs.html', songs = songs, album_id = album_id)

@app.route('/delete-album-songs', methods=['GET', 'POST'])
def delete_album_songs():
    if request.method == 'POST':
        form = request.form
        song_id = form.get('song_id')
        album_id=form.get('album_id')
        cursor.execute("DELETE FROM song WHERE id = %s", (song_id,))
        mydb.commit()
        cursor.execute("SELECT * FROM song WHERE albumId = %s", (album_id, ))
        songs=cursor.fetchall()
        return render_template('view-album-songs.html', songs = songs, album_id = album_id)
    





@app.route('/listener', methods=['GET', 'POST'])
def listener():
    if request.method == 'GET':
        cursor.execute("SELECT * FROM listener;")
        listener = cursor.fetchall()
        return render_template('listener.html', listener = listener)

@app.route('/view-listener', methods=['GET', 'POST'])
def view_listener():
    if request.method == 'POST':
        form = request.form
        listener_id=form.get('listener_id')
        cursor.execute("SELECT * FROM album GROUP BY genre;")
        albums = cursor.fetchall()
        print(albums)
        return render_template('view-listener.html', listener_id = listener_id, albums = albums)

@app.route('/search-genre', methods=['GET', 'POST'])
def search_genre():
    if request.method == 'POST':
        form = request.form
        select=form.get('select')
        print(select)
        cursor.execute("SELECT * FROM song s INNER JOIN album AS a ON a.id = s.albumId WHERE a.genre = %s", (select, ))
        songs = cursor.fetchall()
        return render_template('view-genre.html', songs = songs)

@app.route('/search-song', methods=['GET', 'POST'])
def search_song():
    if request.method == 'POST':
        form = request.form
        title=form.get('title')
        query = "SELECT * FROM song WHERE title like %s"
        cursor.execute(query,("%" + title + "%",))
        songs = cursor.fetchall()
        print(songs)
        return render_template('view-songs.html', songs = songs)

@app.route('/add-listener', methods=['GET', 'POST'])
def add_listener():
    if request.method == 'POST':
        form = request.form
        username = form.get('username')
        email = form.get('e-mail')
        val = (username, email)
        cursor.execute("INSERT INTO listener(username, email) VALUES (%s, %s)", val)
        mydb.commit()
        return redirect('/listener')

@app.route('/rank-all-artists', methods=['GET', 'POST'])
def rank_all_artists():
    if request.method == 'POST':
        cursor.execute("SELECT ar.id, ar.name, ar.surname, COUNT(*) FROM like_song ls INNER JOIN song AS s ON ls.songId = s.id INNER JOIN album AS a ON a.id = s.albumId \
                        INNER JOIN artist AS ar ON ar.id = a.artistId GROUP BY ar.id ORDER BY COUNT(*) DESC;")
        artists = cursor.fetchall()
        return render_template('rank-all-artists.html', artists = artists) 

@app.route('/view-listener-artists', methods=['GET', 'POST'])
def view_listener_artists():
    if request.method == 'POST':
        form = request.form
        listener_id=form.get('listener_id')
        cursor.execute("SELECT * FROM artist ORDER BY id;")
        artists = cursor.fetchall()
        return render_template('view-listener-artists.html', artists = artists, listener_id = listener_id) 

@app.route('/view-produced-together', methods=['GET', 'POST'])
def view_produced_together():
    if request.method == 'POST':
        form = request.form
        artist_id=form.get('artist_id')
        qry = "CALL prc(%s)"
        data_qry = (artist_id,)
        cursor.execute(qry,data_qry)
        artists = cursor.fetchall()
        return render_template('view-produced-together.html', artists = artists) 

@app.route('/view-listener-popular-songs', methods=['GET', 'POST'])
def view_listener_popular_songs():
    if request.method == 'POST':
        form = request.form
        listener_id=form.get('listener_id')
        artist_id=form.get('artist_id')
        # cursor.execute("SELECT DISTINCT * FROM song s INNER JOIN like_song AS ls ON ls.songId = s.id INNER JOIN album AS a ON a.id = s.albumId WHERE a.artistId = %s", (artist_id,))
        cursor.execute("SELECT songId, s.title, COUNT(songId) as cnt FROM song s INNER JOIN like_song AS ls ON ls.songId = s.id INNER JOIN album AS a ON a.id = s.albumId WHERE a.artistId = %s GROUP BY songId ORDER BY cnt DESC", (artist_id,) )
        songs = cursor.fetchall()
        print(songs)
        return render_template('view-listener-popular-songs.html', songs = songs) 

@app.route('/view-listener-albums', methods=['GET', 'POST'])
def view_listener_albums():
    if request.method == 'POST':
        form = request.form
        artist_id=form.get('artist_id')
        listener_id=form.get('listener_id')
        #cursor.execute("SELECT * FROM album s INNER JOIN album as a on a.id = s.albumId WHERE a.artistId = %s", (artist_id,))
        cursor.execute("SELECT * FROM album WHERE artistId = %s", (artist_id,))
        albums = cursor.fetchall()
        return render_template('view-listener-albums.html', albums = albums, artist_id = artist_id, listener_id = listener_id)

@app.route('/view-listener-songs', methods=['GET', 'POST'])
def view_listener_songs():
    if request.method == 'POST':
        form = request.form
        album_id=form.get('album_id')
        listener_id=form.get('listener_id')
        cursor.execute("SELECT * FROM song WHERE albumId = %s", (album_id, ))
        songs=cursor.fetchall()
        return render_template('view-listener-songs.html', songs = songs, album_id = album_id, listener_id = listener_id)

@app.route('/like-listener-albums', methods=['GET', 'POST'])
def like_listener_albums():
    if request.method == 'POST':
        form = request.form
        listener_id=form.get('listener_id')
        album_id=form.get('album_id')
        artist_id=form.get('artist_id')
        cursor.execute("INSERT INTO like_album(likerId, albumId) VALUES (%s, %s)", (listener_id, album_id))
        mydb.commit()
        cursor.execute("SELECT * FROM album WHERE artistId = %s", (artist_id,))
        albums = cursor.fetchall()
        return render_template('view-listener-albums.html', albums = albums, artist_id = artist_id, listener_id = listener_id)

@app.route('/like-listener-songs', methods=['GET', 'POST'])
def like_listener_songs():
    if request.method == 'POST':
        form = request.form
        listener_id=form.get('listener_id')
        album_id=form.get('album_id')
        song_id=form.get('song_id')
        cursor.execute("INSERT INTO like_song(likerId, songId) VALUES (%s, %s)", (listener_id, song_id))
        mydb.commit()
        cursor.execute("SELECT * FROM song WHERE albumId = %s", (album_id, ))
        songs=cursor.fetchall()
        return render_template('view-listener-songs.html', songs = songs, album_id = album_id, listener_id = listener_id)

@app.route('/view-other-listeners', methods=['GET', 'POST'])
def view_other_listeners():
    if request.method == 'POST':
        form = request.form
        listener_id=form.get('listener_id')
        cursor.execute("SELECT * FROM listener WHERE NOT id = %s", (listener_id, ))
        listener = cursor.fetchall()
        return render_template('view-other-listeners.html', listener = listener)

@app.route('/view-liked-songs', methods=['GET', 'POST'])
def view_liked_songs():
    if request.method == 'POST':
        form = request.form
        listener_id=form.get('listener_id')
        cursor.execute("SELECT * FROM song s INNER JOIN like_song AS a ON a.songId = s.id WHERE a.likerId = %s", (listener_id,))
        songs = cursor.fetchall()
        return render_template('view-liked-songs.html', songs = songs)


if __name__ == "__main__":
    app.run(debug=True)
