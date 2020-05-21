import requests
from zipfile import ZipFile


def main(redownload=False):
    # TODO: Check if files exist, then unzip!
    if redownload:
        download_prime_zips()
    print("Done!")


def download_prime_zips(save_path="./primezips/", portion=(1, 50)):
    for i in range(portion[0], portion[1] + 1):
        url = r"https://primes.utm.edu/lists/small/millions/primes" + str(i) + ".zip"
        try:
            r = requests.get(url, stream=True, verify=False)
        except requests.exceptions.MissingSchema:
            print("The supplied URL is invalid. Please update and run again.")
            raise Exception("InvalidURL")
        with open(save_path + str(i) + ".zip", "wb") as f:
            f.write(r.content)


if __name__ == "__main__":
    main()
