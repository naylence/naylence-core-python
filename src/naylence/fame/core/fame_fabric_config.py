from __future__ import annotations

from pydantic import Field
from typing import Any, Dict, Optional
from naylence.fame.core.util.resource_config import ResourceConfig


class FameFabricConfig(ResourceConfig):
    """High-level fabric bootstrap config passed to FameFabric.create()."""

    type: str = "FameFabric"
    
    opts: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Arbitrary kwargs forwarded to the fabric factory.",
    )
