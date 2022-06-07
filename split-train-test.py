from argparse import ArgumentParser
from augment import load_labelfile, dump_labelfile
from numpy.random import choice


def main():
    parser = ArgumentParser()
    parser.add_argument("--train", dest="train", required=True, type=float)
    parser.add_argument("--test", dest="test", required=True, type=float)
    parser.add_argument("--validate", dest="validate", default=0, type=float)
    parser.add_argument("--labelfile", dest="labelfile", required=True)
    args = parser.parse_args()
    ratio = [args.train, args.test, args.validate]
    ratio = [r/sum(ratio) for r in ratio]

    labels = load_labelfile(args.labelfile)

    new_labels = dict(train={}, test={}, validate={})
    targets = list(new_labels.keys())
    for (filepath, label) in labels.items():
        target = targets[choice([0, 1, 2], p=ratio)]
        new_labels[target][filepath] = label

    for (target, labels_) in new_labels.items():
        print(target, len(labels_.keys()))
        labelfile = args.labelfile.replace('.txt', f'.{target}.txt')
        if len(labels_.keys()) == 0:
            continue
        with open(labelfile, 'w') as f:
            f.write(dump_labelfile(labels_))


if __name__ == "__main__":
    main()
 