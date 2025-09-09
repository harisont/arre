import argparse

def subdict(sub):
    [_, time, text] = sub.split("\n")
    simpletext = text.replace('<font color="#00ff00">', '').replace('</font>', '')
    [start,end] = time.split(' --> ')
    return {"text": simpletext, "start": start, "end": end}

def time2int(str):
    return int("".join([char for char in str if char.isdigit()]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remove word alignments from .srt files."
    )
    parser.add_argument("path", help="path to word-aligned .srt file")
    
    args = parser.parse_args()
    with open(args.path) as handle:
        subs = handle.read().split("\n\n")

    subdicts = [subdict(sub) for sub in subs]

    simplesubs = []
    for subdict in subdicts:
        samedicts = [samedict for samedict in subdicts if subdict["text"] == samedict["text"]]
        subdict["end"] = max(samedicts, key=lambda samedict: time2int(samedict["end"]))["end"]
        simplesubs.append(subdict)
        for samedict in samedicts:
            subdicts.remove(samedict)

    for (i,subdict) in enumerate(simplesubs):
        print(i)
        print('{} --> {}'.format(subdict["start"], subdict["end"]))
        print(subdict["text"])
        print()