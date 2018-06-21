from os.path import dirname, join
from os import listdir, mkdir
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from adapter.intend import adapterIntend
from adapter.greeting import adapterGreeting
from adapter.ner_crf import adapterNer
from adapter.make_response import weather_response
from engine.hoaian import HoaiAn

adapIntend = adapterIntend.AdapterIntend()
adapGreeting = adapterGreeting.AdapterGreeting()
adapNer = adapterNer.AdapterNer()

def index(request):
    return render(request, 'index.html')


def log(text):
    today = datetime.now().strftime('%Y%m%d')
    LOG_FOLDER = join(dirname(dirname(__file__)), "logs")
    log_file = join(LOG_FOLDER, "{}.txt".format(today))
    with open(log_file, "a") as f:
        f.write(text + "\n")


@csrf_exempt
def chatbot(request):
    result = {}
    try:
        data = json.loads(request.body.decode("utf-8"))
        text = data["text"]
        uid = data["uid"]
        ip = request.META["REMOTE_ADDR"]
        time = datetime.now().strftime('%Y%m%d %H:%M:%S')
        log_text = "{} {} {} {}".format(ip, time, "USER:", text)
        log(log_text)
        # response_message = HoaiAn.reply("uid", text)

        intend = adapIntend.get_intend(text)
        print("intend : ", intend)

        # if intend is greeting and other
        if intend == 1 or intend == 4:
            response_message = HoaiAn.reply("uid", text)
            # response_message = adapGreeting.make_response(text)

        # if intend is weather question
        else:
            ner_response = adapNer.detect_entity(text)
            print(ner_response)
            results = weather_response.make_msg(ner_response)
            print(results)
            response_message = "hihihi"
            msg = ''
            for i in range(len(results['data'])):
                msg += " Tại " + str(results['data'][i]['địa điểm']).title() + " " + str(
                    results['data'][i]['thời gian']) + ': '
                for k, v in results['data'][i]['thời tiết'].items():
                    if isinstance(v, dict):
                        msg += str(k) + ":  "
                        for i, j in v.items():
                            msg += ", "
                    else:
                        msg += str(k) + " : " + str(v)
                    msg += ", "
            print("msg : ", msg)

        log_text = "{} {} {} {}".format(ip, time, "BOT:", response_message)
        log(log_text)

        result["output"] = msg
    except Exception as e:
        print(e)
        result = {"error": "Bad request!"}
    return JsonResponse(result)


if __name__ == '__main__':
    log("hihi")
