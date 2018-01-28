from urllib.parse import parse_qsl

from tornado.web import HTTPError

from engine.common.Handlers import DataHandler
from engine.common.Utils import paginate


class MySQLHandler(DataHandler):
    async def get(self, *args):
        # Retrieve city from request uri path
        # Path may be:
        # /api/xxxxxx
        # /api_cq/xxxxxx
        # /api_gy/xxxxxx
        path = self.request.path
        city = path.split('/')[1]

        if city == 'api':
            city = 'cd'
        else:
            city = city.split('_')[1]

        # Retrieve 'table_name' from request uri (last path)
        table_name = args[0]

        # Parse query parameters into dict
        params = dict(parse_qsl(self.request.query, True))

        # Retrieve and init page parameters
        if "page" in params:
            p = params["page"]
            del params["page"]
        else:
            p = ""

        if "page_size" in params:
            pz = params["page_size"]
            del params["page_size"]
        else:
            pz = ""

        page, page_size = self.init_paging_param(p, pz)

        # Specify table name
        sql_template = "SELECT * FROM {} WHERE 1=1"
        sql = sql_template.format(table_name)

        # Format SQL statement according to parameters
        for k in params:
            if params[k]:
                sql = sql + " AND " + k + " LIKE '%{" + k + "}%'"

        sql = sql.format(**params)
        # Add pager to SQL statement
        sql = paginate(sql).format(page, page_size)

        # This message will be sent to datagate
        msg = {
            "sql": sql,
            "city": city
        }

        try:
            # Access datagate to fetch data
            flag, result = await self.fetch_data(msg)
            if flag:
                raise HTTPError

            self.send_json_response(result)
        except HTTPError:
            self.send_json_response(self.config["error"]["DATAGATE_ACCESS_ERR"], 0)

