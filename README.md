pyClickTrack
============

pyClickTrack is, as the name suggests, a python program to generate click tracks. A click track is commonly used by musicians to navigate and time the beat of any given song. Click tracks can be crucial in helping to keep the timing or *tightness* right when recording live or via a [DAW](http://en.wikipedia.org/wiki/Digital_audio_workstation "Digital Audio Workstation").

pyClickTrack uses [YAML](http://yaml.org/ "YAML.org") (an easy to read plain text configuration file format) as input and standard WAVE (.wav) files as output - if ffmpeg or libav is present on the system pyClickTrack will unlock a very large range of output formats as it relies on [pyDub](https://github.com/jiaaro/pydub) as audio processing library.

Quick start
-----------

See if stuff works:

### Linux (bash-like)
``
cd <path/to/pyClickTrack>
python ./pyClickTrack.py Test.ct
``

### Windows (cmd)
``
cd <path/to/pyClickTrack>
python ./pyClickTrack.py Test.ct
``

The above should create a file named *Test.wav* in the current directory.

