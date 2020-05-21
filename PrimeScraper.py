import os
import requests
from zipfile import ZipFile


def main(redownload=False):
    zips_range = (1, 50 + 1)
    if redownload:
        refetch = range(*zips_range)
    else:
        refetch = []
        for i in range(*zips_range):
            filename = "./primezips/" + str(i) + ".zip"
            if not os.path.isfile(filename) or os.stat(filename).st_size < 1500:
                refetch.append(i)
    download_prime_zips(portion=refetch)
    unzip_primes(portion=range(*zips_range))
    print("Done!")


def download_prime_zips(save_path="./primezips/", portion=range(1, 50 + 1)):
    for i in portion:
        url = r"https://primes.utm.edu/lists/small/millions/primes" + str(i) + ".zip"
        try:
            r = requests.get(url, stream=True, verify=False)
        except requests.exceptions.MissingSchema:
            print("The supplied URL is invalid. Please update and run again.")
            raise Exception("InvalidURL")
        with open(save_path + str(i) + ".zip", "wb") as f:
            f.write(r.content)


def unzip_primes(portion=range(1, 50 + 1)):
    old_path = "./primezips/"
    new_path = "./primetables/"
    for i in portion:
        with ZipFile(old_path + str(i) + ".zip") as zfile:
            zfile.extract("primes" + str(i) + ".txt", path=new_path)


if __name__ == "__main__":
    main(redownload=False)
