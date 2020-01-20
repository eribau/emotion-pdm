import csv
import sys

from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

IP = "127.0.0.1"
PORT = "6503"

features = {"f0_mean": 0,
            "f0_var": 0,
            "f0_max": 0,
            "loud_mean": 0,
            # "speech_rate": 0,
            "f1_mean": 0,
            "zcr": 0}
# ranges [min, max] (e.g. ranges["features"][0] = min and ranges["features"][0] = max)
ranges = {  "f0_mean": [0, 450],
            "f0_var": [45, 180],
            "f0_max": [0, 450],
            "loud_mean": [0, 1],
            # "speech_rate": [0, 12],
            "f1_mean": [300, 3000],
            "zcr": [20, 220]}

num_of_features = len(features)
ready_to_send = 0

osc_startup()

# Create channel to send packets over
osc_udp_client(IP, PORT, "osc_client")


def norm(value, feature):
    return (value - ranges[feature][0]) / (ranges[feature][1] - ranges[feature][0])

try:
    for line in iter(sys.stdin.readline, b''):
        # print(line)

        line = line.split(" ")
        if(line[2] == 'smo.F0final_sma') and (float(line[4]) > 0):
            # print("sending message!", line[4])
            msg = oscbuildparse.OSCMessage("/test/F0", ",f", [line[4]])
            print("F0 = ", line[4])
            osc_send(msg, "osc_client")
        if(line[2] == 'smo.pcm_loudness_sma'):
            # print("sending message!", line[4])
            msg = oscbuildparse.OSCMessage("/test/int", ",f", [line[4]])
            print("Int = ", line[4])
            osc_send(msg, "osc_client")
        if(line[2] == 'func.pcm_loudness_sma_amean'):
            loud_mean = float(line[4])
            # Normalize the value so that it is in the range [0, 1]
            loud_mean_norm = norm(loud_mean, "loud_mean")
            features["loud_mean"] = loud_mean_norm
            ready_to_send += 1
            print("loud_mean = ", loud_mean_norm)
        if(line[2] == 'func.F0_sma_amean'):
            f0_mean = float(line[4])
            f0_mean_norm = norm(f0_mean, "f0_mean")
            features["f0_mean"] = f0_mean_norm
            ready_to_send += 1
            # print("f0_mean = ", f0_mean_norm)
        if(line[2] == 'func.F0_sma_max'):
            f0_max = float(line[4])
            f0_max_norm = norm(f0_max, "f0_max")
            features["f0_max"] = f0_max_norm
            ready_to_send += 1
            # print("f0_max = ", f0_max_norm)
        if(line[2] == 'func.F0_sma_stddev'):
            f0_var = float(line[4])
            f0_var_norm = norm(f0_var, "f0_var")
            features["f0_var"] = f0_var_norm
            ready_to_send += 1
            print("f0_var = ", f0_var_norm)
        # if(line[2] == 'func.speakingRate_sma_amean'):
        #     speech_rate = float(line[4])
        #     speech_rate_norm = norm(speech_rate, "speech_rate")
        #     features["speech_rate"] = speech_rate_norm
        #     ready_to_send += 1
        #     print("speech rate = ", speech_rate_norm)
        if(line[2] == 'func.formantFreqLpc_sma[1]_amean'):
            f1_mean = float(line[4])
            f1_mean_norm = norm(f1_mean, "f1_mean")
            features["f1_mean"] = f1_mean_norm
            ready_to_send += 1
            print("f1 mean = ", f1_mean_norm)
        if(line[2] == 'func.voiceQual_sma_amean'):
            zcr_mean = float(line[4])
            zcr_mean_norm = norm(zcr_mean, "zcr")
            features["zcr"] = zcr_mean_norm
            ready_to_send += 1
            print("zcr = ", zcr_mean_norm)

        if(ready_to_send == num_of_features):
            # activation = (0.62 * features["f0_mean"]) * (0.62 * features["f0_var"]) * (0.68 * features["f0_max"])  * (0.8 * features["loud_mean"])
            # valence = (-0.21 * features["f0_mean"]) * (0.08 * features["f0_var"]) * (-0.09 * features["f0_max"]) * (-0.26 * features["loud_mean"])
            activation = (0.2 * features["f0_var"]) + (0.54 * features["loud_mean"]) + (0.25 * features["f1_mean"])  + (0.01 * features["zcr"])
            valence = (0.54 * features["f0_var"]) + (0.07 * features["loud_mean"]) + (0.04 * features["f1_mean"]) + (0.35 * features["zcr"])

            activation = (activation * 2 - 1)
            valence = valence * 2 - 1

            print("Activation = ", activation, " Valence = ", valence)
            act_msg = oscbuildparse.OSCMessage("/test/act", ",f", [activation])
            osc_send(act_msg, "osc_client")
            val_msg = oscbuildparse.OSCMessage("/test/val", ",f", [valence])
            osc_send(val_msg, "osc_client")
            # msg = oscbuildparse.OSCMessage("/test/F0", ",f", [1.0])
            # osc_send(msg, "osc_client")
            ready_to_send = 0

        osc_process()
except KeyboardInterrupt():
    sys.stdout.flush()
    osc_terminate()
    pass
