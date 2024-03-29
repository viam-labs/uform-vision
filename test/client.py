import asyncio
import os
from PIL import Image

from viam.robot.client import RobotClient
from viam.services.vision import VisionClient

# these must be set, you can get them from your robot's 'CODE SAMPLE' tab
robot_api_key_id = os.getenv('API_KEY_ID') or ''
robot_api_key = os.getenv('API_KEY') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''

async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key=robot_api_key,
      api_key_id=robot_api_key_id
    )
    return await RobotClient.at_address(robot_address, opts)

async def main():
    robot = await connect()
    uform_vision = VisionClient.from_robot(robot, "uform-vision")

    prompt = "In one word, is there a cat standing on a table or countertop?"

    image = Image.open( os.getcwd() + "/test/table.jpg")
    uform_vision_return_value = await uform_vision.get_classifications(image, 1, extra={"question": prompt})
    print(f"empty table pic result: {uform_vision_return_value[0].class_name}")

    image = Image.open( os.getcwd() + "/test/cattable.jpg")
    uform_vision_return_value = await uform_vision.get_classifications(image, 1, extra={"question": prompt})
    print(f"cat on table pic result: {uform_vision_return_value[0].class_name}")

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())