import json 
import argparse
import tempfile
import os

def main(key, val):

    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    # storage_path = os.path.join('./', 'storage.data')

    if val is None:
        if os.path.isfile(storage_path):
            local_dict = json.load(open(storage_path))
            if key in local_dict.keys():
                print(*local_dict[key], sep=', ')
            else:
                print(' ')
        else:
            local_dict = {}
            local_dict.setdefault(key, [])
            with open(storage_path, 'w') as file:
                res = json.dump(local_dict, file)
            print(' ')

    else:
        if os.path.isfile(storage_path):
            local_dict = json.load(open(storage_path))
        else:
            local_dict = {}
        if key in local_dict.keys():
            local_dict[key].append(val)    
        else:
            local_dict.setdefault(key, [])
            local_dict[key].append(val)
        with open(storage_path, 'w') as file:
            res = json.dump(local_dict, file)
        # print(*local_dict[key], sep=' ')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='key value task')
    parser.add_argument('--key', default='key')
    parser.add_argument('--val')  
    

    args = parser.parse_args()

    main(args.key, args.val)
