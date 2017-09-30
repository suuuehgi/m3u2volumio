# m3u2volumio
Translate .m3u files into a volumio conform playlist. The intervention requires SSH.

# Dependencies

* `python3 >= 3.1`

# Usage
./m3u2volumio <filename.m3u>

Personal playlists lie in `/data/playlist/`.

The playlist *My Web Radios* is located at `/data/favourites/my-web-radio`.

# Assumptions

* Assuming proper formatting:
    * Weblinks contain `http://` or `https://`
    * [EXTINF](https://en.wikipedia.org/wiki/M3U#Extended_M3U) is structured:
        * `#EXTINF:length,Artist Name - Track Title` or
        * `#EXTINF:length,Title`
* Non-weblinks will be considered filelinks
* In regular (non-EXT) m3u:
    * If the filename contains a single '-', it will be considered as `artist - title` formatting
    * Otherwise the extention will be removed and the filename taken as title


# Example

## Webradio

**test.m3u**
```
#EXTM3U
#EXTINF:-1,RadioParadise -- 320k
http://stream-uk1.radioparadise.com/aac-320
#EXTINF:-1,OrganLive
http://play2.organlive.com:7000/320
#EXTINF:-1,KlassikRadio - Pure Bach
http://stream.klassikradio.de/purebach/mp3-192/stream.klassikradio.de/
```

Webradio playlist lies in `/data/favourites/my-web-radio`. Hence copy the following output into the file.

```
$ m3u2volumio test.m3u 
[{"service":"webradio","name":"RadioParadise -- 320k","uri":"http://stream-uk1.radioparadise.com/aac-320"},{"service":"webradio","name":"OrganLive","uri":"http://play2.organlive.com:7000/320"},{"service":"webradio","name":"KlassikRadio - Pure Bach","uri":"http://stream.klassikradio.de/purebach/mp3-192/stream.klassikradio.de/"}]
```

## Files

[**Example 3**](https://en.wikipedia.org/wiki/M3U#Examples)
```
#EXTM3U

#EXTINF:123, Sample artist - Sample title
Sample.mp3

#EXTINF:321,Example Artist - Example title
Greatest Hits\Example.ogg
```

Results in:

```
$ m3u2volumio example3.m3u
[{"service":"mpd","title":"Sample title","artist":"Sample artist","uri":"Sample.mp3"},{"service":"mpd","title":"Example title","artist":"Example Artist","uri":"Greatest Hits\Example.ogg"}]
```

Create new file `/data/playlist/playlistname` and copy the output there or directly by typing:

```
m3u2volumio filename.m3u | ssh volumio@volumiocomputer 'cat >> /data/playlist/newplaylistname'
```

[**Example 4**](https://en.wikipedia.org/wiki/M3U#Examples)

```
Alternative\Band - Song.mp3
Classical\Other Band - New Song.mp3
Stuff.mp3
D:\More Music\Foo.mp3
..\Other Music\Bar.mp3
http://emp.cx:8000/Listen.pls
http://www.example.com/~user/Mine.mp3
```

```
$ m3u2volumio example4.m3u
[{"service":"mpd","title":"Song","artist":"Band","uri":"Alternative/Band - Song.mp3"},{"service":"mpd","title":"New Song","artist":"Other Band","uri":"Classical/Other Band - New Song.mp3"},{"service":"mpd","title":"Stuff","uri":"Stuff.mp3"},{"service":"mpd","title":"Foo","uri":"D:/More Music/Foo.mp3"},{"service":"mpd","title":"Bar","uri":"../Other Music/Bar.mp3"},{"service":"webradio","name":"Listen.pls","uri":"http://emp.cx:8000/Listen.pls"},{"service":"webradio","name":"Mine.mp3","uri":"http://www.example.com/~user/Mine.mp3"}]
```
