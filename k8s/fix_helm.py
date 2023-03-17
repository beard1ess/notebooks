# This is really stupid. :)
# Adds happy helm annotations to existing resources that should be annotated.

import subprocess
import yaml

chart_path = "./"
release_name = "RELEASE"
namespace = "NAMESPACE"

def helm_template(chart_path, release_name, namespace):
    command = f"helm template {release_name} {chart_path} --namespace {namespace}"
    output = subprocess.check_output(command, shell=True).decode('utf-8')
    return yaml.safe_load_all(output)

def resource_exists(api_version, kind, name, namespace):
    command = f"kubectl get {kind} {name} -n {namespace} -o jsonpath='{{.apiVersion}}'"
    try:
        existing_api_version = subprocess.check_output(command, shell=True).decode('utf-8')
        return existing_api_version.strip() == api_version
    except subprocess.CalledProcessError:
        return False


def add_helm_ownership_annotations(resource_type, resource_name, namespace, release_name):
    helm_annotations = {
        'meta.helm.sh/release-name': release_name,
        'meta.helm.sh/release-namespace': namespace
    }

    annotations_str = " ".join([f'{k}={v}' for k, v in helm_annotations.items()])
    command = f"kubectl annotate {resource_type} {resource_name} -n {namespace} {annotations_str} --overwrite"

    try:
        subprocess.run(command, shell=True, check=True, capture_output=True)
        print(f"Added Helm ownership annotations to {resource_type}/{resource_name} in namespace {namespace}")
    except subprocess.CalledProcessError as e:
        print(f"Error updating {resource_type}/{resource_name} annotations: {e.stderr.decode('utf-8').strip()}")

for document in helm_template(chart_path, release_name, namespace):
    if document is None:
        continue
    api_version = document['apiVersion']
    kind = document['kind']
    name = document['metadata']['name']

    if resource_exists(api_version, kind, name, namespace):
      print(f"{kind}/{name} in namespace {namespace} exists.")
      add_helm_ownership_annotations(kind.lower(), name, namespace, release_name)
    else:
      pass
        


