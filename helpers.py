import json
import time
from selenium.common import WebDriverException

def retrieve_phone_code(driver) -> str:
    """
    Este método intercepta el log de rendimiento del navegador
    para extraer el código de confirmación SMS.
    """
    all_logs = []
    for _ in range(10):
        try:
            all_logs.extend(driver.get_log('performance'))
            matching_logs = [
                log["message"] for log in all_logs
                if log.get("message") and 'api/v1/number?number' in log.get("message")
            ]
            for log in reversed(matching_logs):
                message_data = json.loads(log)["message"]
                params = message_data.get("params", {})
                request_id = params.get("requestId")
                if request_id:
                    body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                    code = ''.join([x for x in body['body'] if x.isdigit()])
                    if code:
                        return code
        except WebDriverException:
            pass
        time.sleep(1)
    raise Exception("No se encontró el código de confirmación del teléfono.")