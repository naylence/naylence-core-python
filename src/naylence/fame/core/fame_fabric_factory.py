from naylence.fame.core.fame_fabric import FameFabric
from naylence.fame.core.fame_fabric_config import FameFabricConfig
from naylence.fame.core.util.resource_factory import ResourceFactory


class FameFabricFactory(ResourceFactory[FameFabric, FameFabricConfig]):
    """Entry-point base-class for concrete fabric factories."""
