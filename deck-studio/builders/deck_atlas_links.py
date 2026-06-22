"""Backward-compatible shim — use deck_link_bindings.py."""
from deck_link_bindings import (  # noqa: F401
    build_deck_link_ops as build_atlas_link_ops,
    cmd_apply,
    cmd_validate,
    load_link_bindings_doc as load_link_bindings,
    main,
    merged_bindings,
    partner_doc_path,
)

if __name__ == "__main__":
    raise SystemExit(main())