import requests

class DiceAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def send_roll(self, user: str, dice_notation: str, result: dict) -> None:
        """
        Sends roll data to external API.
        """
        payload = {
            "user": user,
            "notation": dice_notation,
            "result": result
        }
        try:
            response = requests.post(f"{self.base_url}/rolls", json=payload, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"API error: {e}")
