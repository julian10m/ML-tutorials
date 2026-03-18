from __future__ import annotations

from pathlib import Path
import shutil
import filecmp


def files_are_equal(src: Path, dst: Path) -> bool:
    """Return True if both files exist and have the same contents."""
    return dst.exists() and filecmp.cmp(src, dst, shallow=False)


def sync_figures(code_root: Path, assets_root: Path) -> None:
    """
    Find every directory named 'figures' under code_root and mirror its files
    into assets_root, preserving the relative path from code_root.
    """
    if not code_root.exists():
        print(f"[sync-assets] code root does not exist: {code_root}")
        return

    copied = 0
    skipped = 0

    for figures_dir in code_root.rglob("figures"):
        if not figures_dir.is_dir():
            continue

        rel_dir = figures_dir.relative_to(code_root)
        target_dir = assets_root / rel_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        for src_file in figures_dir.rglob("*"):
            if not src_file.is_file():
                continue

            rel_file = src_file.relative_to(figures_dir)
            dst_file = target_dir / rel_file
            dst_file.parent.mkdir(parents=True, exist_ok=True)

            if files_are_equal(src_file, dst_file):
                skipped += 1
                print(f"[skip] {dst_file}")
                continue

            shutil.copy2(src_file, dst_file)
            copied += 1
            print(f"[copy] {src_file} -> {dst_file}")

    print(f"[sync-assets] done. copied={copied}, skipped={skipped}")


def main() -> None:
    # File is expected at: repo/quarto/scripts/sync_assets.py
    quarto_dir = Path(__file__).resolve().parents[1]
    repo_root = quarto_dir.parent

    code_root = repo_root / "code"
    assets_root = quarto_dir / "assets"

    assets_root.mkdir(parents=True, exist_ok=True)
    sync_figures(code_root, assets_root)


if __name__ == "__main__":
    main()