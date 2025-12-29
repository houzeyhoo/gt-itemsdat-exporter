from typing import BinaryIO, NamedTuple

# Latest supported version
MAX_VERSION = 23

# Used to decrypt item names
ITEM_NAME_KEY = "PBG892FXX982ABC*"


ItemData = dict[str, int | str]


class ItemsDatParsed(NamedTuple):
    version: int | None
    item_count: int | None
    items: list[ItemData]


def parse_items_dat(
    fp: BinaryIO, *, skip_version_check: bool = False, include_metadata: bool = False, skip_bytes: int = 0
) -> ItemsDatParsed:
    version = _read_integer(fp, size=2)
    if not skip_version_check and version > MAX_VERSION:
        raise ValueError(f"Unsupported items.dat version: {version}, max supported: {MAX_VERSION}")
    item_count = _read_integer(fp, size=4)
    items = []

    for i in range(item_count):
        item = {}
        item["Id"] = _read_integer(fp, size=4)

        # If the item ID doesn't match, something has gone wrong during parsing
        if item["Id"] != i:
            raise ValueError(f"Item ID mismatch at index {i}: expected {i}, got {item['Id']}.")

        item["Properties"] = _read_integer(fp, size=2)
        item["Type"] = _read_integer(fp, size=1)
        item["Material"] = _read_integer(fp, size=1)

        # Item names are encrypted starting from version 3 onwards
        item["Name"] = _read_string(fp)
        if version >= 3:
            item["Name"] = _decrypt_string(item["Name"], offset=i)

        item["FilePath"] = _read_string(fp)
        item["FileHash"] = _read_integer(fp, size=4)
        item["VisualType"] = _read_integer(fp, size=1)
        item["CookTime"] = _read_integer(fp, size=4)
        item["TexX"] = _read_integer(fp, size=1)
        item["TexY"] = _read_integer(fp, size=1)
        item["StorageType"] = _read_integer(fp, size=1)
        item["Layer"] = _read_integer(fp, size=1)
        item["CollisionType"] = _read_integer(fp, size=1)
        item["Hardness"] = _read_integer(fp, size=1)
        item["RegenTime"] = _read_integer(fp, size=4)
        item["ClothingType"] = _read_integer(fp, size=1)
        item["Rarity"] = _read_integer(fp, size=2)
        item["MaxHold"] = _read_integer(fp, size=1)
        item["AltFilePath"] = _read_string(fp)
        item["AltFileHash"] = _read_integer(fp, size=4)
        item["AnimMs"] = _read_integer(fp, size=4)

        if version >= 4:
            item["PetName"] = _read_string(fp)
            item["PetPrefix"] = _read_string(fp)
            item["PetSuffix"] = _read_string(fp)

        if version >= 5:
            item["PetAbility"] = _read_string(fp)

        # Back to base version
        item["SeedBase"] = _read_integer(fp, size=1)
        item["SeedOver"] = _read_integer(fp, size=1)
        item["TreeBase"] = _read_integer(fp, size=1)
        item["TreeOver"] = _read_integer(fp, size=1)
        item["BgCol"] = _read_integer(fp, size=4)
        item["FgCol"] = _read_integer(fp, size=4)
        item["Seed1"] = _read_integer(fp, size=2)
        item["Seed2"] = _read_integer(fp, size=2)
        item["BloomTime"] = _read_integer(fp, size=4)

        if version >= 7:
            item["AnimType"] = _read_integer(fp, size=4)
            item["AnimString"] = _read_string(fp)

        if version >= 8:
            item["AnimTex"] = _read_string(fp)
            item["AnimString2"] = _read_string(fp)
            item["DLayer1"] = _read_integer(fp, size=4)
            item["DLayer2"] = _read_integer(fp, size=4)

        if version >= 9:
            item["Properties2"] = _read_integer(fp, size=2)
            _discard_fixed(fp, n=62)

        if version >= 10:
            item["TileRange"] = _read_integer(fp, size=4)
            item["PileRange"] = _read_integer(fp, size=4)

        if version >= 11:
            item["CustomPunch"] = _read_string(fp)

        if version >= 12:
            _discard_fixed(fp, n=13)

        if version >= 13:
            item["ClockDiv"] = _read_integer(fp, size=4)

        if version >= 14:
            item["ParentId"] = _read_integer(fp, size=4)

        # Version 15
        if version >= 15:
            _discard_fixed(fp, n=25)
            item["AltSitPath"] = _read_string(fp)

        # Version 16 (Dynamic Padding)
        if version >= 16:
            _discard_string(fp)

        if version >= 17:
            _discard_fixed(fp, n=4)

        if version >= 18:
            _discard_fixed(fp, n=4)

        if version >= 19:
            _discard_fixed(fp, n=9)

        if version >= 21:
            _discard_fixed(fp, n=2)

        if version >= 22:
            item["Description"] = _read_string(fp)

        if version >= 23:
            item["Ingredient1"] = _read_integer(fp, size=2)
            item["Ingredient2"] = _read_integer(fp, size=2)

        # Skip extra bytes if specified
        if skip_bytes > 0:
            _discard_fixed(fp, n=skip_bytes)
        elif skip_bytes == -1:
            _discard_string(fp)

        items.append(item)

    if include_metadata:
        return ItemsDatParsed(version=version, item_count=item_count, items=items)
    else:
        return ItemsDatParsed(version=None, item_count=None, items=items)


def _discard_fixed(fp: BinaryIO, *, n: int) -> None:
    fp.seek(n, 1)


def _discard_string(fp: BinaryIO) -> None:
    length = _read_integer(fp, size=2)
    _discard_fixed(fp, n=length)


def _read_integer(fp: BinaryIO, *, size: int, signed: bool = False) -> int:
    return int.from_bytes(fp.read(size), "little", signed=signed)


def _read_string(fp: BinaryIO) -> str:
    length = _read_integer(fp, size=2)
    return fp.read(length).decode("utf-8")


def _decrypt_string(encrypted: str, *, offset: int) -> str:
    key_length = len(ITEM_NAME_KEY)
    decrypted = []
    for i, c in enumerate(encrypted):
        decrypted.append(chr(ord(c) ^ ord(ITEM_NAME_KEY[(i + offset) % key_length])))
    return "".join(decrypted)
