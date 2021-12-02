# Data analysis
- Document here the project: music-generator
- Description: Exploring datasets to try to generate some listenable music with deep learning
- Data Source: multiple sources
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

You can load the notes from the midi files using the `music21` package.

```py

midi = music21.converter.parse(file)

    notes_to_parse = None

    try: # file has instrument parts
        s2 = instrument.partitionByInstrument(midi)
        notes_to_parse = s2.parts.recurse()

    except: # file has notes in a flat structure
        notes_to_parse = midi.flat.notes

    for element in notes_to_parse:
      if isinstance(element, note.Note):
        notes.append(str(element.pitch))
      elif isinstance(element, chord.Chord):
        notes.append('.'.join(str(n) for n in element.normalOrder))
```
