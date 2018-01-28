from tornado.web import HTTPError
from engine.common.Handlers import DataHandler


class RedisHandler(DataHandler):
    async def get(self):
        # Get last request uri path as key
        url = self.request.path
        key = url.split('/')[-1]

        amount = self.get_arguments("amount")
        if len(amount) and amount[0]:

            msg = {
                "key": key,
                "filter": int(float(amount[0]))
            }
        else:
            msg = {
                "key": key
            }
        try:
            # Access datagate to fetch data
            flag, result = await self.fetch_data(msg)
            if flag:
                raise HTTPError

            self.send_json_response(result)
        except HTTPError:
            self.send_json_response(self.config["error"]["DATAGATE_ACCESS_ERR"], 0)

