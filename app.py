from flask import Flask, render_template, views

import aws

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def home():
    return render_template("index.html")


app.add_url_rule('/aws', view_func=aws.aws_s3_index)
app.add_url_rule('/api/aws/s3/<bucket_name>', view_func=aws.get_all_items_in_bucket)
app.add_url_rule('/api/aws/s3/<bucket_name>/download/', methods=['POST'], view_func=aws.download_file)
app.add_url_rule('/api/aws/s3/<bucket_name>', methods=['DELETE'], view_func=aws.delete_file)
app.add_url_rule('/api/aws/s3/<bucket_name>', methods=['POST'], view_func=aws.upload_file)
app.add_url_rule('/api/aws/ec2/regions', view_func=aws.get_all_regions)
app.add_url_rule('/api/aws/ec2/regions/<region_name>', view_func=aws.get_all_instances)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
