import json

if __name__ == "__main__":
    fp = open("result.json", "r")
    wp = open("textrank_output.txt", "w")

    for line in fp:
        wd = json.loads(line.strip())
        wp.write("{0}:{1}\n".format(wd["text"], wd["rank"]))

    fp.close()
    wp.close()
