import pandas as pd


def parseFuelHeight(hexString):
    if not isinstance(hexString, str):
        return "No Data"

    prefix = "000E012B010A00"
    startIndex = hexString.find(prefix)

    if startIndex != -1:
        dataStart = startIndex + len(prefix) + 6

        heightHex = hexString[dataStart: dataStart+8]
        try:
            return int(heightHex, 16)
        except ValueError:
            return "Error"
    return None


def parseNetwork(hexString):
    try:
        if not isinstance(hexString, str):
            return "No Data"

        hexString = hexString.strip()
        pos = hexString.find("0137")

        if pos == -1:
            return "Not Found"

        statusHex = hexString[pos+4: pos+12]
        statusVal = int(statusHex, 16)
        networkBits = statusVal & 0b11

        networkMap = {0: "Unknown", 1: "2G", 2: "4G", 3: "5G"}
        return networkMap.get(networkBits, "Unknown")
    except:
        return None


def parseInternalVoltage(hexString):
    if not isinstance(hexString, str):
        return "No Data"

    idx = hexString.find("0004002D")
    if idx != -1:
        dataStart = idx + 8
        if dataStart + 4 <= len(hexString):
            valHex = hexString[dataStart: dataStart+4]
            try:
                return round(int(valHex, 16) * 0.001, 2)
            except ValueError:
                return "Error"
    return None


def parseExternalVoltage(hexString):
    if not isinstance(hexString, str):
        return "No Data"

    idx = hexString.find("000400CE")
    if idx != -1:
        dataStart = idx + 8
        if dataStart + 4 <= len(hexString):
            valHex = hexString[dataStart: dataStart+4]
            try:
                return round(int(valHex, 16) * 0.001, 2)
            except ValueError:
                return "Error"
    return None


# blm selesai
def parseTemperatures(hexString):
    if not isinstance(hexString, str):
        return []

    idx = hexString.find("012C")
    if idx >= 4:
        try:
            length = int(hexString[idx-4: idx], 16)
            dataLenChars = (length - 2) * 2
            dataStart = idx + 4
            dataHex = hexString[dataStart: dataStart + dataLenChars]

            temps = []
            for i in range(0, len(dataHex), 2):
                temps.append(int(dataHex[i:i+2], 16))
            return temps
        except ValueError:
            return "Error"
    return None


def process_hex_row(row):
    hexData = row['custom.235.hex']
    return pd.Series({
        'fuelHeight': parseFuelHeight(hexData),
        'networkType': parseNetwork(hexData),
        'internalVoltage': parseInternalVoltage(hexData),
        'externalVoltage': parseExternalVoltage(hexData),
        # 'temperatures': parseTemperatures(hexData),
    })
