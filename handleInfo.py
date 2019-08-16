# convert info.list to yolo labels

import os


def handleInfoFile(path):
    with open(path + "info.lst") as file:
        lines = [line.rstrip('\n') for line in file]
        # print (lines)
        for info in lines:
            fields = info.split()

            x = int(fields[2])
            y = int(fields[3])
            w = int(fields[4])
            h = int(fields[5])

            size = 100.0

            bx = (x + w / 2) / size
            by = (y + h / 2) / size
            bw = w / size
            bh = h / size

            imgname = fields[0]
            labelName = imgname.split('.')[0] + ".txt"
            with open(path + labelName, 'w') as f:
                print(0, bx, by, bw, bh, file=f)

            pass

    pass


handleInfoFile(os.getcwd() + "/info/")
