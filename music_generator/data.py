import pypianoroll
import glob


def get_npz_data(n, data_path='raw_data/lpd_5/lpd_5_cleansed'):
    ''''
    Load n number of npz files from all of the folders contained in the raw_data folder
    '''
    # get a list of the possible filepaths for the npz files
    files = glob.glob(f'{data_path}/**/**/**/**/*.npz')

    # Load n files from the dataset
    multitracks = [pypianoroll.load(fp) for fp in files[0:n]]
    return multitracks


def multitrack_to_midi(multitracks, save_path='raw_data/midi'):
    '''
    Given a list of multitrack objects convert each of them into a midi file
    and save it on the raw_data folder
    '''
    for i in range(len(multitracks)):
        pypianoroll.write(f'{save_path}/track{i}.midi', multitracks[i])
    return 'midi files saved successfully'
