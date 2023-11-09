
# ToDo convert this into a datatype, would be more fun to have as object

class PraatConversion:


    @staticmethod
    def file_set(json_text: dict) -> list:
        """
        Script to convert JSON data to TextGrid/Praat format
        Textgrid is Tab spaced with a new line per item
        Kind of like YAML but more Dutch
        :param json_text: singular dict of data with input in format:
            {
                "start": time,
                "end": time,
                "AudioLength": float,
                "Filename": string,
                "UUID": string,
                "Segments": [{
                        "xmin": time,
                        "xmax": time,
                        "transciption": str
                    }
                ]

            }
        :return: to_file - array of data to be written line by line
        """

        # This  func converts the json to Textgrid format
        to_file = []
        to_file.append('File type = "ooTextFile"')
        to_file.append('Object class = "TextGrid"\n')
        to_file.append(f"xmin = {json_text['start']}")

        # Start and end timestamps for entire file
        to_file.append(f'xmax = {json_text["end"] - json_text["start"]}')
        to_file.append("tiers? <exists>")

        # This should match the amount of Tiers per job
        to_file.append("size = 4")
        to_file.append("item []:")

        to_file.append("\titem[1]:")
        to_file.append('\t\tclass = "IntervalTier"')
        to_file.append('\t\tname = "text"')
        to_file.append(f"\t\txmin = {json_text['start']}")
        to_file.append(f'\t\txmax = {json_text["end"] - json_text["start"]}')
        to_file.append(f'\t\tintervals: size = {len(json_text["Segments"])}')

        l = 1
        # Creating a tier for the text of the transcription
        # assumes time intervals
        for k in json_text["Segments"]:
            to_file.append(f"\t\tintervals [{l}]:")
            to_file.append(f"\t\t\txmin = {k['xmin']}")
            to_file.append(f"\t\t\txmax = {k['xmax']}")
            to_file.append(f'\t\t\ttext = "{k["transcription"]}"')
            l += 1
        to_file.append("\titem[2]:")
        to_file.append('\t\tclass = "TextTier"')
        to_file.append('\t\tname = "Tone"')
        to_file.append(f"\t\txmin = {0}")
        to_file.append(f"\t\txmax = {json_text['end'] - json_text['start']}")
        to_file.append(f"\t\tpoints: size = 0")

        to_file.append("\titem[3]:")
        to_file.append('\t\tclass = "TextTier"')
        to_file.append('\t\tname = "Breaks"')
        to_file.append(f"\t\txmin = {0}")
        to_file.append(f"\t\txmax = {json_text['end'] - json_text['start']}")
        to_file.append(f"\t\tpoints: size = 0")

        to_file.append("\titem[4]:")
        to_file.append('\t\tclass = "IntervalTier"')
        to_file.append('\t\tname = "Miscellaneous"')
        to_file.append(f"\t\txmin = {0}")
        to_file.append(f"\t\txmax = {json_text['end'] - json_text['start']}")
        to_file.append(f"\t\tintervals: size = {len(json_text['Segments'])}")

        for k in json_text["Segments"]:
            to_file.append(f"\t\tintervals [{l}]:")
            to_file.append(f"\t\t\txmin = {k['xmin']}")
            to_file.append(f"\t\t\txmax = {k['xmax']}")
            to_file.append('\t\t\ttext = ""')

        return to_file


    def add_tier(input_):
        """
        Add tiers to a textgrid document to allow dynamic tiers
        :param input_:
        :return:
        """
        tiers = False
        out_array = []
        _tier = []
        for i in input_:
            if i == "size = 2":
                out_array.append("size = 3")
                continue
            elif i == "	item[2]:":
                out_array.append(i)
                _tier.append("\n	item[3]:")
                tiers = True
                continue
            if tiers is False:
                out_array.append(i)
                continue
            if tiers is True:
                if i == '		name = "correction"':
                    out_array.append(i)
                    _tier.append('		name = "transcription"')
                    continue
                out_array.append(i)
                _tier.append(i)
                continue
        out = ""
        out += "\n".join(out_array)
        out += "\n".join(_tier)

        return out

def main():

    # praat conversion example
    example = {
        "start": 0,
        "end": 50,
        'AudioLength': 50,
        "Filename": "fuubar.wav",
        "UUID": "12345",
        "Segments": [{
            "xmin": 0,
            "xmax": 1,
            "transcription": "fuu"
        }, {
            "xmin": 1,
            "xmax": 4,
            "transcription": "bar"}]}


if __name__ == "__main__":
    main()