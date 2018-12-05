

def MarkFirstPara(self):
    """
    Tries to locate the first paragraph of a text (containing a real sentence)
    """
    import re

    for e_idx, entry in enumerate(self.data):
        for i_idx, item in enumerate(entry["data"]):
            txt = self.data[e_idx]["data"][i_idx]["txt"]
            pat = re.compile("\n{2,}")
            paragraphs = pat.split(txt)
            first_para = paragraphs[0]
            i = 0
            while len(first_para.split(" ")) < 5 or not re.search("[.!?;:]", first_para):
                i += 1
                if i < len(paragraphs):
                    first_para = paragraphs[i]
                else:
                    break
            txt = self.data[e_idx]["data"][i_idx]["firstpara_new"] = first_para

    self.Output()


JsonUpdater.custom = MarkFirstPara
