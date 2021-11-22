import pypianoroll
import glob

def get_npz_data(n):
    ''''
    Load n number of npz files from all of the folders contained in the raw_data folder
    '''
    # get a list of the possible filepaths for the npz files
    files = glob.glob('raw_data/lpd_5/lpd_5_cleansed/**/**/**/**/*.npz')

    # Load n files from the dataset
    multitracks = [pypianoroll.load(fp) for fp in files[0:n]]
    return multitracks


def multitrack_to_midi(multitracks):
    '''
    Given a list of multitrack objects convert each of them into a midi file
    and save it on the raw_data folder
    '''
    for i in range(len(multitracks)):
        pypianoroll.write(f'raw_data/midi/track{i}.midi', multitracks[1])
    return 'midi files saved successfully'
