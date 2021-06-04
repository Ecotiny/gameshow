import requests

API_ROOT = "https://gameshow.nsn.nz/api/"
VERIFY = True 

cmds = ['add', 'del']
scores = []

def add_party(partyname):
    data = {'party': partyname}
    r = requests.post(API_ROOT + '/party', json=data, verify=VERIFY)
    if r.json()['success']:
        return True
    else:
        return r.json()['error']

def del_party(partyname):
    data = {'party': partyname}
    r = requests.delete(API_ROOT + '/party', json=data, verify=VERIFY)
    if r.json()['success']:
        return True
    else:
        return r.json()['error']

def add_points(partyname, amount):
    currentscore = None
    try:
        currentscore = next(score for score in scores if score['partyname'] == partyname)
    except StopIteration:
        print(f"Party {partyname} doesn't exist")

    newscore = currentscore['score'] + amount
    data = {
        'party': partyname,
        'value': newscore
    }
    r = requests.put(API_ROOT + '/score', json=data, verify=VERIFY)
    print(r.content)
    if r.json()['success']:
        return True 
    else:
        return r.json()['error'] 

def del_points(partyname, amount):
    return add_points(partyname, -amount) 

def get_info():
    r = requests.get(API_ROOT + '/score', verify=VERIFY)
    return r.json()['scores']

def cli_parse(instr):
    args = instr.split(" ")
    cmd = args[0].strip().lower()
    if cmd not in cmds:
        print("Please enter a valid command (add/del)")
        return False

    if cmd == 'add':
        if args[1] == 'party':
            # add party
            add_party(args[2])
            print(f"Adding party {args[2]}")
            return True
        else:
            if len(args) == 3:
                # add args[2] points to party args[1]
                # example syntax 'add Aoraki 400'
                points = args[2]
                partyname = args[1]
                try:
                    points = int(points)
                except ValueError:
                    print("Please enter a valid number, e.g. add <partyname> 400")
                    return False

                print(f"Giving {points} points to {partyname}")
                add_points(partyname, points)
            else:
                print("Please enter a valid command (3 arguments expected)")
                return False

    elif cmd == 'del':
        if args[1] == 'party':
            # del party
            del_party(args[2])
            print(f"Deleting party {args[2]}")
        else:
            if len(args) == 3:
                points = args[2]
                partyname = args[1]
                try:
                    points = int(points)
                except ValueError:
                    print("Please enter a valid number, e.g. del <partyname> 400")
                    return False

                del_points(partyname, points)
                print(f"Giving -{points} points to {partyname}")
            else:
                print("Please enter a valid command (3 arguments expected)")
                return False

if __name__ == "__main__":
    scores = get_info()
    while True:
        instr = input("> ")
        if instr in ["exit",'q','quit']:
            break
        else:
            cli_parse(instr)

