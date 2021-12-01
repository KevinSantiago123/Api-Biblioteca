"""
Descriptive HTTP status codes, for code readability.

See RFC 2616 - https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
And RFC 6585 - https://tools.ietf.org/html/rfc6585
And RFC 4918 - https://tools.ietf.org/html/rfc4918
"""

__author__ = 'kcastanedat'


class StatusHttp():
    """Util class StatusHTTP.
    Clase que contiene los status y las respuestas para los servicios"""
    __status_values = {
            100: "",
            101: "",
            200: "",
            201: "Datos almacenados correctamente.",
            202: "",
            203: "",
            204: "",
            205: "",
            206: "",
            207: "",
            208: "",
            226: "",
            300: "",
            301: "",
            302: "",
            303: "",
            304: "",
            305: "",
            306: "",
            307: "",
            308: "",
            400: "La información ingresada no pudo ser procesada.",
            401: "No tiene autorización para continuar.",
            402: "Pago requerido.",
            403: "",
            404: "No se encontró la información solicitada.",
            405: "",
            406: "",
            407: "",
            408: "",
            409: "Ya existen datos con la información ingresada.",
            410: "",
            411: "",
            412: "",
            413: "",
            414: "",
            415: "",
            416: "",
            417: "",
            418: "",
            422: "",
            423: "",
            424: "",
            426: "",
            428: "",
            429: "",
            431: "",
            451: "",
            500: "Hubo un error al procesar la petición.",
            501: "",
            502: "",
            503: "",
            504: "",
            505: "",
            506: "",
            507: "",
            508: "",
            509: "",
            510: "",
            511: ""
        }

    @classmethod
    def status(self, status_type, description_error=None):
        """Genera el contenido y el estatus de la respuesta del servicio"""
        select_response = {"status": status_type}
        if self.__status_values[status_type] != "":
            select_response['data'] = {"Message": self.__status_values[status_type]}
            if description_error != None:
                select_response['data'].update({"Descripcion_Error": description_error})
        elif description_error != None:
            select_response['data'] = {"Descripcion_Error": description_error}
        return select_response
