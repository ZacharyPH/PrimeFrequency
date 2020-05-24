import os
import requests
from zipfile import ZipFile


class PrimeNumbers:
    # TODO: Implement this with each of the below functions, as well as a new function that returns an arbitrary number
    #       of primes numbers in a list. Potentially, this function could instead return a generator (yield)
    pass


def main(refresh=False):
    zips_range = range(1, 50 + 1)

    refetch = get_reloads("./prime_zips/", extension="zip", min_size=1500) if not refresh else zips_range
    download_prime_zips(portion=refetch)
    unzip = get_reloads("./prime_tables/", extension="txt", min_size=10 * 1000 * 1000) if not refresh else zips_range
    unzip_primes(portion=unzip)
    detable = get_reloads("./prime_csvs/", extension="csv", min_size=10 * 1000 * 1000) if not refresh else zips_range
    detable_primes(portion=detable)

    print("Done!")


def get_reloads(root_path, extension, min_size=0):
    reloads = []
    for i in range(1, 50 + 1):
        filename = root_path + str(i) + "." + extension
        if not os.path.isfile(filename) or os.stat(filename).st_size < min_size:
            reloads.append(i)
    return reloads


def download_prime_zips(save_path="./prime_zips/", portion=range(1, 50 + 1)):
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
    old_path = "./prime_zips/"
    new_path = "./prime_tables/"
    for i in portion:
        with ZipFile(old_path + str(i) + ".zip") as zfile:
            zfile.extract("primes" + str(i) + ".txt", path=new_path)


def detable_primes(portion=range(1, 50 + 1)):
    old_path = "./prime_tables/primes"
    new_path = "./prime_csvs/"
    for i in portion:
        with open(old_path + str(i) + ".txt") as table:
            primes = []
            for line in table:
                nums = [num for num in line.strip(" \n").split(" ") if num != ""]
                if nums:
                    primes.extend(nums)
        del primes[:6]
        with open(new_path + str(i) + ".csv", "w") as out:
            print(*primes, sep=",", file=out)


if __name__ == "__main__":
    main(refresh=False)
