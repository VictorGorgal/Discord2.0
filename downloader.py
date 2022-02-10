from requests import get
from multiprocessing import Process
from os.path import exists

# single-thread: 5.8s avg.
# multi-process: 3.3s avg.


def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


def process_thread(*urls, size=64):
    for name, url in urls:
        if not exists(f'./images/{name}.png'):
            img = get(url.replace('size=1024', f'size={size}')).content
            with open(f'images/{name}.png', 'wb') as file:
                file.write(img)


def main(urls, processes_count=30, img_size=64):
    urls = chunkify(urls, processes_count)

    processes = []
    for lis in urls:
        p = Process(target=process_thread, args=lis, kwargs={'size': img_size})
        p.start()
        processes.append(p)

    for process in processes:
        process.join()


if __name__ == '__main__':
    main([['fuguetero', 'https://cdn.discordapp.com/avatars/273534659646717973/80bbe533f3ed5cae086638e69ecad651.webp?size=1024']], processes_count=1, img_size=32)
