import json
from loguru import logger
import aiohttp
import base64


with open("data/database.json") as d:
    database = json.load(d)

with open("data/birthdates.json") as b:
    birthdates = json.load(b)


class Utils:
    # Automatically push new data to Github
    async def pushdata(self):
        filenames = ["data/birthdates.json"]
        for filename in filenames:
            try:
                token = database["github_oath"]
                repo = "Ryxn7/Birthday-Bot"
                branch = "main"
                url = "https://api.github.com/repos/" + repo + "/contents/" + filename

                base64content = base64.b64encode(open(filename, "rb").read())

                async with aiohttp.ClientSession() as session:
                    async with session.get(url + '?ref=' + branch, headers={"Authorization": "token " + token}) as data:
                        data = await data.json()
                sha = data['sha']

                if base64content.decode('utf-8') + "\n" != data['content']:
                    message = json.dumps(
                        {"message": "Automatic data update.",
                        "branch": branch,
                        "content": base64content.decode("utf-8"),
                        "sha": sha}
                    )
                    async with aiohttp.ClientSession() as session:
                        async with session.put(url, data=message, headers={"Content-Type": "application/json",
                                                                            "Authorization": "token " + token}) as resp:
                            print(resp)
                else:
                    print("Nothing to update.")
            except Exception as e:
                logger.exception(e)

    
    def dateFormatter(self, month, day):
        m = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        _month = m[int(month)-1]
        month = _month
        
        if int(day) < 10:
            d = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
            _day = d[int(day)-1]
            day = _day

        return month, day