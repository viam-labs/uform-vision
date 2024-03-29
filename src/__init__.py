"""
This file registers the model with the Python SDK.
"""

from viam.services.vision import Vision
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .uform import uform

Registry.register_resource_creator(Vision.SUBTYPE, uform.MODEL, ResourceCreatorRegistration(uform.new, uform.validate))
