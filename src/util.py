def get_data(ipath: str) -> list[str]:
    with open(ipath, encoding="utf8") as ifile:
        return [entry.strip() for entry in ifile.readlines()]
