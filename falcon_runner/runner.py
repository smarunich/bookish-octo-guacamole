import json
import falcon
import jinja2
import os
import ansible_runner

def load_template(name):
    path = os.path.join('templates', name)
    with open(os.path.abspath(path), 'r') as fp:
        return jinja2.Template(fp.read())

class Index(object):
    def on_get(self, req, resp):
        runner = AnsibleRunner()
        template = load_template('index.j2')
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.body = template.render(path = runner.path, modules = sorted(runner.directories))

class AnsibleRunner(object):
    def __init__(self):
        self.path= '../modules'
        self.directories = []
        self.modules = []
        self.refresh()

    def refresh(self):
        self.directories = []
        self.modules = []
        for i in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, i)):
                self.directories.append(i)

    def on_get(self, req, resp, run=None):
        doc = {}
        if run is None:
            if 'refresh' in req.params:
                self.refresh()
            doc['directories'] = []
            for i in range(len(self.directories)):
                doc['directories'].append({'href': "%s%s/%s" % (req.prefix, req.path, self.directories[i])})
            doc['message'] = 'Provide param refresh=true to update directory listing'
        elif 'playbook' in req.params:
            if '_' in req.params.keys():
              req.params.pop('_')
            run_sync = ansible_runner.run(private_data_dir=os.path.join(self.path, run),rotate_artifacts=1, **req.params)
            doc['status'] = {}
            doc['status']['status'] = run_sync.status
            doc['status']['stdout'] = run_sync.stdout.readlines()
            doc['status']['stats'] = run_sync.stats
        else:
            doc['message'] = 'Params are passed to the runner eg playbook=testing.yml'
        resp.body = json.dumps(doc, ensure_ascii=False)
        if run_sync.status == "successful":
          resp.status = falcon.HTTP_200
        else:
          resp.status = falcon.HTTP_500
