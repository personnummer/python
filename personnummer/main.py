import argparse

from personnummer import personnummer
from personnummer.personnummer import PersonnummerException

def setup_args():
    ap = argparse.ArgumentParser('personnummer')
    ap.add_argument('pnr')
    return ap


def main():
    ap = setup_args()
    args = ap.parse_args()
    if args.pnr:
        try:
            pn = personnummer.Personnummer(args.pnr)
            
            print(f'Age: {pn.get_age()}')
            sex = 'female'
            if pn.is_male():
                sex = 'male'
            print(f'Sex: {sex}')

        except PersonnummerException:
            print('Not a valid Swedish personnummer')
            

