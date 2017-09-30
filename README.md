# m3u2volumio
Translate .m3u files into a volumio playlist

# Usage
./m3u2volumio <filename.m3u>

# Example

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
