import gzip

ALLOWED_EXTENSIONS = (".vcf", ".vcf.gz")
REQUIRED_COLUMNS = ["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]


class VcfParseError(Exception):
    """Raised when an uploaded file is not a valid VCF file."""


def has_valid_extension(filename: str) -> bool:
    return filename.lower().endswith(ALLOWED_EXTENSIONS)


def decode_content(filename: str, content: bytes) -> str:
    if filename.lower().endswith(".gz"):
        try:
            content = gzip.decompress(content)
        except OSError as exc:
            raise VcfParseError("File is not a valid gzip archive") from exc
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VcfParseError("File is not a valid text file") from exc


def _empty_to_none(value: str) -> str | None:
    return None if value == "." else value


def _to_float(value: str, line_number: int) -> float | None:
    if value == ".":
        return None
    try:
        return float(value)
    except ValueError as exc:
        raise VcfParseError(f"Line {line_number}: invalid number '{value}'") from exc


def _parse_info(info: str) -> dict[str, str]:
    result = {}
    if info == ".":
        return result
    for item in info.split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            result[key] = value
        else:
            result[item] = ""
    return result


def parse_vcf(text: str) -> tuple[str, list[dict]]:
    file_format = None
    header_found = False
    variants = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue

        # 1. meta lines (##...)
        if line.startswith("##"):
            if line.startswith("##fileformat="):
                file_format = line.split("=", 1)[1].strip()
            continue

        # 2. header line (#CHROM ...)
        if line.startswith("#CHROM"):
            if line.split("\t")[:8] != REQUIRED_COLUMNS:
                raise VcfParseError(f"Line {line_number}: invalid header line")
            header_found = True
            continue

        if not header_found:
            raise VcfParseError(f"Line {line_number}: data found before #CHROM header")

        # 3. data lines (variants)
        fields = line.split("\t")
        if len(fields) < 8:
            raise VcfParseError(f"Line {line_number}: expected at least 8 columns")

        chrom, pos, variant_id, ref, alt, qual, filter_value, info = fields[:8]

        try:
            position = int(pos)
        except ValueError as exc:
            raise VcfParseError(f"Line {line_number}: invalid position '{pos}'") from exc

        info_values = _parse_info(info)
        af_values = info_values["AF"].split(",") if "AF" in info_values else []

        # one row per ALT allele (multi-allelic sites like "A,T" are split)
        for index, single_alt in enumerate(alt.split(",")):
            af = _to_float(af_values[index], line_number) if index < len(af_values) else None
            variants.append(
                {
                    "chrom": chrom,
                    "pos": position,
                    "variant_id": _empty_to_none(variant_id),
                    "ref": ref,
                    "alt": single_alt,
                    "qual": _to_float(qual, line_number),
                    "filter": _empty_to_none(filter_value),
                    "af": af,
                }
            )

    if file_format is None or not file_format.startswith("VCF"):
        raise VcfParseError("Missing or invalid ##fileformat line")
    if not header_found:
        raise VcfParseError("Missing #CHROM header line")

    return file_format, variants
