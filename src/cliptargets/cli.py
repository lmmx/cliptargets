"""Command line interface for cliptargets."""

import json
import sys

from .core import get_all_targets


def format_value(value: str | None) -> str:
    """Format a target value for display.

    Args:
        value: The target value to format

    Returns:
        str: A formatted string representation

    """
    if value is None:
        return "<not available>"

    # Replace literal newlines with '\n' for cleaner output
    if "\n" in value:
        formatted = repr(value)
        # Strip quotes added by repr if they exist
        if formatted.startswith(("'", '"')) and formatted.endswith(("'", '"')):
            formatted = formatted[1:-1]
        return formatted

    return value


def cli() -> None:
    """Run the CLI command."""
    as_json = "--json" in sys.argv
    try:
        targets = get_all_targets()

        # Handle empty result
        if not targets:
            print("No clipboard targets found.", file=sys.stderr)
            sys.exit(0)

        # Print targets
        max_target_len = max(len(target) for target in targets.keys())

        # Print JSON data if requested
        if as_json:
            # Convert None values to null for proper JSON
            json_targets = {k: v if v is not None else None for k, v in targets.items()}
            print(json.dumps(json_targets, indent=2))
        else:
            print(f"Found {len(targets)} clipboard targets:", file=sys.stderr)
            print(file=sys.stderr)
            for target, value in sorted(targets.items()):
                formatted_value = format_value(value)
                print(f"{target:{max_target_len}} : {formatted_value}", file=sys.stderr)

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    cli()
