import json
from rich import print

from examples.common import oci_openai_client
from openai.types.responses import ResponseFunctionToolCall
from openai.types.responses.response_input_param import FunctionCallOutput
from fc_tools import fc_tools, execute_function_call

model = "openai.gpt-4.1"

# Creates first request
response = oci_openai_client.responses.create(
  model=model,
  input="what is the weather in seattle?",
  previous_response_id=None, # root of the history
  tools=fc_tools
)
print(response.output)

# Based on output if it is function call, execute the function and provide output back
if isinstance(response.output[0], ResponseFunctionToolCall):
  obj = response.output[0]
  function_name = obj.name
  function_args = json.loads(obj.arguments)

  function_response = execute_function_call(function_name, function_args)

  response = oci_openai_client.responses.create(
    model=model,
    input=[FunctionCallOutput(
      type="function_call_output",
      call_id=obj.call_id,
      output=str(function_response),
    )],
    previous_response_id=response.id,
    tools=fc_tools
  )
  print(response.output)

# Ask followup question related to previoud context
response = oci_openai_client.responses.create(
  model=model,
  input="what clothes should i wear in this weather?",
  previous_response_id=response.id,
  tools=fc_tools
)
print(response.output)

# Based on FCTool execute the function tool output
if isinstance(response.output[0], ResponseFunctionToolCall):
  obj = response.output[0]
  function_name = obj.name
  function_args = json.loads(obj.arguments)

  function_response = execute_function_call(function_name, function_args)

  response = oci_openai_client.responses.create(
    model=model,
    input=[FunctionCallOutput(
      type="function_call_output",
      call_id=obj.call_id,
      output=str(function_response),
    )],
    previous_response_id=response.id,
    tools=fc_tools
  )
  print(response.output)

