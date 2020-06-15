from flask import jsonify, Flask, Blueprint, g
from flask_apispec import marshal_with, doc
from schemas import hypervisor_schema
import boto3

app = Flask(__name__)
hypervisor_bp = Blueprint("hypervisor_api", "hypervisor_api", url_prefix='/api/hypervisor')


def create_ec2():
    sess_key = g.session["access_key"]
    sess_secret = g.session["secret_key"]
    region = g.session["region"]

    session = boto3.Session(aws_access_key_id=sess_key,
                            aws_secret_access_key=sess_secret,
                            region_name=region)
    ec2 = session.client('ec2')
    return ec2


@hypervisor_bp.route('/<session_id>/', methods=(["GET"]))
@marshal_with(hypervisor_schema.HypervisorResponseSchema(), code=200, description='Success')
@doc(info={'title': 'Hypervisor APIs'}, tags=['Hypervisor'], description="Get Hypervisor",
     responses={500: {'description': 'Failed to get Hypervisor'}})
def get_hypervisor(session_id):
    ec2 = create_ec2()
    response = {
        "name": "AWS EC2 " + ec2.meta.region_name,
        "api_version": 1,
        "management_server_id": ec2.meta.region_name,
        "supports_zones": True,
        "support_summary": {
            "vm_create_requires_existing_storage": False,
            "vm_change_id": False,
            "vm_set_id": False
        }
    }
    return jsonify(response)
