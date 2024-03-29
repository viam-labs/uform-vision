from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self

from typing import Any, Final, List, Mapping, Optional, Union

from PIL import Image
from transformers import AutoModel, AutoProcessor
import torch

from viam.media.video import RawImage
from viam.proto.common import PointCloudObject
from viam.proto.service.vision import Classification, Detection
from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype
from viam.utils import ValueTypes

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.components.camera import Camera

from viam.services.vision import Vision
from viam.logging import getLogger

import time
import asyncio

LOGGER = getLogger(__name__)

class uform(Vision, Reconfigurable):
    
    """
    Vision represents a Vision service.
    """
    

    MODEL: ClassVar[Model] = Model(ModelFamily("viam-labs", "vision"), "uform")
    
    model = AutoModel
    processor = AutoProcessor
    inference_config = {}

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        # here we validate config, the following is just an example and should be updated as needed
        some_pin = config.attributes.fields["some_pin"].number_value
        if some_pin == "":
            raise Exception("A some_pin must be defined")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.DEPS = dependencies
        self.inference_config['max_tokens'] = config.attributes.fields["max_tokens"].number_value or 256
        self.model = AutoModel.from_pretrained("unum-cloud/uform-gen2-qwen-500m", trust_remote_code=True)
        self.processor = AutoProcessor.from_pretrained("unum-cloud/uform-gen2-qwen-500m", trust_remote_code=True)
        return

    
    async def get_detections_from_camera(
        self, camera_name: str, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Detection]:
        # not implemented, not a detector
        ...

    
    async def get_detections(
        self,
        image: Union[Image.Image, RawImage],
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Detection]:
        # not implemented, not a detector
        ...

    
    async def get_classifications_from_camera(
        self,
        camera_name: str,
        count: int,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Classification]:
        
        actual_cam = self.DEPS[Camera.get_resource_name(camera_name)]
        cam = cast(Camera, actual_cam)
        cam_image = await cam.get_image(mime_type="image/jpeg")
        return await self.get_classifications(cam_image, count, extra=extra)

    
    async def get_classifications(
        self,
        image: Union[Image.Image, RawImage],
        count: int,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Classification]:
       
       prompt = "describe this image"
       if extra != None and extra.get('question') != None:
        prompt = extra['question']

       inputs = self.processor(text=[prompt], images=[image], return_tensors="pt")
       with torch.inference_mode():
        output = self.model.generate(
            **inputs,
            do_sample=False,
            use_cache=True,
            max_new_tokens=self.inference_config['max_tokens'],
            eos_token_id=151645,
            pad_token_id=self.processor.tokenizer.pad_token_id
        )
        prompt_len = inputs["input_ids"].shape[1]
        decoded_text = self.processor.batch_decode(output[:, prompt_len:])[0]
        # uform always includes this at the end, remove
        decoded_text = decoded_text.replace('<|im_end|>', '')
        classifications = [{"class_name": decoded_text, "confidence": 1}]
        return classifications
       
    async def get_object_point_clouds(
        self, camera_name: str, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[PointCloudObject]:
        """
        Returns a list of the 3D point cloud objects and associated metadata in the latest
        picture obtained from the specified 3D camera (using the specified segmenter).

        To deserialize the returned information into a numpy array, use the Open3D library.
        ::

            import numpy as np
            import open3d as o3d

            object_point_clouds = await vision.get_object_point_clouds(camera_name, segmenter_name)

            # write the first object point cloud into a temporary file
            with open("/tmp/pointcloud_data.pcd", "wb") as f:
                f.write(object_point_clouds[0].point_cloud)
            pcd = o3d.io.read_point_cloud("/tmp/pointcloud_data.pcd")
            points = np.asarray(pcd.points)

        Args:
            camera_name (str): The name of the camera

        Returns:
            List[viam.proto.common.PointCloudObject]: The pointcloud objects with metadata
        """
        ...

    
    async def do_command(self, command: Mapping[str, ValueTypes], *, timeout: Optional[float] = None) -> Mapping[str, ValueTypes]:
        """Send/receive arbitrary commands

        Args:
            command (Dict[str, ValueTypes]): The command to execute

        Returns:
            Dict[str, ValueTypes]: Result of the executed command
        """
        ...

