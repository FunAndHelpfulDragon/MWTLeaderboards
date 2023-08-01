import argparse
import json
import easyocr
from modules.is_digit import is_digit


def parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--picture", help="Path of the picture to get data out of", metavar="path", required=True)
    arg_parser.add_argument("-r", "--result", default="results.json", help="Path of the result file.", metavar="path")

    return vars(arg_parser.parse_args())


def retrieve_data(path: str) -> list[str]:
    """Reads the data off an image

    Args:
        path (str): The path to the image to read

    Returns:
        list[str]: The data returned from the image
    """
    reader = easyocr.Reader(["ch_sim", "en"])
    return reader.readtext(path, detail=0)


def fix_result_and_translate(data: list) -> dict:
    place = -1
    place_index = -1
    json_data = {"type": "", "data": {}}
    for index, item in enumerate(data):
        # print(place_index, index)
        item: str

        # Tells the program what type of leaderboard to save them time
        if item.startswith("[") and item.endswith("]"):
            json_data["type"] = item.removeprefix("[").removesuffix("]")

        # Assume that the data hasn't become corrupt enough
        # that this can't detect the first place position
        # Stupid, To be improved
        if index == 2:
            place = 1
            place_index = index
            json_data["data"][place] = {
                "name": data[index + 1],
                "value": data[index + 2].split(" ")[0],
            }

        if index == place_index + 3:
            # assuming data isn't broken, this should be the next place index
            # as "rebirths" text would be groped
            place += 1
            place_index = index

            json_data["data"][place] = {
                "name": data[index + 1],
                "value": data[index + 2],
            }

        if index == place_index + 2:
            if not is_digit(item):
                for letter in item:
                    # This can be expanded as neseccary.
                    match letter:
                        case "o":
                            letter = "0"
                            continue
                        case "O":
                            letter = "0"
                            continue
                        case "G":
                            letter = "6"
                            continue
                        case "g":
                            letter = "9"
                            continue

    return json_data


args = parser()
print(args)

result = fix_result_and_translate(retrieve_data(args.get("picture")))
with open(f'{args.get("result")}', "w+") as f:
    f.write(json.dumps(result))
