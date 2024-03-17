import base64
import io
import json
import os
from io import BytesIO

import qrcode
from firebase_admin import storage
from flask import jsonify, request
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

import syntax
from api.base import ApiController
from api.common import add_row, delete_row, make_query, row_to_dict, unique
from app import app
from models.professional.business import Business
from models.professional.job_offers import JobOffers as TJobOffers


def add_multiline_text(_canvas, text, start_x, start_y, line_height):
    lines = text.split("\n")
    current_y = start_y
    for line in lines:
        _canvas.drawString(start_x, current_y, line.strip())
        current_y -= line_height
    return current_y


class JobOffers(ApiController):
    @staticmethod
    @app.route(
        "/api/professional_get_job_offer/<pro_username>/<job_id>", methods=["GET"]
    )
    def professional_get_job_offer(pro_username, job_id, debug=False):
        def inspect(_pdf_buffer):
            """For debug purpose."""
            _pdf_buffer.seek(0)
            with open("inspect.pdf", "wb") as f:
                f.write(_pdf_buffer.getvalue())
            _pdf_buffer.seek(0)

        bucket = storage.bucket()
        blob = bucket.blob(f"professional/{pro_username}/job_offer_qr_codes/{job_id}")
        byte_stream = BytesIO()
        blob.download_to_file(byte_stream)
        byte_stream.seek(0)
        image_reader = ImageReader(byte_stream)
        pdf_buffer = BytesIO()
        _canvas = canvas.Canvas(pdf_buffer, pagesize=letter)
        job = row_to_dict(make_query(TJobOffers, TJobOffers.id == job_id).one())
        text = ""
        for attr in ["name", "description", "requires"]:
            if job.get(attr, None):
                prepend = ""
                if attr == "description":
                    prepend = "Description :"
                elif attr == "requires":
                    prepend = "Requis :"
                elif attr == "name":
                    prepend = "[Poste à pourvoir] Nous recrutons !"
                    prepend = f"{prepend} :" if job.get(attr, None) else prepend
                text += f"\n{prepend} {job.get(attr)} "
        text += "\n Veuillez scanner le code QR pour postuler:"
        current_y = 700
        if text:
            current_y = add_multiline_text(_canvas, text, 50, 700, 20)
        _canvas.drawImage(image_reader, 200, current_y - 200, width=200, height=200)
        _canvas.save()
        if debug:
            inspect(pdf_buffer)
        pdf_buffer.seek(0)
        res = base64.b64encode(pdf_buffer.getvalue()).decode("ascii")
        return json.dumps({"res": res})

    @staticmethod
    @app.route("/api/professional_get_job_offers/<pro_id>", methods=["GET"])
    def professional_get_job_offers(pro_id):
        legit_business = unique(Business, "id", Business.professional_id == pro_id)
        result = make_query(TJobOffers, TJobOffers.business_id.in_(legit_business))
        result = [row_to_dict(o) for o in result]
        result = jsonify(list(result))
        result.status_code = 200
        return result

    @staticmethod
    @app.route("/api/candidate_get_job_offer/<job_offer_id>", methods=["GET"])
    def candidate_get_job_offer(job_offer_id):
        result = make_query(TJobOffers, TJobOffers.id == job_offer_id).one()
        result = jsonify(row_to_dict(result))
        result.status_code = 200
        return result

    @staticmethod
    @app.route("/api/candidate_get_job_offers", methods=["POST"])
    def candidate_get_job_offers():
        input_json = request.get_json(force=True)
        filters = []
        city = input_json.get("city", None)
        if city and city != syntax.all_cities:
            legit_business = make_query(Business, Business.city == input_json["city"])
            legit_business = [row_to_dict(o) for o in legit_business]
            legit_business = list(map(lambda d: d["id"], legit_business))
            legit_business = list(set(legit_business))
            filters.append(TJobOffers.business_id.in_(legit_business))

        if len(filters) < 1:
            filters = None
        elif len(filters) < 2:
            filters = filters[0]

        result = make_query(TJobOffers, filters)
        result = [row_to_dict(o) for o in result]
        result = jsonify(list(result))
        result.status_code = 200
        return result

    @staticmethod
    @app.route("/api/add_job_offer", methods=["POST"])
    def add_job_offer():
        input_json = request.get_json(force=True)
        new_job_offer, session = add_row(TJobOffers, input_json, end_session=False)
        new_job_offer_id = str(new_job_offer.id)
        session.close()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(new_job_offer_id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        r_dict = {
            "img": base64.b64encode(img_byte_arr.getvalue()).decode("ascii"),
            "id": new_job_offer_id,
        }
        return json.dumps(r_dict)

    @staticmethod
    @app.route("/api/delete_job_offer/<pro_id>/<job_offer_id>", methods=["GET"])
    def delete_job_offer(pro_id, job_offer_id):
        legit_business = unique(Business, "id", Business.professional_id == pro_id)

        delete_row(
            TJobOffers,
            [TJobOffers.business_id.in_(legit_business), TJobOffers.id == job_offer_id],
        )
        resp = jsonify({"success": True})
        resp.status_code = 200
        return resp
