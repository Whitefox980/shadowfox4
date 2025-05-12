import json
import openai

class AIBrain:
    def __init__(self, site_data):
        self.site_data = site_data

    def suggest_plan(self):
        prompt = f"""
Analiziraj sajt na osnovu sledećih informacija i predloži konkretne fuzz testove ili mutacije napada.

TITLE: {self.site_data.get('title')}
META: {self.site_data.get('meta')}
LINKOVI: {self.site_data.get('links')[:5]}

Vrati JSON u formatu: {{
  "SQL Injection": ["napad1", "napad2"],
  "XSS": ["napad1"],
  ...
}}

Koristi precizne tehničke izraze. Ne dodaj objašnjenja.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return json.loads(response.choices[0].message.content.strip())
        except Exception as e:
            return {"error": str(e)}
