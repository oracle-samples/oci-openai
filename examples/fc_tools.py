# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from openai.types.responses.function_tool_param import FunctionToolParam


def get_stock_price(symbol: str) -> dict:
    """Get the current stock price for a given symbol."""
    print(f"Fetching stock price for {symbol}...")

    # Mock stock data
    return {
        "symbol": symbol.upper(),
        "price": 175.42 if symbol.upper() == "AAPL" else 198.76,
        "currency": "USD",
        "change": 2.34 if symbol.upper() == "AAPL" else -1.23,
        "change_percent": 1.35 if symbol.upper() == "AAPL" else -0.62,
        "last_updated": "2025-06-26T15:00:00Z",
    }


def get_current_weather(location: str, unit: str = "fahrenheit") -> dict:
    """Get current weather for a given location.

    Args:
        location: The city and state, e.g., San Francisco, CA
        unit: The unit of temperature (celsius or fahrenheit)

    Returns:
        dict: Weather information
    """
    # In a real application, you would call a weather API here
    # This is a mock implementation for demonstration
    print(f"Fetching weather for {location} in {unit}...")

    # Mock weather data
    weather_data = {
        "location": location,
        "temperature": "72",
        "unit": "fahrenheit",
        "forecast": ["sunny", "windy"],
        "humidity": "65%",
        "description": "Sunny with a gentle breeze",
    }

    return weather_data


def recommend_clothing(temperature, unit="fahrenheit"):
    """
    Returns clothing recommendations based on input temperature and unit.

    Parameters:
        temperature (float or int): The temperature value to base the recommendation on.
        unit (str, optional): The unit of the temperature value.
            Can be 'fahrenheit' or 'celsius'. Defaults to 'fahrenheit'.
    """
    # Convert to Fahrenheit if input is in Celsius
    if unit.lower() == "celsius":
        temperature = temperature * 9 / 5 + 32

    if temperature >= 80:
        return "It's hot! Wear shorts and a t-shirt."
    elif temperature >= 65:
        return "It's warm. A short-sleeve shirt and pants are fine."
    elif temperature >= 50:
        return "It's a bit chilly. Wear a light jacket or sweater."
    elif temperature >= 32:
        return "It's cold. Wear a coat, sweater, and possibly a hat."
    else:
        return "It's freezing! Dress warmly in layers, including a winter coat, gloves, and a hat."


fc_tools = [
    FunctionToolParam(
        name="get_current_weather",
        strict=True,
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia",
                }
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        type="function",
        description="Get current weather for a given location.",
    ),
    FunctionToolParam(
        name="recommend_clothing",
        strict=True,
        parameters={
            "type": "object",
            "properties": {
                "temperature": {
                    "type": "integer",
                    "description": "The temperature value to base the recommendation on.",
                }
            },
            "required": ["temperature"],
            "additionalProperties": False,
        },
        type="function",
        description="Returns clothing recommendations based on input temperature and unit.",
    ),
]


def execute_function_call(function_name, function_args):
    # Call the function
    if function_name == "get_current_weather":
        return get_current_weather(**function_args)
    elif function_name == "recommend_clothing":
        return recommend_clothing(**function_args)
    else:
        return None
