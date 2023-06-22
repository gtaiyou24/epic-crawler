from enum import Enum


class CharacterCode(Enum):
    UTF_8 = 1
    ASCII = 2
    SHIFT_JIS = 3
    EUC_JP = 4
    WINDOWS_1254 = 5

    @staticmethod
    def value_of(char_code: str):
        if (char_code == "UTF-8") or (char_code == "utf-8"):
            return CharacterCode.UTF_8
        elif (char_code == "ascii") or (char_code == "ascii"):
            return CharacterCode.ASCII
        elif (char_code == "SHIFT-JIS") or (char_code == "shift-jis"):
            return CharacterCode.SHIFT_JIS
        elif (char_code == "EUC-JP") or (char_code == "euc-jp"):
            return CharacterCode.EUC_JP
        elif (char_code == "Windows-1254") or (char_code == "windows-1254"):
            return CharacterCode.WINDOWS_1254
        else:
            raise Exception("該当の文字コードが存在しません。 (文字コード = {})".format(char_code))
