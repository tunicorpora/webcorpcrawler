import re
import progressbar

def TryToFixByText(orig, conll):
    """
    If the usual method for adding parsed fails and the parsing has been done with 
    Turku neural parser, try to match sentences by the txt property

    - orig the unparsed, prepared input
    - conll the raw conll input
    """
    texts = re.findall("# text = (.*)", conll)
    raw = "\n".join([l for l in conll.splitlines() if not re.search("^#", l) or re.search("^# text", l)])
    pat = re.compile("# text = .*")
    conll_sentences = [sent for sent in  pat.split(raw) if sent]
    segments = re.split("###C:.*", orig)
    sent_idx = -1
    matches = []
    print("Scanning through the sentences/segments...")
    for idx, seg in progressbar.progressbar(enumerate(segments)):
        sent_idx += 1
        seg = seg.strip().replace("\n"," ")
        seg = re.sub(r"\s+", " ", seg.strip())
        if sent_idx < len(texts):
            sents = texts[sent_idx]
            conllsents = conll_sentences[sent_idx]
            while sents != seg:
                if sent_idx + 1 < len(texts):
                    sent_idx += 1
                else:
                    break
                sents += " "  + texts[sent_idx]
                conllsents += "\n\n" +  conll_sentences[sent_idx]
            if sents == seg:
                #If a match was found
                matches.append({"text" : seg, "conll": conllsents.strip(), "idx": idx})
    print("Managed to locate {} matching segments.".format(len(matches)))
    return matches




