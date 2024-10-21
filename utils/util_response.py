from fastapi import Response


class PDFResponse(Response):
    media_type = "application/pdf"

class SVGResponse(Response):
    media_type = "image/svg+xml"

class PNGResponse(Response):
    media_type = "image/png"

class JPEGResponse(Response):
    media_type = "image/jpeg"

class ExcelXlsxResponse(Response):
    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"