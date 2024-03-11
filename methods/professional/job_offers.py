import base64
import io
import json
import os
from io import BytesIO

import qrcode
from firebase_admin import credentials, exceptions, get_app, initialize_app, storage
from flask import jsonify, request
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

import syntax
from app import app
from methods.base import Methods
from methods.common import add_row, delete_row, make_query, row_to_dict, unique
from tables.professional.business import Business
from tables.professional.job_offers import JobOffers as TJobOffers


class JobOffers(Methods):
    def __init__(self):
        post_rules = [
            self.candidate_get_job_offers,
        ]
        Methods.__init__(self, post_methods=post_rules)

    @staticmethod
    @app.route(
        "/api/professional_get_job_offer/<pro_username>/<job_id>", methods=["GET"]
    )
    def professional_get_job_offer(pro_username, job_id):
        def inspect(_pdf_buffer):
            """For debug purpose."""
            _pdf_buffer.seek(0)
            with open("mypdf.pdf", "wb") as f:
                f.write(_pdf_buffer.getvalue())
            _pdf_buffer.seek(0)

        try:
            _ = get_app()
        except ValueError:
            cred = credentials.Certificate(os.environ.get("GOOGLE_CREDENTIALS"))
            _ = initialize_app(cred, {"storageBucket": "kicko-b75db.appspot.com"})
        bucket = storage.bucket()
        blob = bucket.blob(f"professional/{pro_username}/job_offer_qr_codes/{job_id}")
        byte_stream = BytesIO()
        blob.download_to_file(byte_stream)
        byte_stream.seek(0)
        # image = Image.open(byte_stream)
        image_reader = ImageReader(byte_stream)
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        # width, height = letter
        c.drawString(100, 700, "FOO")
        c.drawImage(image_reader, 100, 500, width=200, height=200)
        c.drawString(100, 450, "FOOBAR")
        c.save()
        """
        blob = bucket.blob(f"professional/{pro_username}/job_offer_pdfs/{job_id}.pdf")
        blob.upload_from_file(pdf_buffer, content_type="application/pdf")
        pdf_url = blob.public_url
        return jsonify({"success": True, "pdf_url": pdf_url})
        """
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

    def candidate_get_job_offers(self):
        input_json = request.get_json(force=True)
        filters = []
        city = input_json.get("city", None)
        if city is not None and city != syntax.all_cities:
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
