# import local modules
import dictionary as dict
import preprocessing
import beat_algorithm
# import foreign modules
import flask
import time
import math

start_time = time.time()
app = flask.Flask(__name__)


# Main program.
def main():
    # define youtube id
    id = "N8BXtM6onEY"
    # preprocess audio file
    preprocessing.downloadAudio(id)
    preprocessing.splitAudio(id, mode=dict.STEMS2, output=dict.ACCOMPANIMENT)
    preprocessing.resampleAudio(id)
    # preprocessing.filterAudio(id)
    # analyze song
    _, librosaBeats = beat_algorithm.librosaBeatAnalysis(id)
    manual = [
            0.3,
            1.0058823529411764,
            1.711764705882353,
            2.4176470588235297,
            3.1235294117647063,
            3.829411764705883,
            4.53529411764706,
            5.241176470588236,
            5.947058823529413,
            6.6529411764705895,
            7.358823529411766,
            8.064705882352943,
            8.770588235294118,
            9.476470588235294,
            10.18235294117647,
            10.888235294117646,
            11.594117647058821,
            12.299999999999997,
            13.005882352941173,
            13.711764705882349,
            14.417647058823524,
            15.1235294117647,
            15.829411764705876,
            16.53529411764705,
            17.24117647058823,
            17.947058823529407,
            18.652941176470584,
            19.35882352941176,
            20.06470588235294,
            20.770588235294117,
            21.476470588235294,
            22.18235294117647,
            22.88823529411765,
            23.594117647058827,
            24.300000000000004,
            25.005882352941182,
            25.71176470588236,
            26.417647058823537,
            27.123529411764714,
            27.829411764705892,
            28.53529411764707,
            29.241176470588247,
            29.947058823529424,
            30.652941176470602,
            31.35882352941178,
            32.06470588235295,
            32.77058823529413,
            33.4764705882353,
            34.182352941176475,
            34.88823529411765,
            35.59411764705882,
            36.3,
            37.00588235294117,
            37.711764705882345,
            38.41764705882352,
            39.12352941176469,
            39.82941176470587,
            40.53529411764704,
            41.241176470588215,
            41.94705882352939,
            42.65294117647056,
            43.35882352941174,
            44.06470588235291,
            44.770588235294085,
            45.47647058823526,
            46.18235294117643,
            46.88823529411761,
            47.59411764705878,
            48.299999999999955,
            49.00588235294113,
            49.7117647058823,
            50.417647058823476,
            51.12352941176465,
            51.829411764705824,
            52.535294117647,
            53.24117647058817,
            53.947058823529346,
            54.65294117647052,
            55.358823529411694,
            56.06470588235287,
            56.77058823529404,
            57.476470588235216,
            58.18235294117639,
            58.888235294117564,
            59.59411764705874,
            60.29999999999991,
            61.005882352941086,
            61.71176470588226,
            62.417647058823434,
            63.12352941176461,
            63.82941176470578,
            64.53529411764696,
            65.24117647058813,
            65.9470588235293,
            66.65294117647048,
            67.35882352941165,
            68.06470588235283,
            68.770588235294,
            69.47647058823517,
            70.18235294117635,
            70.88823529411752,
            71.5941176470587,
            72.29999999999987,
            73.00588235294104,
            73.71176470588222,
            74.41764705882339,
            75.12352941176457,
            75.82941176470574,
            76.53529411764691,
            77.24117647058809,
            77.94705882352926,
            78.65294117647043,
            79.35882352941161,
            80.06470588235278,
            80.77058823529396,
            81.47647058823513,
            82.1823529411763,
            82.88823529411748,
            83.59411764705865,
            84.29999999999983,
            85.005882352941,
            85.71176470588217,
            86.41764705882335,
            87.12352941176452,
            87.8294117647057,
            88.53529411764687,
            89.24117647058804,
            89.94705882352922,
            90.65294117647039,
            91.35882352941157,
            92.06470588235274,
            92.77058823529391,
            93.47647058823509,
            94.18235294117626,
            94.88823529411744,
            95.59411764705861,
            96.29999999999978,
            97.00588235294096,
            97.71176470588213,
            98.4176470588233,
            99.12352941176448,
            99.82941176470565,
            100.53529411764683,
            101.241176470588,
            101.94705882352918,
            102.65294117647035,
            103.35882352941152,
            104.0647058823527,
            104.77058823529387,
            105.47647058823505,
            106.18235294117622,
            106.8882352941174,
            107.59411764705857,
            108.29999999999974,
            109.00588235294092,
            109.71176470588209,
            110.41764705882326,
            111.12352941176444,
            111.82941176470561,
            112.53529411764679,
            113.24117647058796,
            113.94705882352913,
            114.6529411764703,
            115.35882352941148,
            116.06470588235265,
            116.77058823529383,
            117.476470588235,
            118.18235294117618,
            118.88823529411735,
            119.59411764705852,
            120.2999999999997,
            121.00588235294087,
            121.71176470588205,
            122.41764705882322,
            123.1235294117644,
            123.82941176470557,
            124.53529411764674,
            125.24117647058792,
            125.94705882352909,
            126.65294117647026,
            127.35882352941144,
            128.06470588235263,
            128.77058823529381,
            129.476470588235,
            130.1823529411762,
            130.88823529411738,
            131.59411764705857,
            132.29999999999976,
            133.00588235294094,
            133.71176470588213,
            134.41764705882332,
            135.1235294117645,
            135.8294117647057,
            136.53529411764688,
            137.24117647058807,
            137.94705882352926,
            138.65294117647045,
            139.35882352941164,
            140.06470588235283,
            140.770588235294,
            141.4764705882352,
            142.1823529411764,
            142.88823529411758,
            143.59411764705877,
            144.29999999999995,
            145.00588235294114,
            145.71176470588233,
            146.41764705882352,
            147.1235294117647,
            147.8294117647059,
            148.53529411764708,
            149.24117647058827,
            149.94705882352946,
            150.65294117647065,
            151.35882352941184,
            152.06470588235302,
            152.7705882352942,
            153.4764705882354,
            154.1823529411766,
            154.88823529411778,
            155.59411764705897,
            156.30000000000015,
            157.00588235294134,
            157.71176470588253,
            158.41764705882372,
            159.1235294117649,
            159.8294117647061,
            160.53529411764728,
            161.24117647058847,
            161.94705882352966,
            162.65294117647085,
            163.35882352941204,
            164.06470588235322,
            164.7705882352944,
            165.4764705882356,
            166.1823529411768,
            166.88823529411798,
            167.59411764705916,
            168.30000000000035,
            169.00588235294154,
            169.71176470588273,
            170.41764705882392,
            171.1235294117651,
            171.8294117647063,
            172.53529411764748,
            173.24117647058867,
            173.94705882352986,
            174.65294117647105,
            175.35882352941223,
            176.06470588235342,
            176.7705882352946,
            177.4764705882358,
            178.182352941177,
            178.88823529411818,
            179.59411764705936,
            180.30000000000055,
            181.00588235294174,
            181.71176470588293,
            182.41764705882412,
            183.1235294117653,
            183.8294117647065,
            184.53529411764768,
            185.24117647058887,
            185.94705882353006,
            186.65294117647124,
            187.35882352941243,
            188.06470588235362,
            188.7705882352948,
            189.476470588236,
            190.1823529411772,
            190.88823529411837,
            191.59411764705956,
            192.30000000000075,
            193.00588235294194,
            193.71176470588313,
            194.41764705882431,
            195.1235294117655,
            195.8294117647067,
            196.53529411764788,
            197.24117647058907,
            197.94705882353026,
            198.65294117647144,
            199.35882352941263,
            200.06470588235382,
            200.770588235295,
            201.4764705882362,
            202.18235294117738,
            202.88823529411857,
            203.59411764705976,
            204.30000000000095,
            205.00588235294214,
            205.71176470588333,
            206.4176470588245,
            207.1235294117657,
            207.8294117647069,
            208.53529411764808,
            209.24117647058927,
            209.94705882353045,
            210.65294117647164,
            211.35882352941283,
            212.06470588235402,
            212.7705882352952,
            213.4764705882364,
            214.18235294117758,
            214.88823529411877,
            215.59411764705996,
            216.30000000000115,
            217.00588235294234,
            217.71176470588352,
            218.4176470588247,
            219.1235294117659,
            219.8294117647071,
            220.53529411764828,
            221.24117647058947,
            221.94705882353065,
            222.65294117647184,
            223.35882352941303,
            224.06470588235422,
            224.7705882352954,
            225.4764705882366,
            226.18235294117778,
            226.88823529411897,
            227.59411764706016,
            228.30000000000135,
            229.00588235294254,
            229.71176470588372,
            230.4176470588249,
            231.1235294117661,
            231.8294117647073,
            232.53529411764848,
            233.24117647058966,
            233.94705882353085
        ]
    beat_algorithm.plotBeats(id, manual_beats=manual, aubio_beats=None, librosa_beats=librosaBeats, start=None, end=None)


# Calculate time since program started in seconds.
def getUptime():
    return ("%i seconds" % math.floor(time.time() - start_time))


# Diagnosis endpoint.
@app.route(dict.DIAGNOSIS_PATH)
def diagnosis():
    output = {
        "Version": dict.VERSION,
        "Uptime": getUptime()
    }
    return output


# Analysis endpoint.
@app.route(dict.ANALYSIS_PATH)
def analysis():
    # get youtube id
    id = flask.request.args.get('id', None)
    if id is None:
        error = {
            "Msg": "Requires a YouTube ID, example: '.../v1/analysis?id=dQw4w9WgXcQ'"
        }
        return error
    # preprocess audio file
    preprocessing.downloadAudio(id)
    preprocessing.resampleAudio(id)
    # analyze song
    bpm, beats = beat_algorithm.librosaBeatAnalysis(id)
    # return output
    output = {
        "bpm": bpm,
        "beats": beats
    }
    return output


# branch if program is run through 'python main.py'
if __name__ == "__main__":
    main()
