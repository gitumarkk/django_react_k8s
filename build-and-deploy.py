import argparse
import os
from pathlib import Path

def get_docker_image(tag, env):
  return f'gcr.io/<PROJECT_ID>/django_react_k8s:{tag}'

def get_bucket(env):
  return f'<BUCKET_PREFIX>-{env}'

def build(tag, env):
  os.system('rm -rf static/build/*')
  os.system('find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf')
  os.system(f'REACT_GCLOUD_BUCKET={get_bucket(env)} npm run --prefix static build')
  os.system(f'docker build -t {get_docker_image(tag, env)} .')

def deploy(tag, env):
  os.system('rm -rf collectstatic/*')
  os.system('python manage.py collectstatic -i node_modules --noinput')
  os.system(f'gsutil -m cp -Z -a public-read -r ./collectstatic/* gs://{get_bucket(env)}/static')
  os.system(f'docker push {get_docker_image(tag, env)}')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--tag', help='The docker tag to use', required=True)
  parser.add_argument('--env', help='The environment to deploy to', default='staging')
  args = parser.parse_args()

  build(args.tag, args.env)
  deploy(args.tag, args.env)
