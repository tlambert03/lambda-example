import json
import numpy as np
import base64
from PIL import Image
import io


def lambda_handler(event: dict, context) -> dict:
    """Main Lambda function

    https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html

    The default name in the Lambda console is `lambda_function.lambda_handler`.
    You can change it to whatever you want, but it should match the name in
    Dockerfile.
    """

    # Parse the input parameters from the event
    if "body" in event:
        params = json.loads(event["body"])
    else:
        params = event

    # example of doing a thing...
    shape = tuple(params.get("shape", (12, 12))) + (3,)
    image_array = np.random.randint(0, 256, shape, dtype=np.uint8)
    buffered = io.BytesIO()
    Image.fromarray(image_array).save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Return the response
    # What happens to the returned value depends on the invocation type and the
    # service that invoked the function.
    # https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html#python-handler-return
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"image": img_str}),
    }
