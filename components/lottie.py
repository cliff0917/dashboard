import os
from flask import send_from_directory

def serve_lottie(server):
    @server.route("/total", methods=['GET'])
    def serving_lottie_total():
        directory = os.path.join(os.getcwd(), "assets/lottie")
        return send_from_directory(directory, "total.json")

    @server.route("/alert", methods=['GET'])
    def serving_lottie_alert():
        directory = os.path.join(os.getcwd(), "assets/lottie")
        return send_from_directory(directory, "alert.json")

    @server.route("/failure", methods=['GET'])
    def serving_lottie_failure():
        directory = os.path.join(os.getcwd(), "assets/lottie")
        return send_from_directory(directory, "failure.json")

    @server.route("/success", methods=['GET'])
    def serving_lottie_success():
        directory = os.path.join(os.getcwd(), "assets/lottie")
        return send_from_directory(directory, "success.json")

    return server