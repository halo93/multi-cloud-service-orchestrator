from flask import render_template, jsonify, Response, request

from AwsEC2Service import AwsEC2Service
from AwsS3Service import AwsS3Service

awsS3Service = AwsS3Service()
awsEc2Service = AwsEC2Service()


def aws_s3_index():
    bucket_list = awsS3Service.print_content()
    return render_template("aws.html", bucket_list=bucket_list)


def get_all_items_in_bucket(bucket_name):
    items = awsS3Service.get_all_keys_in_bucket(bucket_name)
    if len(items) > 0:
        return jsonify({'data': render_template('file_list.html', items=items, chosen_bucket_name=bucket_name)})
    return jsonify({})


def download_file(bucket_name):
    file_name = request.form.get('file_name')
    response = awsS3Service.download_file(bucket_name, file_name)
    if response != 0:
        return Response(
            response,
            mimetype='application/octet-stream',
            headers={"Content-Disposition": "attachment;filename=" + file_name}
        )
    return 'Bad Request', 400


def delete_file(bucket_name):
    file_name = request.json['file_name']
    response = awsS3Service.delete_file(bucket_name, file_name)
    if response is True:
        items = awsS3Service.get_all_keys_in_bucket(bucket_name)
        return jsonify({'data': render_template('file_list.html', items=items, chosen_bucket_name=bucket_name)})
    return 'Bad Request', 400


def upload_file(bucket_name):
    file = request.files['file']
    response = awsS3Service.upload_file_object(file, bucket_name)
    if response is "":
        return 'Bad Request', 400
    items = awsS3Service.get_all_keys_in_bucket(bucket_name)
    return jsonify({'data': render_template('file_list.html', items=items, chosen_bucket_name=bucket_name)})


def get_all_regions():
    regions = awsEc2Service.list_regions()
    if len(regions) > 0:
        return jsonify({'data': render_template('region_list.html', region_list=regions)})
    return jsonify({})


def get_all_instances(region_name):
    instances = awsEc2Service.get_all_instances(region_name)
    if len(instances) > 0:
        return jsonify({'data': render_template('instance_list.html',
                                                chosen_region=region_name, instance_list=instances)})
    return jsonify({})
