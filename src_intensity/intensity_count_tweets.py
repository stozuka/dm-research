import glob


def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_files = glob.glob(base_path + 'data_intensity/sep_intensity/new_method/*')
    out_file = base_path + 'data_intensity/sep_intensity_count/count'
    return in_files, out_file

def count_tweets(in_file):
    count = 0
    with open(in_file, 'r') as f:
        for line in f:
            count +=1
    return count

def create_out_file(result, out_file):
    with open(out_file, 'w+') as f:
        for intensity, count in result.items():
            f.write(intensity + '\n')
            f.write(str(count) + '\n\n')

def sep_intensity():
    in_files, out_file = get_files()
    result = {}
    for in_file in in_files:
        intensity = in_file.split('/')[-1]
        count = count_tweets(in_file)
        result[intensity] = count
    create_out_file(result, out_file)

if __name__ == '__main__':
    sep_intensity()
