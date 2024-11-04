import base64
import requests
import json
from pathlib import Path
import os

def send_to_claude(api_key: str, user_message: str, screenshot_path: str = None):
    """
    Send a request to Claude with an optional screenshot and print the tool selection response
    """
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "content-type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "computer-use-2024-10-22"
    }

    # Prepare the content blocks
    content_blocks = []
    
    # Add screenshot if provided
    if screenshot_path:
        with open(screenshot_path, 'rb') as img:
            b64_image = base64.b64encode(img.read()).decode()
            content_blocks.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": b64_image
                }
            })
    
    # Add the user message
    content_blocks.append({
        "type": "text",
        "text": user_message
    })

    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1024,
        "tools": [
            {
                "type": "computer_20241022",
                "name": "computer", 
                "display_width_px": 1024,
                "display_height_px": 768,
                "display_number": 1
            },
            {
                "type": "text_editor_20241022",
                "name": "str_replace_editor"
            },
            {
                "type": "bash_20241022",
                "name": "bash"
            }
        ],
        "system": """
            You are a helpful assistant named Hal that can use a computer to perform tasks. 
            
            After each step, take a screenshot and describe the contents of the web page. Carefully evaluate if you have achieved the right outcome.
            
            Explicitly show your thinking in 3rd person: "Hal sees a picture of a giraffe. Hal has evaluated step X..." If not correct, try again. 
            
            Only when you confirm a step was executed correctly should you move on to the next one.""",
        "messages": [
            {
                "role": "user",
                "content": content_blocks
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print(f"\nUser Message: {user_message}")
        print("\nClaude's Response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Please set ANTHROPIC_API_KEY environment variable")
    
    # Test different scenarios with the Wikipedia screenshot
    test_cases = [
        {
            "message": "Click on the 'Talk' tab in the Wikipedia page",
            "screenshot": "/Users/shawnesquivel/GitHub/anthropic-quickstarts/computer-use-demo/wikipedia.png"
        },
        {
            "message": "Type 'neural networks' into the Wikipedia search box",
            "screenshot": "/Users/shawnesquivel/GitHub/anthropic-quickstarts/computer-use-demo/wikipedia.png"
        },
        {
            "message": "Create a new directory called 'neural_networks' and list its contents",
            "screenshot": None  # Bash commands don't need screenshots
        }
    ]
    
    for test in test_cases:
        send_to_claude(api_key, test["message"], test["screenshot"])
        print("\n" + "="*80 + "\n")