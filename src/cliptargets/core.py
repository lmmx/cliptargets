"""Core functionality for cliptargets package."""

import subprocess


def get_targets() -> list[str]:
    """Get all available clipboard targets from xclip.

    Returns:
        List[str]: A list of available clipboard target names

    """
    try:
        result = subprocess.run(
            ["xclip", "-o", "-t", "TARGETS"],
            capture_output=True,
            check=True,
        )
        targets = result.stdout.decode("utf-8").strip().splitlines()
        return targets
    except subprocess.CalledProcessError:
        return []
    except FileNotFoundError:
        raise RuntimeError(
            "xclip command not found. Please install xclip on your system.",
        )


def smart_decode(data: bytes) -> str:
    """Intelligently decode binary data based on content.

    Args:
        data: Binary data to decode

    Returns:
        str: Decoded string

    """
    # Try UTF-16LE if we see null bytes in an alternating pattern
    if b"\x00" in data and len(data) > 2 and data[1:2] == b"\x00":
        try:
            return data.decode("utf-16le")
        except UnicodeDecodeError:
            pass

    # Try UTF-8
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        # Fall back to latin1 which always works
        return data.decode("latin1")


def get_target_value(target: str) -> str | None:
    """Get the value of a specific clipboard target.

    Args:
        target: The target name to query

    Returns:
        Optional[str]: The decoded value of the target, or None if not available

    """
    try:
        result = subprocess.run(
            ["xclip", "-o", "-t", target],
            capture_output=True,
            check=False,  # Don't raise exception on non-zero exit
        )

        if result.returncode != 0:
            return None

        return smart_decode(result.stdout)
    except Exception:
        return None


def get_all_targets() -> dict[str, str | None]:
    """Get all clipboard targets and their values.

    Returns:
        Dict[str, Optional[str]]: A dictionary mapping target names to their values

    """
    targets = get_targets()
    result = {}

    for target in targets:
        result[target] = get_target_value(target)

    return result
