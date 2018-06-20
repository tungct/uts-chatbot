from adapter.ner_crf import ner_crf

def getResponse(usr_message):
    ner_message = ner_crf.detect_entity(usr_message)
    return ner_message