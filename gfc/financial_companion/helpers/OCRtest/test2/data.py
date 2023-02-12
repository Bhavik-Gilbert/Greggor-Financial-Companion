import stow
import tarfile
from tqdm import tqdm
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

def download_and_unzip(url, extract_to='Datasets', chunck_size=1024*1024):
    http_response = urlopen(url)

    data = b''

    iterations = http_response.length // chunck_size +1
    for _ in tqdm(range(iterations)):
        data += http_response.read(chunck_size)

    zipfile = ZipFile(BytesIO(data))
    zipfile.extractall(path=extract_to)

dataset_path = stow.join('Datasets', 'IAM_Words')
if not stow.exists(dataset_path):
    download_and_unzip('https://git.io/J0fjL', extract_to='Datasets')

    file = tarfile.open(stow.join(dataset_path, "words.tgz"))
    file.extractall(stow.join(dataset_path, "words"))