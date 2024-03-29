# uform modular vision service

This module implements the [rdk vision API](https://github.com/rdk/vision-api) in a viam-labs:vision:uform model.

This model leverages the [UForm vision language model](https://huggingface.co/unum-cloud/uform-gen2-qwen-500m) to allow for image classification and querying.

The UForm model and inference will run locally, and therefore speed of inference is highly dependant on hardware.

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the `viam-labs:vision:uform` model from the [viam-labs uform-vision module](https://app.viam.com/module/viam-labs/uform-vision).

## Configure your vision service

> [!NOTE]  
> Before configuring your vision service, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/).
Click on the **Service** subtab and click **Create service**.
Select the `vision` type, then select the `viam-labs:vision:uform` model.
Enter a name for your vision service and click **Create**.

On the new service panel, copy and paste the following attribute template into your vision service's **Attributes** box:

```json
{
  "revision": "<optional model revision>"
}
```

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `viam-labs:vision:yolov8` model:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `max_tokens` | number | optional |  Max tokens to return, default 256 |

### Example Configurations

```json
{
  "max_tokens": 128
}
```

## API

The uform resource provides the following methods from Viam's built-in [rdk:service:vision API](https://python.viam.dev/autoapi/viam/services/vision/client/index.html)

### get_classifications(image=*binary*, count)

### get_classifications_from_camera(camera_name=*string*, count)

Note: if using this method, any cameras you are using must be set in the `depends_on` array for the service configuration, for example:

```json
      "depends_on": [
        "cam"
      ]
```

By default, the UForm model will be asked the question "describe this image".
If you want to ask a different question about the image, you can pass that question as the extra parameter "question".
For example:

``` python
uform.get_classifications(image, 1, extra={"question": "what is the person wearing?"})
```
