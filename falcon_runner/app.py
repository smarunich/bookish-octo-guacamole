import falcon
from runner import AnsibleRunner
from runner import Index

api = application = falcon.API()

runner = AnsibleRunner()
index = Index()

api.add_route('/', index)
api.add_route('/runner/{run}', runner)
