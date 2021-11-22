# Data analysis
- Document here the project: music-generator
- Description: Project Description
- Data Source:
- Type of analysis:

Please document the project the better you can.

# Documentation

1. General articles :
    - https://towardsdatascience.com/creating-a-pop-music-generator-with-the-transformer-5867511b382a
    - https://towardsdatascience.com/how-to-generate-music-using-a-lstm-neural-network-in-keras-68786834d4c5
    - https://towardsdatascience.com/making-music-with-machine-learning-908ff1b57636
    - https://towardsdatascience.com/generating-music-using-deep-learning-cb5843a9d55e

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for music-generator in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/music-generator`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "music-generator"
git remote add origin git@github.com:{group}/music-generator.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
music-generator-run
```

# Install

Go to `https://github.com/{group}/music-generator` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/music-generator.git
cd music-generator
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
music-generator-run
```

# Loading Files

You can load npz files containing the Multitrack object for each song using `pypianoroll`.

```py
multitrack = pypianoroll.load('../raw_data/lpd_5/lpd_5_cleansed/B/B/D/TRBBDZW128F9300562/12b9eb224cc12c7afec94c9535f14b90.npz')
```

The Multitrack object has the following properties:

```
========== =========================== ================================== ==================================
Attribute  Description                 Type                               Default
========== =========================== ================================== ==================================
name       Name of the multitrack      str
resolution Time steps per quarter note int                                ``pypianoroll.DEFAULT_RESOLUTION``
tempo      Tempo at each time step     NumPy array of dtype float
downbeat   Downbeat positions          NumPy array of dtype bool
tracks     Music tracks                list of :class:`pypianoroll.Track` []
========== =========================== ================================== ==================================
```

The tempo contains an array with length equal to the amount of steps in the song. Its value represents the tempo of each step.

Each Track consists of:

```
========= ===================== =========== ===============================
Attribute Description           Type        Default
========= ===================== =========== ===============================
name      Name of the track     str
program   MIDI program number   int         ``pypianoroll.DEFAULT_PROGRAM``
is_drum   If it is a drum track bool        ``pypianoroll.DEFAULT_IS_DRUM``
pianoroll Downbeat positions    NumPy array ``np.zeros((0, 128))``
========= ===================== =========== ===============================
```

The pianoroll matrix has shape `(t, p)` where _t_ is the number of steps and _p_ the number of notes represented.
Each cell in the pianoroll matrix contains a number between 0 and 127 that represents the _velocity_.

Important: some tracks are stored as BinaryTracks and they're not relevant for the model we're trying to create.

New multitracks can be created to isolate specific tracks of existing songs with:

```py
m2 = pypianoroll.Multitrack(tempo=m1.tempo, tracks=[m1.tracks[1]])
```
