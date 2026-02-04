import pandas as pd
from models import detail_repo_form, CardDetailsManager

LEVEL_REMAP_N2S = {
    "0": "--",
    "1": "A1",
    "2": "A2",
    "3": "B1",
    "4": "B2",
    "5": "C1",
    "6": "C2",
}

LEVEL_REMAP_S2N = {
    "--": "0",
    "A1": "1",
    "A2": "2",
    "B1": "3",
    "B2": "4",
    "C1": "5",
    "C2": "6",
}

PART_OF_SPEECH_REMAP_N2S = {
    "00": "--",
    "10": "n.",
    "11": "cn.",
    "12": "un.",
    "13": "pn.",
    "20": "v.",
    "21": "vt.",
    "22": "vi.",
    "30": "adj.",
    "40": "adv.",
    "50": "prep.",
    "60": "conj.",
    "70": "exclam.",
    "80": "art.",
    "90": "quant.",
}

PART_OF_SPEECH_REMAP_S2N = {
    "--": "00",
    "n.": "10",
    "cn.": "11",
    "un.": "12",
    "pn.": "13",
    "v.": "20",
    "vt.": "21",
    "vi.": "22",
    "adj.": "30",
    "adv.": "40",
    "prep.": "50",
    "conj.": "60",
    "exclam.": "70",
    "art.": "80",
    "quant.": "90",
}



class DetailRepositoryManager:
    def __init__(self):
        self.detail_repo_path = "./Assets/detail_repository.csv"
        # self.detail_repo = pd.read_csv(self.detail_repo_path, dtype=detail_repo_form)
        self.card_details_manager = CardDetailsManager()
        self._explain_counter = {}

    def generate_line(self, detail:dict):
        root_raw = detail.get("root", 0)
        word = detail.get("word", "")
        level_str = detail.get("level", "--")
        pos_str = detail.get("part of speech", detail.get("part_of_speech", "--"))
        addition = detail.get("addition", "-")
        explaination = detail.get("explaination", "")

        try:
            root_code = "{:0>8d}".format(int(str(root_raw)))
        except:
            root_code = "{:0>8s}".format(str(root_raw)[:8])

        level_second = LEVEL_REMAP_S2N.get(level_str, str(level_str))
        if level_second not in ["0","1","2","3","4","5","6"]:
            level_second = "0"
        level_code = "1" + level_second

        pos_code = PART_OF_SPEECH_REMAP_S2N.get(pos_str, "00")

        counter_key = (str(root_raw), pos_code)
        current = self._explain_counter.get(counter_key, 0) + 1
        self._explain_counter[counter_key] = current
        explain_code = "{:0>2d}".format(current)

        phrase_code = "00"
        serial_code = f"{level_code}{pos_code}{explain_code}{phrase_code}"

        content = word if addition == "-" or addition == "" else f"{word}({addition})"

        line = {
            "root": root_code,
            "serial": serial_code,
            "sentence": "00000000",
            "content": content,
            "translation": explaination,
            "synonym": "",
            "antonym": "",
        }
        return line
