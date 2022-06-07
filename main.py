from ocr_datagen.gen import generate_image
from random import randint
from os.path import dirname, exists, join
from os import makedirs
from multiprocessing import Pool, Process, Manager


def random_split(corpus, min_l, max_l):
    current_index = 0
    while current_index < len(corpus):
        length = randint(min_l, max_l)
        yield ' '.join(corpus[current_index:(current_index+length)])
        current_index += length


def append_dataset(image_path, label_file, text):
    image_dir = dirname(image_path)
    makedirs(image_dir, exist_ok=True)

    image = generate_image(text)
    if image is None:
        return
    image.save(image_path)
    with open(label_file, "a", encoding='utf-8') as f:
        if exists(label_file):
            f.write("\n")
        f.write(f"{image_path}\t{text}")


def p_generate_image(queue, text):
    image = generate_image(text)
    if image is not None:
        queue.put((image, text))


def write_dataset(queue, label_file):
    first = True
    i = 0
    with open(label_file, "a", encoding='utf-8') as f:
        while True:
            index = str(i).rjust(9, '0')
            if first:
                f.write("\n")
            image, text = queue.get()
            image_path = join('img', f'{index}.png')
            image.save(image_path)
            f.write(f"{image_path}\t{text}")
            i = i + 1


def main(corpus, num_proc, max_records, max_words):
    manager = Manager()
    queue = manager.Queue()
    splits = list(random_split(corpus, 1, max_words))[:max_records]
    Process(target=write_dataset, args=(queue, 'label.txt')).start()
    with Pool(num_proc) as p:
        p.starmap(p_generate_image, [(queue, t) for t in splits])


if __name__ == "__main__":
    vocab = """aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ """
    with open("viwiki.txt", encoding="utf-8") as f:
        corpus_str = f.read()
        corpus_str = corpus_str.replace('\r', ' ')
        corpus_str = corpus_str.replace('\n', ' ')
        corpus_str = corpus_str.replace('  ', ' ')
        corpus = [c for c in corpus_str if c in vocab]
        corpus = corpus_str.split(' ')
        corpus = [c.strip() for c in corpus]
        corpus = [c for c in corpus if len(c) > 0]
    main(corpus, 11, 20000, max_words=3)

# for (i, split) in enumerate(random_split(corpus, 1, 7)):
#     index = str(i).rjust(6, '0')
#     image_path = join('output', f'{index}.png')
    # append_dataset(image_path, 'label.txt', split)
